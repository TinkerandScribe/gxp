"""Decision union is exactly three values; public types stay vendor-neutral."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path
from typing import get_args

from jev_pilot_b.types import DECISIONS, DecideInput, Decision


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
TYPES_PATH = EXPERIMENT_ROOT / "jev_pilot_b" / "types.py"
# Names that must not appear as identifiers in the public types module.
_BANNED_PUBLIC_IDENTIFIERS = frozenset(
    {
        "jev_check",
        "JevCheck",
        "JevProvider",
        "noul",
        "Noul",
        "TypeSafe",
        "probability_yes",
    }
)


class TestDecisionType(unittest.TestCase):
    def test_decision_has_exactly_three_values(self) -> None:
        values = get_args(Decision)
        self.assertEqual(len(values), 3)
        self.assertEqual(set(values), {"pass", "fail", "needs_review"})
        self.assertEqual(DECISIONS, values)

    def test_public_types_have_no_jev_specific_names(self) -> None:
        source = TYPES_PATH.read_text(encoding="utf-8")
        lowered = source.lower()
        for token in ("jev_check", "noul", "typesafe", "probability_yes", "jevprovider"):
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

    def test_decide_input_accepts_camel_case_mapping(self) -> None:
        inp = DecideInput.from_mapping(
            {
                "artifact": "x",
                "question": "ok?",
                "yesMeans": "criterion holds",
                "noMeans": "criterion fails",
                "yesAtOrAbove": 0.8,
                "noAtOrBelow": 0.2,
            }
        )
        self.assertEqual(inp.yes_means, "criterion holds")
        self.assertEqual(inp.yes_at_or_above, 0.8)
