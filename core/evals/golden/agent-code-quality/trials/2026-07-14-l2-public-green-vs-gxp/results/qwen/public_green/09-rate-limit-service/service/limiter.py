"""RateLimiter — fixed: check-then-record, proper window, zero-max deny."""

from __future__ import annotations

import time

from service.config import load_limits
from service.store import HitStore


class RateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        *,
        clock=None,
        store: HitStore | None = None,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clock = clock or time.monotonic
        self.store = store or HitStore()

    def allow(self, key: str) -> bool:
        # If max_requests is 0, always deny
        if self.max_requests == 0:
            return False
        now = self.clock()
        hits = self.store.hits_in_window(key, now, self.window_seconds)
        # Check BEFORE recording: if already at limit, deny
        if hits >= self.max_requests:
            return False
        # Record the hit and allow
        self.store.record(key, now)
        return True

    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "RateLimiter":
        lim = load_limits(path)
        return cls(lim["max_requests"], lim["window_seconds"], clock=clock)
