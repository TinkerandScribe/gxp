"""Human terminal stub — cascade last resort (no UI)."""

from __future__ import annotations

import time

from jev_pilot_b.types import DecideInput, DecideResult


class HumanProvider:
    """Marks the item for a human without inventing a pass/fail.

    Does not abstain, so a cascade stops here.
    """

    name = "human"

    async def decide(self, input: DecideInput) -> DecideResult:
        started = time.perf_counter()
        _ = input
        return DecideResult(
            decision="needs_review",
            provider="human",
            latency_ms=(time.perf_counter() - started) * 1000.0,
            abstained=False,
            raw={"reason": "human_gate_stub"},
        )
