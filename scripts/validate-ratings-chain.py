#!/usr/bin/env python3
"""Validate optional hash-chain fields in a ratings.jsonl ledger.

Lines without entry_hash are ignored for chaining (legacy / example rows).
When a line has entry_hash, prev_hash must match the previous chained line's
entry_hash (or be null/omitted for a re-anchor/genesis).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def entry_payload_hash(obj: dict) -> str:
    data = {k: v for k, v in obj.items() if k != "entry_hash"}
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main(path: Path) -> int:
    prev = None
    chained = 0
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        obj = json.loads(line)
        if obj.get("_schema"):
            continue
        eh = obj.get("entry_hash")
        if not eh:
            continue
        expected = entry_payload_hash(obj)
        if eh != expected:
            print(f"line {i}: entry_hash mismatch", file=sys.stderr)
            return 1
        ph = obj.get("prev_hash")
        if ph in (None, "", "null") and prev is None:
            prev = eh
            chained += 1
            continue
        if prev is None:
            # First chained line after unchained history — treat as re-anchor.
            prev = eh
            chained += 1
            continue
        if ph != prev:
            print(f"line {i}: prev_hash does not match previous entry_hash", file=sys.stderr)
            return 1
        prev = eh
        chained += 1
    print(f"OK ({chained} chained entries validated; unchained lines skipped)")
    return 0


if __name__ == "__main__":
    p = Path(sys.argv[1] if len(sys.argv) > 1 else "core/ratings.jsonl")
    sys.exit(main(p))
