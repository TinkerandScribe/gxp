"""Hit store — fixed: per-key storage with proper sliding window."""

from __future__ import annotations

from collections import defaultdict


class HitStore:
    def __init__(self) -> None:
        # FIX: per-key dict instead of single global list
        self._hits: dict[str, list[float]] = defaultdict(list)

    def record(self, key: str, ts: float) -> None:
        self._hits[key].append(ts)

    def hits_in_window(self, key: str, now: float, window_seconds: float) -> int:
        # FIX: count only timestamps in (now - window_seconds, now]
        cutoff = now - window_seconds
        return sum(1 for t in self._hits[key] if t > cutoff and t <= now)
