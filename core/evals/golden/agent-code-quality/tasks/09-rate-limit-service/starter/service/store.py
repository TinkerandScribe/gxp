"""Hit store — starter: global list, ignores key and window."""

from __future__ import annotations


class HitStore:
    def __init__(self) -> None:
        # BUG: single list for all keys
        self._hits: list[float] = []

    def record(self, key: str, ts: float) -> None:
        self._hits.append(ts)

    def hits_in_window(self, key: str, now: float, window_seconds: float) -> int:
        # BUG: ignores key and window entirely
        return len(self._hits)
