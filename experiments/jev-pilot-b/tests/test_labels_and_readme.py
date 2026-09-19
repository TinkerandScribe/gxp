"""Label-sheet columns, README metrics, and experiment-tree guardrails."""

from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from jev_pilot_b.labels import (
    EXPECTED_CALIBRATE,
    EXPECTED_HOLDOUT,
    FILLED_CSV_NAME,
    FILLED_JSONL_NAME,
    LABEL_COLUMNS,
    PLANNED_ROW_COUNT,
    SOURCE_TAGS,
    load_csv,
    load_jsonl,
)

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
README = EXPERIMENT_ROOT / "README.md"
TEMPLATE_JSONL = EXPERIMENT_ROOT / "data" / "labels.template.jsonl"
TEMPLATE_CSV = EXPERIMENT_ROOT / "data" / "labels.template.csv"
FILLED_JSONL = EXPERIMENT_ROOT / "data" / FILLED_JSONL_NAME
FILLED_CSV = EXPERIMENT_ROOT / "data" / FILLED_CSV_NAME

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
        rows = load_jsonl(TEMPLATE_JSONL)
        self.assertGreaterEqual(len(rows), 5)
        self.assertTrue(all(set(r.to_dict()) == set(LABEL_COLUMNS) for r in rows))
        splits = {r.split for r in rows}
        self.assertEqual(splits, {"calibrate", "holdout"})
        golds = {r.gold for r in rows}
        self.assertTrue(golds <= {"pass", "fail", "needs_review"})
        self.assertTrue({"pass", "fail", "needs_review"} <= golds)

    def test_csv_template_header_and_parse(self) -> None:
        with TEMPLATE_CSV.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(tuple(header), LABEL_COLUMNS)
        rows = load_csv(TEMPLATE_CSV)
        self.assertEqual(len(rows), len(load_jsonl(TEMPLATE_JSONL)))

    def test_filled_jsonl_is_exactly_120_valid_rows(self) -> None:
        self.assertTrue(FILLED_JSONL.is_file(), f"missing {FILLED_JSONL}")
        rows = load_jsonl(FILLED_JSONL)
        self.assertEqual(len(rows), PLANNED_ROW_COUNT)
        self.assertEqual(len({r.id for r in rows}), PLANNED_ROW_COUNT)
        for row in rows:
            self.assertEqual(set(row.to_dict()), set(LABEL_COLUMNS))
            self.assertTrue(row.artifact.strip(), f"{row.id}: empty artifact")
            self.assertTrue(row.criterion.strip(), f"{row.id}: empty criterion")
            self.assertIn(row.gold, {"pass", "fail", "needs_review"})
            self.assertIn(row.split, {"calibrate", "holdout"})

    def test_filled_split_counts_and_gold_coverage(self) -> None:
        rows = load_jsonl(FILLED_JSONL)
        split_counts = {name: 0 for name in ("calibrate", "holdout")}
        golds: set[str] = set()
        tags: set[str] = set()
        holdout_golds: set[str] = set()
        holdout_tags: set[str] = set()
        for row in rows:
            split_counts[row.split] += 1
            golds.add(row.gold)
            tags.add(row.source_tag)
            if row.split == "holdout":
                holdout_golds.add(row.gold)
                holdout_tags.add(row.source_tag)
        self.assertEqual(split_counts["calibrate"], EXPECTED_CALIBRATE)
        self.assertEqual(split_counts["holdout"], EXPECTED_HOLDOUT)
        self.assertEqual(golds, {"pass", "fail", "needs_review"})
        self.assertTrue(set(SOURCE_TAGS) <= tags)
        self.assertGreaterEqual(len(holdout_golds), 2)
        self.assertGreaterEqual(len(holdout_tags), 2)

    def test_filled_csv_matches_jsonl(self) -> None:
        with FILLED_CSV.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(tuple(header), LABEL_COLUMNS)
        jsonl_rows = load_jsonl(FILLED_JSONL)
        csv_rows = load_csv(FILLED_CSV)
        self.assertEqual(len(csv_rows), len(jsonl_rows))
        self.assertEqual([r.to_dict() for r in csv_rows], [r.to_dict() for r in jsonl_rows])


class TestReadmeAndGuardrails(unittest.TestCase):
    def test_readme_lists_cascade_and_metrics(self) -> None:
        text = README.read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertIn("rules", lowered)
        self.assertIn("jev", lowered)
        self.assertIn("llm", lowered)
        self.assertIn("human", lowered)
        for metric in (
            "accuracy",
            "calibration",
            "latency",
            "cost",
            "abstention",
            "disagreement",
        ):
            self.assertIn(metric, lowered)
        self.assertIn("data/labels.jsonl", text)
        self.assertIn("N=120", text)
        self.assertIn("80 calibrate", text)
        self.assertIn("40 holdout", text)
        self.assertIn("incomplete_evidence", text)
        self.assertIn("UNSHIPPED", text)
        self.assertIn("policy_v1", text)
        self.assertIn("empty_artifact", text)
        self.assertIn("fail_border_handoff", text)

    def test_spike_b_audit_covers_eight_holdout_ids(self) -> None:
        audit = EXPERIMENT_ROOT / "docs" / "spike_b_label_audit.md"
        self.assertTrue(audit.is_file(), f"missing {audit}")
        text = audit.read_text(encoding="utf-8")
        for row_id in ("042", "048", "083", "104", "105", "106", "107", "108"):
            self.assertIn(row_id, text)
        self.assertIn("keep gold", text.lower())
        rows = {r.id: r for r in load_jsonl(FILLED_JSONL)}
        for row_id in ("042", "048", "083", "104", "105", "106", "107", "108"):
            self.assertEqual(rows[row_id].gold, "needs_review", row_id)
            self.assertEqual(rows[row_id].split, "holdout", row_id)

    def test_default_cascade_has_no_policy_v1_cues(self) -> None:
        cascade_src = (EXPERIMENT_ROOT / "jev_pilot_b" / "cascade.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("policy_v1", cascade_src)
        self.assertNotIn("cue_list", cascade_src)

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
        for path in (TEMPLATE_JSONL, FILLED_JSONL):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    json.loads(line)
