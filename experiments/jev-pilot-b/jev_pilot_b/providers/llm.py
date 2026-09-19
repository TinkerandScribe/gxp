"""LLM judge stub — interface only; live calls are out of scope."""

from __future__ import annotations

import time

from jev_pilot_b.types import DecideInput, DecideResult


class LlmJudgeProvider:
    """Placeholder so cascade order can include an LLM slot.

    ``decide`` does not call any model. It abstains so a cascade can reach
    the next provider (typically human).
    """

    name = "llm"

    async def decide(self, input: DecideInput) -> DecideResult:
        started = time.perf_counter()
        _ = input
        return DecideResult(
            decision="needs_review",
            provider="llm",
            latency_ms=(time.perf_counter() - started) * 1000.0,
            abstained=True,
            raw={"reason": "llm_judge_not_implemented"},
        )
