"""Gold sheet: N≥40, calibrate|holdout, five labels, four source tags."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from jev_choice_router.gold import (
    GOLD_COLUMNS,
    MIN_ROW_COUNT,
    SOURCE_TAGS,
    load_jsonl,
)
from jev_choice_router.types import CHOICES


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
GOLD_PATH = EXPERIMENT_ROOT / "data" / "gold.jsonl"
PILOT_B_LABELS = EXPERIMENT_ROOT.parent / "jev-pilot-b" / "data" / "labels.jsonl"


class TestGoldSheet(unittest.TestCase):
    def test_gold_meets_plan(self) -> None:
        self.assertTrue(GOLD_PATH.is_file(), f"missing {GOLD_PATH}")
        rows = load_jsonl(GOLD_PATH)
        self.assertGreaterEqual(len(rows), MIN_ROW_COUNT)
        self.assertEqual(len({r.id for r in rows}), len(rows))
        for row in rows:
            self.assertEqual(set(row.to_dict()), set(GOLD_COLUMNS))
            self.assertTrue(row.state.strip(), f"{row.id}: empty state text")
            self.assertIn(row.gold, CHOICES)
            self.assertIn(row.split, {"calibrate", "holdout"})
            self.assertIn(row.source_tag, SOURCE_TAGS)

        golds = {r.gold for r in rows}
        self.assertEqual(golds, set(CHOICES))
        splits = Counter(r.split for r in rows)
        self.assertGreaterEqual(splits["calibrate"], 1)
        self.assertGreaterEqual(splits["holdout"], 1)
        # ~2/1: calibrate should outnumber holdout and not be a 1:1 split.
        self.assertGreater(splits["calibrate"], splits["holdout"])
        ratio = splits["calibrate"] / splits["holdout"]
        self.assertGreaterEqual(ratio, 1.5)
        self.assertLessEqual(ratio, 3.0)

        tags = {r.source_tag for r in rows}
        self.assertEqual(tags, set(SOURCE_TAGS))
        holdout_golds = {r.gold for r in rows if r.split == "holdout"}
        holdout_tags = {r.source_tag for r in rows if r.split == "holdout"}
        self.assertEqual(holdout_golds, set(CHOICES))
        self.assertGreaterEqual(len(holdout_tags), 3)

        counts = Counter(r.gold for r in rows)
        # Balance as evenly as practical: no class more than 2× another.
        self.assertLessEqual(max(counts.values()), 2 * min(counts.values()))

    def test_gold_lines_are_json(self) -> None:
        for line in GOLD_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                json.loads(line)

    def test_gold_does_not_copy_pilot_b_g1_rows(self) -> None:
        gold_states = {r.state.strip() for r in load_jsonl(GOLD_PATH)}
        if not PILOT_B_LABELS.is_file():
            self.skipTest("pilot b labels absent")
        pilot_artifacts: set[str] = set()
        for line in PILOT_B_LABELS.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            artifact = str(row.get("artifact", "")).strip()
            if artifact:
                pilot_artifacts.add(artifact)
        overlap = gold_states & pilot_artifacts
        self.assertEqual(overlap, set(), f"gold copied Pilot B artifacts: {overlap}")
