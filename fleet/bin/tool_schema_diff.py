#!/usr/bin/env python3
"""Compare two tool-schema snapshots (stdlib only; Plan C, Nov 9 item 5).

Snapshot JSON: {"<namespace>": {"<tool>": <input schema object or sha256 hex>}}.
Each schema is hashed (sha256 of canonical JSON) unless already a 64-hex string.

Exit 0: unchanged, or changes only in read-only namespaces (prints WARN lines).
Exit 1: a changed, new or removed tool in a write-capable namespace; prints
namespace, tool, old hash and new hash. Fail closed: a re-scoped write tool
needs a fresh approval before use.

Usage:
  python fleet/bin/tool_schema_diff.py --old a.json --new b.json
  python fleet/bin/tool_schema_diff.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

WRITE_CAPABLE = ("gmail", "resend", "agentmail", "vercel", "railway", "supabase",
                 "cloudflare", "posthog", "x", "github")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def is_write_capable(namespace: str) -> bool:
    ns = namespace.lower()
    for prefix in ("user-", "cursor-"):
        if ns.startswith(prefix):
            ns = ns[len(prefix):]
    ns = ns.split("--", 1)[0]
    head = re.split(r"[-_.]", ns)[0]
    return head in WRITE_CAPABLE or ns in WRITE_CAPABLE


def _hash(schema: object) -> str:
    if isinstance(schema, str) and HEX64.match(schema):
        return schema
    blob = json.dumps(schema, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def diff(old: dict, new: dict) -> tuple[list[str], list[str]]:
    blocks: list[str] = []
    warns: list[str] = []
    for ns in sorted(set(old) | set(new)):
        o = old.get(ns) or {}
        n = new.get(ns) or {}
        for tool in sorted(set(o) | set(n)):
            oh = _hash(o[tool]) if tool in o else "-"
            nh = _hash(n[tool]) if tool in n else "-"
            if oh == nh:
                continue
            line = f"{ns} {tool} old={oh} new={nh}"
            (blocks if is_write_capable(ns) else warns).append(line)
    return blocks, warns


def run(old_path: Path, new_path: Path) -> int:
    try:
        old = json.loads(old_path.read_text(encoding="utf-8"))
        new = json.loads(new_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR cannot read snapshots: {exc}")
        return 1
    if not isinstance(old, dict) or not isinstance(new, dict):
        print("ERROR snapshots must be JSON objects")
        return 1
    blocks, warns = diff(old, new)
    for w in warns:
        print(f"WARN read-only namespace change: {w}")
    for b in blocks:
        print(f"BLOCK write-capable schema drift: {b}")
    print("FAIL: write-capable tool schema changed; re-approve before use" if blocks else "OK")
    return 1 if blocks else 0


def self_test() -> int:
    a = {"user-Gmail": {"send_message": {"type": "object", "properties": {"to": {"type": "string"}}}},
         "user-logdriver": {"get_today": {"type": "object"}}}
    b = json.loads(json.dumps(a))
    b["user-Gmail"]["send_message"]["properties"]["bcc"] = {"type": "string"}
    c = json.loads(json.dumps(a))
    c["user-logdriver"]["get_week"] = {"type": "object"}
    d = json.loads(json.dumps(a))
    d["user-Resend"] = {"send_email": {"type": "object"}}
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        for name, doc in (("a", a), ("b", b), ("c", c), ("d", d)):
            (p / f"{name}.json").write_text(json.dumps(doc), encoding="utf-8")
        for label, new, want in (("unchanged", "a", 0), ("write-capable-changed", "b", 1),
                                 ("read-only-only", "c", 0), ("new-write-namespace", "d", 1)):
            got = run(p / "a.json", p / f"{new}.json")
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {label}: exit {got} (want {want})")
    print("tool_schema_diff self-test: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Compare tool-schema snapshots")
    ap.add_argument("--old", type=Path)
    ap.add_argument("--new", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.old or not args.new:
        ap.error("pass --old and --new, or --self-test")
    return run(args.old, args.new)


if __name__ == "__main__":
    sys.exit(main())
