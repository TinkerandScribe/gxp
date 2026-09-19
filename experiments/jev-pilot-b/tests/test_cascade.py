"""Rules that always abstain let the cascade reach the next provider."""

from __future__ import annotations

import unittest

from jev_pilot_b.cascade import CASCADE_ORDER, cascade
from jev_pilot_b.gate_g1 import gate_g1
from jev_pilot_b.providers.human import HumanProvider
from jev_pilot_b.providers.llm import LlmJudgeProvider
from jev_pilot_b.providers.rules import RulesProvider
from jev_pilot_b.types import DecideInput, DecideResult


class RecordingProvider:
    def __init__(self, name: str, result: DecideResult) -> None:
        self.name = name
        self.result = result
        self.calls = 0

    async def decide(self, input: DecideInput) -> DecideResult:
        self.calls += 1
        _ = input
        return self.result


class TestCascade(unittest.IsolatedAsyncioTestCase):
    async def test_abstaining_rules_reach_next_provider(self) -> None:
        rules = RulesProvider(hooks=[lambda _inp: None])
        nxt = RecordingProvider(
            "jev",
            DecideResult(
                decision="pass",
                provider="jev",
                latency_ms=1.0,
                abstained=False,
                p=0.91,
            ),
        )
        result = await cascade(
            [rules, nxt],
            DecideInput(artifact="doc", question="Does the criterion hold?"),
        )
        self.assertEqual(nxt.calls, 1)
        self.assertEqual(result.provider, "jev")
        self.assertEqual(result.decision, "pass")
        self.assertFalse(result.abstained)

    async def test_empty_hooks_rules_also_abstain(self) -> None:
        nxt = RecordingProvider(
            "llm",
            DecideResult(
                decision="fail",
                provider="llm",
                latency_ms=2.0,
                abstained=False,
            ),
        )
        result = await cascade(
            [RulesProvider(), nxt],
            DecideInput(artifact="doc", question="q"),
        )
        self.assertEqual(result.provider, "llm")
        self.assertEqual(nxt.calls, 1)

    async def test_default_order_and_human_terminal(self) -> None:
        self.assertEqual(CASCADE_ORDER, ("rules", "jev", "llm", "human"))
        result = await cascade(
            [RulesProvider(), LlmJudgeProvider(), HumanProvider()],
            DecideInput(artifact={"k": 1}, question="ready for review?"),
        )
        self.assertEqual(result.provider, "human")
        self.assertEqual(result.decision, "needs_review")
        self.assertFalse(result.abstained)

    async def test_gate_g1_forwards_criterion(self) -> None:
        seen: list[str] = []

        class Capture:
            name = "rules"

            async def decide(self, input: DecideInput) -> DecideResult:
                seen.append(input.question)
                return DecideResult(
                    decision="pass",
                    provider="rules",
                    latency_ms=0.0,
                    abstained=False,
                )

        out = await gate_g1("artifact-body", "Criterion text holds?", Capture())
        self.assertEqual(seen, ["Criterion text holds?"])
        self.assertEqual(out.decision, "pass")

    async def test_cascade_requires_providers(self) -> None:
        with self.assertRaises(ValueError):
            await cascade([], DecideInput(artifact="x", question="q"))
