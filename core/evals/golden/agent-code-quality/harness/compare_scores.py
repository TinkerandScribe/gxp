#!/usr/bin/env python3
"""Compare two score_trial.py JSON outputs (e.g. control vs gxp).

Usage:
  python .../compare_scores.py --a control.json --b gxp.json --label-a control --label-b gxp
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=Path, required=True)
    ap.add_argument("--b", type=Path, required=True)
    ap.add_argument("--label-a", default="A")
    ap.add_argument("--label-b", default="B")
    args = ap.parse_args()
    a, b = load(args.a), load(args.b)

    def row(s: dict) -> dict:
        return {
            "correctness": s.get("correctness"),
            "primary_code_score": s.get("primary_code_score"),
            "no_test_tamper": s.get("no_test_tamper"),
            "scope_ok": s.get("scope_ok"),
            "disqualified": s.get("disqualified"),
            "process_score": (s.get("process") or {}).get("process_score"),
        }

    ra, rb = row(a), row(b)
    # Winner on code quality
    if ra["disqualified"] and not rb["disqualified"]:
        winner = args.label_b
        reason = f"{args.label_a} disqualified (test tamper)"
    elif rb["disqualified"] and not ra["disqualified"]:
        winner = args.label_a
        reason = f"{args.label_b} disqualified (test tamper)"
    elif ra["disqualified"] and rb["disqualified"]:
        winner = "none"
        reason = "both disqualified"
    elif not ra["scope_ok"] or not rb["scope_ok"]:
        # prefer scoped
        if ra["scope_ok"] and not rb["scope_ok"]:
            winner = args.label_a
            reason = "scope"
        elif rb["scope_ok"] and not ra["scope_ok"]:
            winner = args.label_b
            reason = "scope"
        else:
            winner = "tie"
            reason = "both out of scope"
    else:
        ca, cb = float(ra["correctness"]), float(rb["correctness"])
        if abs(ca - cb) < 0.05:
            winner = "tie"
            reason = f"correctness within 0.05 ({ca} vs {cb})"
        elif cb > ca:
            winner = args.label_b
            reason = f"correctness {cb} > {ca}"
        else:
            winner = args.label_a
            reason = f"correctness {ca} > {cb}"

    out = {
        args.label_a: ra,
        args.label_b: rb,
        "code_quality_winner": winner,
        "reason": reason,
        "note": "process_score is informational only and does not decide the winner",
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
