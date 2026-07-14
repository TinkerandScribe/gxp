"""LruTtlCache — GXP implement (criteria-first)."""

from __future__ import annotations

import time
from collections import OrderedDict


class LruTtlCache:
    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("invalid capacity")
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock if clock is not None else time.monotonic
        self._od: OrderedDict = OrderedDict()
        self._expiry: dict = {}

    def _expired(self, key) -> bool:
        if self.ttl is None:
            return False
        t = self._expiry.get(key)
        return t is not None and self.clock() >= t

    def _reap_expired(self) -> None:
        dead = [k for k in self._od if self._expired(k)]
        for k in dead:
            del self._od[k]
            self._expiry.pop(k, None)

    def set(self, key, value) -> None:
        self._reap_expired()
        if key in self._od:
            del self._od[key]
        elif len(self._od) >= self.capacity:
            victim, _ = self._od.popitem(last=False)
            self._expiry.pop(victim, None)
        self._od[key] = value
        if self.ttl is not None:
            self._expiry[key] = self.clock() + self.ttl
        else:
            self._expiry.pop(key, None)

    def get(self, key):
        if key not in self._od:
            raise KeyError(key)
        if self._expired(key):
            del self._od[key]
            self._expiry.pop(key, None)
            raise KeyError(key)
        self._od.move_to_end(key)
        return self._od[key]

    def delete(self, key) -> bool:
        if key not in self._od:
            return False
        del self._od[key]
        self._expiry.pop(key, None)
        return True

    def __len__(self) -> int:
        self._reap_expired()
        return len(self._od)

    def __contains__(self, key) -> bool:
        if key not in self._od:
            return False
        if self._expired(key):
            del self._od[key]
            self._expiry.pop(key, None)
            return False
        return True
