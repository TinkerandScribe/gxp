"""RateLimiter — starter: record-before-check, allows max+1."""

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
        # BUG: record first; allow one past max; zero max still records then compares wrong
        now = self.clock()
        self.store.record(key, now)
        hits = self.store.hits_in_window(key, now, self.window_seconds)
        # off-by-one: permits max_requests + 1 accepts
        return hits <= self.max_requests + 1

    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "RateLimiter":
        lim = load_limits(path)
        return cls(lim["max_requests"], lim["window_seconds"], clock=clock)
