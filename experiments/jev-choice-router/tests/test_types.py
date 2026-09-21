"""Choice union is exactly five values; public types stay vendor-neutral."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path
from typing import get_args

from jev_choice_router.logging_shape import LOG_FIELDS, choice_log
from jev_choice_router.options import FROZEN_OPTIONS, load_frozen_options
from jev_choice_router.types import CHOICES, Choice, ChoiceInput, ChoiceResult


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
TYPES_PATH = EXPERIMENT_ROOT / "jev_choice_router" / "types.py"
OPTIONS_PATH = EXPERIMENT_ROOT / "options.json"

_BANNED_PUBLIC_IDENTIFIERS = frozenset(
    {
        "jev_classify",
        "JevClassify",
        "JevChoiceProvider",
        "noul",
        "Noul",
        "TypeSafe",
    }
)


class TestChoiceType(unittest.TestCase):
    def test_choice_has_exactly_five_values(self) -> None:
        values = get_args(Choice)
        self.assertEqual(len(values), 5)
        self.assertEqual(set(values), {"deterministic", "tool", "llm", "human", "halt"})
        self.assertEqual(CHOICES, values)

    def test_frozen_options_match_types_and_json(self) -> None:
        self.assertEqual(tuple(FROZEN_OPTIONS.keys()), CHOICES)
        data = load_frozen_options(OPTIONS_PATH)
        self.assertEqual(tuple(data["options"].keys()), CHOICES)
        self.assertEqual(data["options"]["deterministic"], "code/rules can finish this step")
        self.assertEqual(data["options"]["tool"], "call a named tool / retrieval")
        self.assertEqual(
            data["options"]["llm"],
            "generative model needed (draft / reason / explain)",
        )
        self.assertEqual(data["options"]["human"], "stop for review")
        self.assertEqual(data["options"]["halt"], "criteria met or hard stop")
        self.assertIs(data["add_none"], False)

    def test_public_types_have_no_jev_specific_names(self) -> None:
        source = TYPES_PATH.read_text(encoding="utf-8")
        lowered = source.lower()
        for token in ("jev_classify", "noul", "typesafe", "jevchoiceprovider"):
            self.assertNotIn(token, lowered, f"public types mention {token!r}")
        tree = ast.parse(source)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                names.add(node.name)
            elif isinstance(node, ast.arg):
                names.add(node.arg)
        leaked = names & _BANNED_PUBLIC_IDENTIFIERS
        self.assertEqual(leaked, set(), f"public types leaked {sorted(leaked)}")

    def test_choice_input_accepts_mapping(self) -> None:
        inp = ChoiceInput.from_mapping({"state": "run verify.sh", "question": "mode?"})
        self.assertEqual(inp.state, "run verify.sh")
        self.assertEqual(inp.question, "mode?")

    def test_log_fields_present_even_when_zero(self) -> None:
        result = ChoiceResult(
            label="halt",
            provider="jev",
            latency_ms=0.0,
            abstained=True,
            probability=0.0,
            cost_usd=0.0,
        )
        record = choice_log(result)
        self.assertEqual(tuple(record.keys()), LOG_FIELDS)
        self.assertEqual(record["label"], "halt")
        self.assertEqual(record["probability"], 0.0)
        self.assertEqual(record["latency_ms"], 0.0)
        self.assertEqual(record["cost_usd"], 0.0)
