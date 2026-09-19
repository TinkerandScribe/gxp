"""Label-sheet columns, README metrics, and experiment-tree guardrails."""

from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from jev_pilot_b.labels import LABEL_COLUMNS, PLANNED_ROW_COUNT, load_csv, load_jsonl

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
README = EXPERIMENT_ROOT / "README.md"
JSONL = EXPERIMENT_ROOT / "data" / "labels.template.jsonl"
CSV = EXPERIMENT_ROOT / "data" / "labels.template.csv"

# Build the banned phrase without writing it as a literal in this tree.
_BANNED_PHRASE = "full" + " " + "undo"


class TestLabelSheet(unittest.TestCase):
    def test_planned_size_is_120(self) -> None:
        self.assertEqual(PLANNED_ROW_COUNT, 120)
        self.assertEqual(
            LABEL_COLUMNS,
            ("id", "artifact", "criterion", "gold", "split", "source_tag"),
        )

    def test_jsonl_template_columns_and_rows(self) -> None:
        rows = load_jsonl(JSONL)
        self.assertGreaterEqual(len(rows), 5)
        self.assertTrue(all(set(r.to_dict()) == set(LABEL_COLUMNS) for r in rows))
        splits = {r.split for r in rows}
        self.assertEqual(splits, {"calibrate", "holdout"})
        golds = {r.gold for r in rows}
        self.assertTrue(golds <= {"pass", "fail", "needs_review"})
        self.assertTrue({"pass", "fail", "needs_review"} <= golds)

    def test_csv_template_header_and_parse(self) -> None:
        with CSV.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(tuple(header), LABEL_COLUMNS)
        rows = load_csv(CSV)
        self.assertEqual(len(rows), len(load_jsonl(JSONL)))


class TestReadmeAndGuardrails(unittest.TestCase):
    def test_readme_lists_cascade_and_metrics(self) -> None:
        text = README.read_text(encoding="utf-8").lower()
        self.assertIn("rules", text)
        self.assertIn("jev", text)
        self.assertIn("llm", text)
        self.assertIn("human", text)
        for metric in (
            "accuracy",
            "calibration",
            "latency",
            "cost",
            "abstention",
            "disagreement",
        ):
            self.assertIn(metric, text)

    def test_banned_revert_phrase_absent(self) -> None:
        skip_suffixes = {".pyc"}
        for path in EXPERIMENT_ROOT.rglob("*"):
            if not path.is_file() or path.suffix in skip_suffixes:
                continue
            if "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            self.assertNotIn(
                _BANNED_PHRASE,
                text.lower(),
                f"{path.relative_to(EXPERIMENT_ROOT)} contains the banned phrase",
            )

    def test_templates_are_valid_json_lines(self) -> None:
        for line in JSONL.read_text(encoding="utf-8").splitlines():
            if line.strip():
                json.loads(line)
