"""High-precision rules hooks fire on a frozen positive fixture set."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jev_pilot_b.hooks import (
    EMPTY_ARTIFACT_HOOK,
    HIGH_PRECISION_HOOK_NAMES,
    HIGH_PRECISION_HOOKS,
    first_firing_hook,
)
from jev_pilot_b.providers.rules import RulesProvider
from jev_pilot_b.types import DecideInput

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "high_precision_hooks.json"


def _load_fixtures() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _input_from_row(row: dict) -> DecideInput:
    return DecideInput(artifact=row["artifact"], question=row["question"])


class TestHighPrecisionHooks(unittest.IsolatedAsyncioTestCase):
    def test_frozen_positive_set_is_non_empty(self) -> None:
        data = _load_fixtures()
        self.assertGreaterEqual(len(data["positive"]), 1)
        hooks_seen = {row["expect_hook"] for row in data["positive"]}
        self.assertIn(EMPTY_ARTIFACT_HOOK, hooks_seen)
        self.assertTrue(hooks_seen <= set(HIGH_PRECISION_HOOK_NAMES))

    async def test_frozen_positive_set_fires_named_hooks(self) -> None:
        provider = RulesProvider()
        for row in _load_fixtures()["positive"]:
            inp = _input_from_row(row)
            result = await provider.decide(inp)
            self.assertFalse(
                result.abstained,
                f"{row['id']}: default rules still abstained",
            )
            self.assertEqual(result.provider, "rules")
            self.assertEqual(result.decision, row["expect_decision"], row["id"])
            self.assertEqual(result.raw["hook"], row["expect_hook"], row["id"])
            self.assertEqual(first_firing_hook(inp), row["expect_hook"], row["id"])

    async def test_negative_fixtures_still_abstain(self) -> None:
        provider = RulesProvider()
        for row in _load_fixtures()["negative_abstain"]:
            result = await provider.decide(_input_from_row(row))
            self.assertTrue(result.abstained, row["id"])
            self.assertIsNone(first_firing_hook(_input_from_row(row)), row["id"])

    async def test_explicit_empty_hooks_restore_always_abstain(self) -> None:
        result = await RulesProvider(hooks=()).decide(
            DecideInput(artifact="", question="empty?")
        )
        self.assertTrue(result.abstained)

    def test_default_hook_tuple_has_no_policy_v1(self) -> None:
        names = [getattr(hook, "__name__", "") for hook in HIGH_PRECISION_HOOKS]
        self.assertNotIn("policy_v1", names)
        joined = " ".join(names)
        self.assertNotIn("cue", joined)
