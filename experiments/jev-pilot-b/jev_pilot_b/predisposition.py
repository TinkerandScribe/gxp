"""Decision-shape predisposition (not a cue list).

Named path: ``incomplete_evidence``.

If a structured artifact is incomplete, return ``needs_review`` *before*
Jev disposition. Optional ``fail_border_handoff`` routes a Jev ``fail``
whose p(yes) sits in ``(no_at_or_below, fail_border_mid)`` to human review.

``policy_v1`` cue lists stay UNSHIPPED and are not consulted here.
"""

from __future__ import annotations

import time
from dataclasses import replace

from jev_pilot_b.hooks import INCOMPLETE_EVIDENCE_HOOK, incomplete_evidence
from jev_pilot_b.types import DecideInput, DecideResult

# Path name frozen for README + verify.sh (do not rename without both).
INCOMPLETE_EVIDENCE_PATH = "incomplete_evidence"
FAIL_BORDER_HANDOFF = "fail_border_handoff"

# Documented fail-border band: (no_at_or_below, fail_border_mid).
# Defaults match jev_check (no ≤ 0.3, mid = 0.5). Open interval.
DEFAULT_NO_AT_OR_BELOW = 0.3
DEFAULT_FAIL_BORDER_MID = 0.5


def apply_incomplete_evidence_path(input: DecideInput) -> DecideResult | None:
    """Return a rules ``needs_review`` when the named path fires; else None.

    Callers invoke this *before* Jev. Default ``RulesProvider`` also registers
    the same hook so a normal cascade short-circuits the same way.
    """
    started = time.perf_counter()
    decision = incomplete_evidence(input)
    if decision is None:
        return None
    return DecideResult(
        decision=decision,
        provider="rules",
        latency_ms=(time.perf_counter() - started) * 1000.0,
        abstained=False,
        raw={
            "path": INCOMPLETE_EVIDENCE_PATH,
            "hook": INCOMPLETE_EVIDENCE_HOOK,
        },
    )


def apply_fail_border_handoff(
    result: DecideResult,
    *,
    no_at_or_below: float = DEFAULT_NO_AT_OR_BELOW,
    fail_border_mid: float = DEFAULT_FAIL_BORDER_MID,
) -> DecideResult:
    """If Jev fail with p(yes) in (no_at_or_below, mid), route needs_review.

    Confident fails (p ≤ no_at_or_below) stay fail. Missing p is unchanged.
    """
    if result.provider != "jev" or result.decision != "fail" or result.abstained:
        return result
    if result.p is None:
        return result
    if no_at_or_below < result.p < fail_border_mid:
        raw = dict(result.raw) if isinstance(result.raw, dict) else {"prior_raw": result.raw}
        raw["fail_border_handoff"] = True
        raw["fail_border_band"] = (no_at_or_below, fail_border_mid)
        raw["path"] = FAIL_BORDER_HANDOFF
        return replace(
            result,
            decision="needs_review",
            raw=raw,
        )
    return result
