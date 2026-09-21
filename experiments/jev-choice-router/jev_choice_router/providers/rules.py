"""Deterministic rules backend (hooks). Zero model calls.

Each hook returns a Choice or None. None means the hook abstains.
If every hook abstains, the provider abstains so a caller-owned cascade
can continue to the Jev stub / human.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence

from jev_choice_router.hooks import RULES_HOOKS, hook_name
from jev_choice_router.types import Choice, ChoiceInput, ChoiceResult

RuleHook = Callable[[ChoiceInput], Choice | None]


class RulesProvider:
    name = "rules"

    def __init__(self, hooks: Sequence[RuleHook] | None = None) -> None:
        if hooks is None:
            self.hooks: tuple[RuleHook, ...] = RULES_HOOKS
        else:
            self.hooks = tuple(hooks)

    async def choose(self, input: ChoiceInput) -> ChoiceResult:
        started = time.perf_counter()
        for hook in self.hooks:
            label = hook(input)
            if label is not None:
                return ChoiceResult(
                    label=label,
                    provider="rules",
                    latency_ms=_elapsed_ms(started),
                    abstained=False,
                    probability=1.0,
                    cost_usd=0.0,
                    confidence=1.0,
                    raw={"hook": hook_name(hook), "model_calls": 0},
                )
        return ChoiceResult(
            label="human",
            provider="rules",
            latency_ms=_elapsed_ms(started),
            abstained=True,
            probability=0.0,
            cost_usd=0.0,
            raw={"reason": "all_hooks_abstained", "hook_count": len(self.hooks), "model_calls": 0},
        )


def _elapsed_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000.0
