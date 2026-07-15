"""CircuitBreaker — full closed / open / half-open implementation."""

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
        # Check if we should transition from open → half_open based on elapsed time
        if self.state.mode == "open" and self.state.opened_at is not None:
            elapsed = self.clock() - self.state.opened_at
            if elapsed >= self.open_seconds:
                self.state.mode = "half_open"
                self.state.successes = 0
        return self.state.mode

    def allow_request(self) -> bool:
        current_mode = self.mode()
        if current_mode == "closed":
            return True
        if current_mode == "open":
            return False
        # half_open: allow probe requests
        if current_mode == "half_open":
            return True
        return False

    def record_success(self) -> None:
        current_mode = self.mode()
        if current_mode == "closed":
            self.state.failures = 0
        elif current_mode == "half_open":
            self.state.successes += 1
            if self.state.successes >= self.success_threshold:
                # Transition back to closed
                self.state.mode = "closed"
                self.state.failures = 0
                self.state.successes = 0
        # In open state, success should not be recorded (requests shouldn't go through)

    def record_failure(self) -> None:
        current_mode = self.mode()
        if current_mode == "closed":
            self.state.failures += 1
            if self.state.failures >= self.failure_threshold:
                # Transition to open
                self.state.mode = "open"
                self.state.opened_at = self.clock()
                self.state.successes = 0
        elif current_mode == "half_open":
            # Any failure in half_open re-opens the circuit
            self.state.mode = "open"
            self.state.opened_at = self.clock()
            self.state.successes = 0

    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "CircuitBreaker":
        cfg = load_breaker_config(path)
        return cls(
            cfg["failure_threshold"],
            cfg["success_threshold"],
            cfg["open_seconds"],
            clock=clock,
        )
