"""Cascade: rules → jev_stub → confidence floor → human."""

from __future__ import annotations

import unittest

from jev_choice_router.cascade import CASCADE_ORDER, apply_confidence_floor, cascade, default_providers
from jev_choice_router.flags import is_choice_router_enabled
from jev_choice_router.providers.human import HumanProvider
from jev_choice_router.providers.jev import JevChoiceProvider, JevClassifyRequest, JevClassifyResponse
from jev_choice_router.providers.rules import RulesProvider
from jev_choice_router.route import route_choice
from jev_choice_router.types import ChoiceInput, ChoiceResult


class RecordingProvider:
    def __init__(self, name: str, result: ChoiceResult) -> None:
        self.name = name
        self.result = result
        self.calls = 0

    async def choose(self, input: ChoiceInput) -> ChoiceResult:
        self.calls += 1
        _ = input
        return self.result


class FakeClassifyClient:
    def __init__(self, response: JevClassifyResponse) -> None:
        self.response = response
        self.requests: list[JevClassifyRequest] = []

    def classify(self, request: JevClassifyRequest) -> JevClassifyResponse:
        self.requests.append(request)
        return self.response


class TestCascade(unittest.IsolatedAsyncioTestCase):
    async def test_abstaining_rules_reach_jev(self) -> None:
        rules = RulesProvider(hooks=[lambda _inp: None])
        client = FakeClassifyClient(
            JevClassifyResponse(
                label="tool",
                probabilities={"tool": 0.91},
                confidence=0.91,
                action="act",
            )
        )
        jev = JevChoiceProvider(client, enabled=True)
        result = await cascade(
            [rules, jev, HumanProvider()],
            ChoiceInput(state="Decide the next mode for this leftover step."),
        )
        self.assertEqual(len(client.requests), 1)
        self.assertEqual(result.provider, "jev")
        self.assertEqual(result.label, "tool")
        self.assertFalse(result.abstained)

    async def test_confidence_floor_forces_human(self) -> None:
        raw = ChoiceResult(
            label="llm",
            provider="jev",
            latency_ms=3.0,
            abstained=False,
            probability=0.41,
            confidence=0.41,
            cost_usd=0.0,
        )
        floored = apply_confidence_floor(raw, floor=0.6)
        self.assertEqual(floored.label, "human")
        self.assertEqual(floored.provider, "human")
        self.assertEqual(floored.raw["reason"], "confidence_floor")
        self.assertEqual(floored.raw["prior_label"], "llm")

        client = FakeClassifyClient(
            JevClassifyResponse(
                label="llm",
                probabilities={"llm": 0.41},
                confidence=0.41,
                action="act",
            )
        )
        result = await cascade(
            [RulesProvider(hooks=()), JevChoiceProvider(client, enabled=True), HumanProvider()],
            ChoiceInput(state="leftover step with no obvious rule"),
            confidence_floor=0.6,
        )
        self.assertEqual(result.label, "human")
        self.assertEqual(result.raw["reason"], "confidence_floor")

    async def test_default_order_and_human_terminal(self) -> None:
        self.assertEqual(CASCADE_ORDER, ("rules", "jev", "confidence_floor", "human"))
        result = await cascade(
            [RulesProvider(hooks=()), HumanProvider()],
            ChoiceInput(state={"step": "continue", "note": "no obvious rule"}),
        )
        self.assertEqual(result.provider, "human")
        self.assertEqual(result.label, "human")
        self.assertFalse(result.abstained)

    async def test_flag_off_omits_jev(self) -> None:
        self.assertFalse(is_choice_router_enabled({"CHOICE_ROUTER": "0"}))
        providers = default_providers(environ={"CHOICE_ROUTER": "0"})
        names = [p.name for p in providers]
        self.assertEqual(names, ["rules", "human"])
        self.assertNotIn("jev", names)

    async def test_flag_on_includes_jev(self) -> None:
        providers = default_providers(environ={"CHOICE_ROUTER": "1"})
        self.assertEqual([p.name for p in providers], ["rules", "jev", "human"])

    async def test_route_choice_rules_short_circuit(self) -> None:
        result = await route_choice(
            "Draft the PR body summarizing gold N and class counts.",
            environ={"CHOICE_ROUTER": "0"},
        )
        self.assertEqual(result.provider, "rules")
        self.assertEqual(result.label, "llm")

    async def test_cascade_requires_providers(self) -> None:
        with self.assertRaises(ValueError):
            await cascade([], ChoiceInput(state="x"))

    async def test_jev_unused_when_disabled(self) -> None:
        client = FakeClassifyClient(
            JevClassifyResponse(
                label="tool",
                probabilities={"tool": 0.99},
                confidence=0.99,
                action="act",
            )
        )
        result = await JevChoiceProvider(client, enabled=False).choose(
            ChoiceInput(state="leftover")
        )
        self.assertTrue(result.abstained)
        self.assertEqual(result.raw["reason"], "choice_router_unused")
        self.assertEqual(client.requests, [])
