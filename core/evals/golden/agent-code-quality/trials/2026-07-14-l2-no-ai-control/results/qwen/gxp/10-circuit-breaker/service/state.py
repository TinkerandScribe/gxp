"""Breaker state — tracks mode, consecutive failures/successes, and opened_at."""

from __future__ import annotations


class BreakerState:
    def __init__(self) -> None:
        self.mode: str = "closed"  # "closed" | "open" | "half_open"
        self.failures: int = 0       # consecutive failures (used in closed)
        self.successes: int = 0      # consecutive successes (used in half_open)
        self.opened_at: float | None = None
