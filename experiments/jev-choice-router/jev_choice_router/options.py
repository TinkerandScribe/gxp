"""Frozen jev_classify options for the five Choice labels.

Exact option text is the source of truth in ``options.json`` (also copied
into the README). Do not add a sixth label without a new experiment.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jev_choice_router.types import CHOICES, Choice

_OPTIONS_PATH = Path(__file__).resolve().parents[1] / "options.json"

FROZEN_QUESTION = "Which next-step mode should handle this step?"

FROZEN_OPTIONS: dict[Choice, str] = {
    "deterministic": "code/rules can finish this step",
    "tool": "call a named tool / retrieval",
    "llm": "generative model needed (draft / reason / explain)",
    "human": "stop for review",
    "halt": "criteria met or hard stop",
}


def load_frozen_options(path: Path | None = None) -> dict[str, Any]:
    """Read ``options.json`` and check it matches the in-code frozen map."""
    target = path or _OPTIONS_PATH
    data = json.loads(target.read_text(encoding="utf-8"))
    options = data.get("options")
    if not isinstance(options, dict):
        raise ValueError(f"{target}: missing options object")
    keys = tuple(options.keys())
    if keys != CHOICES:
        raise ValueError(f"{target}: options keys must be {CHOICES}, got {keys}")
    for key, expected in FROZEN_OPTIONS.items():
        if options[key] != expected:
            raise ValueError(
                f"{target}: option {key!r} text mismatch: {options[key]!r} != {expected!r}"
            )
    if data.get("question") != FROZEN_QUESTION:
        raise ValueError(f"{target}: question must be {FROZEN_QUESTION!r}")
    if data.get("add_none") is not False:
        raise ValueError(f"{target}: add_none must be false (one of five must apply)")
    return data
