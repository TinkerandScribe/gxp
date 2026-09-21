"""Rules hooks fire on a frozen positive fixture set. Zero model calls."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from jev_choice_router.hooks import (
    EMPTY_STATE_HOOK,
    RULES_HOOK_NAMES,
    RULES_HOOKS,
    first_firing_hook,
)
from jev_choice_router.providers.jev import JevChoiceProvider
from jev_choice_router.providers.rules import RulesProvider
from jev_choice_router.types import ChoiceInput


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "rules_positives.json"


class ExplodingClassifyClient:
    def classify(self, request):  # noqa: ANN001
        raise AssertionError(f"model/client must not be called: {request!r}")


def _load_fixtures() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _input_from_row(row: dict) -> ChoiceInput:
    return ChoiceInput(state=row["state"])


class TestRulesHooks(unittest.IsolatedAsyncioTestCase):
    def test_frozen_positive_set_covers_named_hooks(self) -> None:
        data = _load_fixtures()
        self.assertGreaterEqual(len(data["positive"]), 1)
        hooks_seen = {row["expect_hook"] for row in data["positive"]}
        self.assertIn(EMPTY_STATE_HOOK, hooks_seen)
        self.assertTrue(hooks_seen <= set(RULES_HOOK_NAMES))
        for required in (
            "empty_state",
            "all_criteria_yes",
            "named_verify",
            "open_url_or_search",
            "draft_prose",
            "destructive_action",
        ):
            self.assertIn(required, hooks_seen)

    async def test_frozen_positive_set_fires_named_hooks(self) -> None:
        provider = RulesProvider()
        for row in _load_fixtures()["positive"]:
            inp = _input_from_row(row)
            result = await provider.choose(inp)
            self.assertFalse(result.abstained, f"{row['id']}: rules still abstained")
            self.assertEqual(result.provider, "rules")
            self.assertEqual(result.label, row["expect_label"], row["id"])
            self.assertEqual(result.raw["hook"], row["expect_hook"], row["id"])
            self.assertEqual(result.raw["model_calls"], 0, row["id"])
            self.assertEqual(first_firing_hook(inp), row["expect_hook"], row["id"])

    async def test_rules_path_zero_model_calls(self) -> None:
        from jev_choice_router.cascade import cascade
        from jev_choice_router.providers.human import HumanProvider

        rules = RulesProvider()
        jev = JevChoiceProvider(ExplodingClassifyClient(), enabled=True)
        result = await cascade(
            [rules, jev, HumanProvider()],
            ChoiceInput(state="Next: run bash scripts/verify.sh and record the exit code."),
        )
        self.assertEqual(result.provider, "rules")
        self.assertEqual(result.label, "deterministic")
        self.assertEqual(result.raw["model_calls"], 0)

    async def test_negative_fixtures_still_abstain(self) -> None:
        provider = RulesProvider()
        for row in _load_fixtures()["negative_abstain"]:
            result = await provider.choose(_input_from_row(row))
            self.assertTrue(result.abstained, row["id"])
            self.assertIsNone(first_firing_hook(_input_from_row(row)), row["id"])

    async def test_explicit_empty_hooks_restore_always_abstain(self) -> None:
        result = await RulesProvider(hooks=()).choose(ChoiceInput(state=""))
        self.assertTrue(result.abstained)

    def test_default_hooks_are_not_pilot_b_cues(self) -> None:
        names = [getattr(hook, "__name__", "") for hook in RULES_HOOKS]
        self.assertNotIn("policy_v1", names)
        self.assertNotIn("empty_artifact", names)
        self.assertNotIn("incomplete_evidence", names)
        self.assertNotIn("contradictory_markers", names)
        joined = " ".join(names)
        self.assertNotIn("cue", joined)
        self.assertNotIn("policy_v1", joined)
