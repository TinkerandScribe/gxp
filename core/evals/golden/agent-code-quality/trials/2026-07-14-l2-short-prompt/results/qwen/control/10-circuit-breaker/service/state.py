"""Breaker state — starter is a dumb always-closed flag."""

from __future__ import annotations


class BreakerState:
    def __init__(self) -> None:
        self.mode = "closed"
        self.failures = 0
        self.successes = 0
        self.opened_at: float | None = None
