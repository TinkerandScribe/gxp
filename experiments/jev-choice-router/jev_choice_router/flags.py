"""Opt-in flags. Default off: Jev path is unused.

Hard-usage hold: even when ``CHOICE_ROUTER=1``, this tree does not open a
network socket or call MCP. Live ``jev_classify`` stays a documented
would-call only.
"""

from __future__ import annotations

import os

CHOICE_ROUTER_ENV = "CHOICE_ROUTER"
CONFIDENCE_FLOOR_ENV = "CHOICE_CONFIDENCE_FLOOR"
DEFAULT_CONFIDENCE_FLOOR = 0.6


def is_choice_router_enabled(environ: dict[str, str] | None = None) -> bool:
    """True only when ``CHOICE_ROUTER=1`` (or lowercase ``true`` / ``yes``)."""
    env = os.environ if environ is None else environ
    raw = (env.get(CHOICE_ROUTER_ENV) or "").strip().lower()
    return raw in {"1", "true", "yes", "on"}


def read_confidence_floor(environ: dict[str, str] | None = None) -> float:
    env = os.environ if environ is None else environ
    raw = (env.get(CONFIDENCE_FLOOR_ENV) or "").strip()
    if not raw:
        return DEFAULT_CONFIDENCE_FLOOR
    value = float(raw)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{CONFIDENCE_FLOOR_ENV} must be in [0, 1], got {value}")
    return value
