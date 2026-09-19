"""Deterministic rules backend (hooks).

Each hook returns a Decision or None. None means the hook abstains.
If every hook abstains, the provider abstains so a caller-owned cascade
can continue.

Default hooks are the Spike B high-precision set (empty artifact,
contradictory markers, incomplete_evidence). Pass ``hooks=()`` to restore
the old always-abstain stub. ``policy_v1`` cue lists stay UNSHIPPED here.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence

from jev_pilot_b.hooks import HIGH_PRECISION_HOOKS, hook_name
from jev_pilot_b.types import DecideInput, DecideResult, Decision

RuleHook = Callable[[DecideInput], Decision | None]


class RulesProvider:
    name = "rules"

    def __init__(self, hooks: Sequence[RuleHook] | None = None) -> None:
        if hooks is None:
            self.hooks: tuple[RuleHook, ...] = HIGH_PRECISION_HOOKS
        else:
            self.hooks = tuple(hooks)

    async def decide(self, input: DecideInput) -> DecideResult:
        started = time.perf_counter()
        for hook in self.hooks:
            decision = hook(input)
            if decision is not None:
                raw: dict[str, object] = {"hook": hook_name(hook)}
                if hook_name(hook) == "incomplete_evidence":
                    raw["path"] = "incomplete_evidence"
                return DecideResult(
                    decision=decision,
                    provider="rules",
                    latency_ms=_elapsed_ms(started),
                    abstained=False,
                    raw=raw,
                )
        return DecideResult(
            decision="needs_review",
            provider="rules",
            latency_ms=_elapsed_ms(started),
            abstained=True,
            raw={"reason": "all_hooks_abstained", "hook_count": len(self.hooks)},
        )


def _elapsed_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000.0
