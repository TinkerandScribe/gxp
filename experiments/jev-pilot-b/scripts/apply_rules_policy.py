#!/usr/bin/env python3
"""Apply rules + incomplete_evidence (+ optional fail-border) without live Jev.

Holdout re-score with live Jev / MCP is the parent run's job after merge.
This script only exercises the structured incomplete-evidence path and the
high-precision hooks. It never opens a network socket or reads API keys.

Usage (from repo root or this experiment tree):

    python experiments/jev-pilot-b/scripts/apply_rules_policy.py
    python experiments/jev-pilot-b/scripts/apply_rules_policy.py --fixtures
    python experiments/jev-pilot-b/scripts/apply_rules_policy.py \\
        --artifact-json '{"evidence_complete": false}' --question 'POP present?'
    python experiments/jev-pilot-b/scripts/apply_rules_policy.py \\
        --jev-fail-p 0.41
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jev_pilot_b.predisposition import (  # noqa: E402
    DEFAULT_FAIL_BORDER_MID,
    DEFAULT_NO_AT_OR_BELOW,
    apply_fail_border_handoff,
    apply_incomplete_evidence_path,
)
from jev_pilot_b.providers.rules import RulesProvider  # noqa: E402
from jev_pilot_b.types import DecideInput, DecideResult  # noqa: E402

FIXTURE_PATH = ROOT / "tests" / "fixtures" / "high_precision_hooks.json"


async def _score(input: DecideInput) -> DecideResult:
    early = apply_incomplete_evidence_path(input)
    if early is not None:
        return early
    return await RulesProvider().decide(input)


def _print_result(label: str, result: DecideResult) -> None:
    raw = result.raw if isinstance(result.raw, dict) else {"raw": result.raw}
    print(
        json.dumps(
            {
                "id": label,
                "decision": result.decision,
                "provider": result.provider,
                "abstained": result.abstained,
                "p": result.p,
                "path": raw.get("path"),
                "hook": raw.get("hook"),
                "fail_border_handoff": raw.get("fail_border_handoff"),
            },
            ensure_ascii=False,
        )
    )


async def _run_fixtures() -> int:
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    failed = 0
    for row in data["positive"]:
        result = await _score(
            DecideInput(artifact=row["artifact"], question=row["question"])
        )
        _print_result(row["id"], result)
        if result.abstained or result.decision != row["expect_decision"]:
            failed += 1
            print(
                json.dumps(
                    {
                        "id": row["id"],
                        "error": "fixture_mismatch",
                        "expected": row["expect_decision"],
                    }
                ),
                file=sys.stderr,
            )
    return failed


def _apply_recorded_jev_fail(p_yes: float) -> DecideResult:
    """Replay a recorded Jev fail without calling MCP."""
    recorded = DecideResult(
        decision="fail",
        provider="jev",
        latency_ms=0.0,
        abstained=False,
        p=p_yes,
        raw={"verdict": "no", "source": "recorded_p_only"},
    )
    return apply_fail_border_handoff(
        recorded,
        no_at_or_below=DEFAULT_NO_AT_OR_BELOW,
        fail_border_mid=DEFAULT_FAIL_BORDER_MID,
    )


async def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures",
        action="store_true",
        default=True,
        help="Score the frozen high-precision fixture set (default).",
    )
    parser.add_argument(
        "--no-fixtures",
        action="store_false",
        dest="fixtures",
        help="Skip the frozen fixture pass.",
    )
    parser.add_argument(
        "--artifact-json",
        help="Structured artifact JSON for the incomplete_evidence path.",
    )
    parser.add_argument("--question", default="Does the criterion hold?")
    parser.add_argument(
        "--jev-fail-p",
        type=float,
        help=(
            "Recorded Jev p(yes) with verdict=no. Applies fail_border_handoff "
            "only — no live Jev."
        ),
    )
    args = parser.parse_args(argv)

    print(
        json.dumps(
            {
                "note": (
                    "Holdout re-score with live Jev is the parent run's job "
                    "after merge. This process is offline (rules + "
                    "incomplete_evidence + optional recorded fail-border)."
                ),
                "incomplete_evidence_path": "incomplete_evidence",
                "policy_v1": "UNSHIPPED",
            }
        )
    )
    failed = 0
    if args.fixtures:
        failed += await _run_fixtures()
    if args.artifact_json is not None:
        artifact = json.loads(args.artifact_json)
        result = await _score(
            DecideInput(artifact=artifact, question=args.question)
        )
        _print_result("cli-artifact", result)
    if args.jev_fail_p is not None:
        _print_result(f"recorded-jev-fail-p={args.jev_fail_p}", _apply_recorded_jev_fail(args.jev_fail_p))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
