"""Breaker state — tracks mode, counters, and timestamp."""

from __future__ import annotations


class BreakerState:
    def __init__(self) -> None:
        self.mode: str = "closed"  # "closed" | "open" | "half_open"
        self.failures: int = 0       # consecutive failures in closed state
        self.successes: int = 0      # consecutive successes in half_open state
        self.opened_at: float | None = None  # timestamp when opened
