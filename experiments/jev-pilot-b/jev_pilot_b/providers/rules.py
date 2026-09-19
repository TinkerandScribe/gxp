"""Deterministic rules backend (hooks).

Each hook returns a Decision or None. None means the hook abstains.
If every hook abstains (or no hooks are registered), the provider abstains
so a caller-owned cascade can continue.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence

from jev_pilot_b.types import DecideInput, DecideResult, Decision

RuleHook = Callable[[DecideInput], Decision | None]


class RulesProvider:
    name = "rules"

    def __init__(self, hooks: Sequence[RuleHook] | None = None) -> None:
        self.hooks: tuple[RuleHook, ...] = tuple(hooks or ())

    async def decide(self, input: DecideInput) -> DecideResult:
        started = time.perf_counter()
        for hook in self.hooks:
            decision = hook(input)
            if decision is not None:
                return DecideResult(
                    decision=decision,
                    provider="rules",
                    latency_ms=_elapsed_ms(started),
                    abstained=False,
                    raw={"hook": getattr(hook, "__name__", repr(hook))},
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
