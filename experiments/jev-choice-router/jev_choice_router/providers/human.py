"""Human terminal stub — cascade last resort (no UI)."""

from __future__ import annotations

import time

from jev_choice_router.types import ChoiceInput, ChoiceResult


class HumanProvider:
    """Stops for review. Does not abstain, so a cascade ends here."""

    name = "human"

    async def choose(self, input: ChoiceInput) -> ChoiceResult:
        started = time.perf_counter()
        _ = input
        return ChoiceResult(
            label="human",
            provider="human",
            latency_ms=(time.perf_counter() - started) * 1000.0,
            abstained=False,
            probability=0.0,
            cost_usd=0.0,
            raw={"reason": "human_gate_stub"},
        )
