#!/usr/bin/env python3
"""Fixture tests for scripts/validate-job-contract.py (stdlib only).

Covers Plan A (ESCALATE packet), Plan B (passed criteria need verify_cmds and
at least one raw evidence ref; residual_failing_tests coverage) and Plan C
(subagent_scope_widening). Exit 0 when every case behaves as expected.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-job-contract.py"
FX = ROOT / "scripts" / "fixtures" / "job-contract"

# (fixture, expected exit, error code that must appear when exit is 1)
CASES = [
    ("escalate-full-packet.json", 0, None),
    ("escalate-no-packet.json", 1, "escalate_packet"),
    ("escalate-missing-packet.json", 1, "escalate_packet"),
    ("summary-only-evidence.json", 1, "summary_only_evidence"),
    ("summary-plus-raw-evidence.json", 0, None),
    ("prose-legacy-evidence.json", 1, "schema"),
    ("passed-empty-verify.json", 1, "passed_no_verify"),
    ("passed-empty-evidence.json", 1, "passed_no_evidence"),
    ("residual-uncovered.json", 1, "residual_uncovered"),
    ("residual-covered.json", 0, None),
    ("scope-widening.json", 1, "subagent_scope_widening"),
    ("scope-widening-tools.json", 1, "subagent_scope_widening"),
    ("scope-narrow.json", 0, None),
]


def main() -> int:
    failed = 0
    for name, want, code in CASES:
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FX / name)],
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == want and (code is None or f"ERROR {code}:" in proc.stderr)
        print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {proc.returncode} (want {want}{', ' + code if code else ''})")
        if not ok:
            print(proc.stdout + proc.stderr)
            failed = 1
    print("test-job-contract: " + ("FAIL" if failed else "PASS") + f" ({len(CASES)} cases)")
    return failed


if __name__ == "__main__":
    sys.exit(main())
