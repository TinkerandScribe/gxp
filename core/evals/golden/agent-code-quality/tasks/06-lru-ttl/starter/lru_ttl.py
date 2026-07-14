"""Starter — naive dict cache; fails LRU order, TTL, capacity rules."""

from __future__ import annotations

import time


class LruTtlCache:
    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        self.capacity = capacity  # BUG: no validation
        self.ttl = ttl
        self.clock = clock or time.monotonic
        self._data: dict = {}

    def set(self, key, value) -> None:
        # BUG: no eviction, no TTL tracking
        self._data[key] = value

    def get(self, key):
        return self._data[key]

    def delete(self, key) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key) -> bool:
        return key in self._data
