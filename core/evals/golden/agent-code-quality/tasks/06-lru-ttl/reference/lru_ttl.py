"""Reference LruTtlCache."""

from __future__ import annotations

import time
from collections import OrderedDict


class LruTtlCache:
    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be an integer >= 1")
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock if clock is not None else time.monotonic
        # key -> value; order = LRU (left) ... MRU (right)
        self._data: OrderedDict = OrderedDict()
        self._expiry: dict = {}

    def _expired(self, key) -> bool:
        if self.ttl is None:
            return False
        exp = self._expiry.get(key)
        if exp is None:
            return False
        return self.clock() >= exp

    def _reap(self) -> None:
        dead = [k for k in list(self._data.keys()) if self._expired(k)]
        for k in dead:
            del self._data[k]
            self._expiry.pop(k, None)

    def set(self, key, value) -> None:
        self._reap()
        if key in self._data:
            del self._data[key]
        elif len(self._data) >= self.capacity:
            old, _ = self._data.popitem(last=False)
            self._expiry.pop(old, None)
        self._data[key] = value
        if self.ttl is not None:
            self._expiry[key] = self.clock() + self.ttl
        else:
            self._expiry.pop(key, None)

    def get(self, key):
        if key not in self._data:
            raise KeyError(key)
        if self._expired(key):
            del self._data[key]
            self._expiry.pop(key, None)
            raise KeyError(key)
        self._data.move_to_end(key)
        return self._data[key]

    def delete(self, key) -> bool:
        if key in self._data:
            del self._data[key]
            self._expiry.pop(key, None)
            return True
        return False

    def __len__(self) -> int:
        self._reap()
        return len(self._data)

    def __contains__(self, key) -> bool:
        if key not in self._data:
            return False
        if self._expired(key):
            del self._data[key]
            self._expiry.pop(key, None)
            return False
        return True
