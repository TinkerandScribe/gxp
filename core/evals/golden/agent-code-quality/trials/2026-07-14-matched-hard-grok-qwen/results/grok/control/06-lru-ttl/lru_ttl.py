"""LruTtlCache — control implement from prompt."""

from __future__ import annotations

import time
from collections import OrderedDict


class LruTtlCache:
    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.ttl = ttl
        self.clock = time.monotonic if clock is None else clock
        self._data: OrderedDict = OrderedDict()
        self._exp: dict = {}

    def _is_expired(self, key) -> bool:
        if self.ttl is None:
            return False
        exp = self._exp.get(key)
        return exp is not None and self.clock() >= exp

    def _reap(self) -> None:
        for k in list(self._data.keys()):
            if self._is_expired(k):
                del self._data[k]
                self._exp.pop(k, None)

    def set(self, key, value) -> None:
        self._reap()
        if key in self._data:
            del self._data[key]
        elif len(self._data) >= self.capacity:
            old, _ = self._data.popitem(last=False)
            self._exp.pop(old, None)
        self._data[key] = value
        if self.ttl is not None:
            self._exp[key] = self.clock() + self.ttl
        else:
            self._exp.pop(key, None)

    def get(self, key):
        if key not in self._data:
            raise KeyError(key)
        if self._is_expired(key):
            del self._data[key]
            self._exp.pop(key, None)
            raise KeyError(key)
        self._data.move_to_end(key)
        return self._data[key]

    def delete(self, key) -> bool:
        if key in self._data:
            del self._data[key]
            self._exp.pop(key, None)
            return True
        return False

    def __len__(self) -> int:
        self._reap()
        return len(self._data)

    def __contains__(self, key) -> bool:
        if key not in self._data:
            return False
        if self._is_expired(key):
            del self._data[key]
            self._exp.pop(key, None)
            return False
        return True
