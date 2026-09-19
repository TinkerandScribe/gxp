"""Label sheet for the N=120 Pilot B plan (template + row validation)."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from jev_pilot_b.types import DECISIONS, Decision

Gold = Decision
Split = Literal["calibrate", "holdout"]
SPLITS: tuple[Split, ...] = ("calibrate", "holdout")
LABEL_COLUMNS: tuple[str, ...] = (
    "id",
    "artifact",
    "criterion",
    "gold",
    "split",
    "source_tag",
)

# Filled Gate G1 sheet is N=120. Templates under data/labels.template.*
# remain a schema reference (stub rows only).
PLANNED_ROW_COUNT = 120
EXPECTED_CALIBRATE = 80
EXPECTED_HOLDOUT = 40
SOURCE_TAGS: tuple[str, ...] = ("gxp", "shop", "idea_gate", "adversarial")
FILLED_JSONL_NAME = "labels.jsonl"
FILLED_CSV_NAME = "labels.csv"


@dataclass(frozen=True)
class LabelRow:
    id: str
    artifact: str
    criterion: str
    gold: Gold
    split: Split
    source_tag: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "artifact": self.artifact,
            "criterion": self.criterion,
            "gold": self.gold,
            "split": self.split,
            "source_tag": self.source_tag,
        }


def parse_row(data: dict[str, str]) -> LabelRow:
    missing = [c for c in LABEL_COLUMNS if c not in data or data[c] == ""]
    if missing:
        raise ValueError(f"label row missing columns: {missing}")
    gold = data["gold"]
    if gold not in DECISIONS:
        raise ValueError(f"gold must be one of {DECISIONS}, got {gold!r}")
    split = data["split"]
    if split not in SPLITS:
        raise ValueError(f"split must be one of {SPLITS}, got {split!r}")
    return LabelRow(
        id=data["id"],
        artifact=data["artifact"],
        criterion=data["criterion"],
        gold=gold,  # type: ignore[arg-type]
        split=split,  # type: ignore[arg-type]
        source_tag=data["source_tag"],
    )


def load_jsonl(path: Path) -> list[LabelRow]:
    rows: list[LabelRow] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            try:
                rows.append(parse_row(json.loads(text)))
            except (ValueError, json.JSONDecodeError) as exc:
                raise ValueError(f"{path}:{line_no}: {exc}") from exc
    return rows


def load_csv(path: Path) -> list[LabelRow]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: missing header")
        header = tuple(reader.fieldnames)
        if header != LABEL_COLUMNS:
            raise ValueError(f"{path}: expected columns {LABEL_COLUMNS}, got {header}")
        return [parse_row(row) for row in reader]


def write_csv(path: Path, rows: Iterable[LabelRow]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(LABEL_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())


def write_jsonl(path: Path, rows: Iterable[LabelRow]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")
