"""CircuitBreaker — full state machine."""

from __future__ import annotations

import time

from service.config import load_breaker_config
from service.state import BreakerState


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int,
        success_threshold: int,
        open_seconds: float,
        *,
        clock=None,
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.open_seconds = open_seconds
        self.clock = clock or time.monotonic
        self.state = BreakerState()

    def mode(self) -> str:
        return self.state.mode

    def allow_request(self) -> bool:
        if self.state.mode == "closed":
            return True
        if self.state.mode == "open":
            # Check if enough time has elapsed to transition to half_open
            if self.state.opened_at is not None and (
                self.clock() - self.state.opened_at >= self.open_seconds
            ):
                self.state.mode = "half_open"
                self.state.successes = 0
                return True
            return False
        # half_open: allow probes
        if self.state.mode == "half_open":
            return True
        return False

    def record_success(self) -> None:
        if self.state.mode == "closed":
            self.state.failures = 0
        elif self.state.mode == "half_open":
            self.state.successes += 1
            if self.state.successes >= self.success_threshold:
                self.state.mode = "closed"
                self.state.failures = 0
                self.state.successes = 0
                self.state.opened_at = None

    def record_failure(self) -> None:
        if self.state.mode == "closed":
            self.state.failures += 1
            if self.state.failures >= self.failure_threshold:
                self.state.mode = "open"
                self.state.opened_at = self.clock()
        elif self.state.mode == "half_open":
            # Any failure in half_open re-opens immediately
            self.state.mode = "open"
            self.state.successes = 0
            self.state.opened_at = self.clock()

    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "CircuitBreaker":
        cfg = load_breaker_config(path)
        return cls(
            cfg["failure_threshold"],
            cfg["success_threshold"],
            cfg["open_seconds"],
            clock=clock,
        )
