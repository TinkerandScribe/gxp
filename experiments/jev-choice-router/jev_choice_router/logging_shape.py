"""Cascade log record. These four fields are always present, even when zero."""

from __future__ import annotations

from typing import Any, TypedDict

from jev_choice_router.types import ChoiceResult

LOG_FIELDS: tuple[str, ...] = ("label", "probability", "latency_ms", "cost_usd")


class ChoiceLog(TypedDict):
    label: str
    probability: float
    latency_ms: float
    cost_usd: float


def choice_log(result: ChoiceResult) -> ChoiceLog:
    """Project a result onto the documented log shape (stub zeros allowed)."""
    return {
        "label": result.label,
        "probability": float(result.probability if result.probability is not None else 0.0),
        "latency_ms": float(result.latency_ms if result.latency_ms is not None else 0.0),
        "cost_usd": float(result.cost_usd if result.cost_usd is not None else 0.0),
    }


def assert_log_fields(record: dict[str, Any]) -> None:
    missing = [name for name in LOG_FIELDS if name not in record]
    if missing:
        raise ValueError(f"choice log missing fields: {missing}")
