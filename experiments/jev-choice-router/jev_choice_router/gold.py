"""Gold sheet for the step-choice experiment (N≥40, calibrate|holdout)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from jev_choice_router.types import CHOICES, Choice

Split = Literal["calibrate", "holdout"]
SPLITS: tuple[Split, ...] = ("calibrate", "holdout")
SOURCE_TAGS: tuple[str, ...] = ("gxp", "harness", "iscp", "synthetic")
GOLD_COLUMNS: tuple[str, ...] = ("id", "state", "gold", "split", "source_tag")

MIN_ROW_COUNT = 40
FILLED_JSONL_NAME = "gold.jsonl"


@dataclass(frozen=True)
class GoldRow:
    id: str
    state: str
    gold: Choice
    split: Split
    source_tag: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "state": self.state,
            "gold": self.gold,
            "split": self.split,
            "source_tag": self.source_tag,
        }


def parse_row(data: dict[str, str]) -> GoldRow:
    missing = [c for c in GOLD_COLUMNS if c not in data or data[c] == ""]
    if missing:
        raise ValueError(f"gold row missing columns: {missing}")
    gold = data["gold"]
    if gold not in CHOICES:
        raise ValueError(f"gold must be one of {CHOICES}, got {gold!r}")
    split = data["split"]
    if split not in SPLITS:
        raise ValueError(f"split must be one of {SPLITS}, got {split!r}")
    tag = data["source_tag"]
    if tag not in SOURCE_TAGS:
        raise ValueError(f"source_tag must be one of {SOURCE_TAGS}, got {tag!r}")
    return GoldRow(
        id=data["id"],
        state=data["state"],
        gold=gold,  # type: ignore[arg-type]
        split=split,  # type: ignore[arg-type]
        source_tag=tag,
    )


def load_jsonl(path: Path) -> list[GoldRow]:
    rows: list[GoldRow] = []
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


def write_jsonl(path: Path, rows: Iterable[GoldRow]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")
