"""Breaker state — tracks mode, consecutive failures/successes, and opened_at."""

from __future__ import annotations


class BreakerState:
    def __init__(self) -> None:
        self.mode: str = "closed"  # "closed" | "open" | "half_open"
        self.consecutive_failures: int = 0
        self.consecutive_successes: int = 0
        self.opened_at: float | None = None
