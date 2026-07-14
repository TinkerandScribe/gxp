"""Per-key hit store with sliding window count."""

from __future__ import annotations

from collections import defaultdict


class HitStore:
    def __init__(self) -> None:
        self._hits: dict[str, list[float]] = defaultdict(list)

    def record(self, key: str, ts: float) -> None:
        self._hits[key].append(ts)

    def hits_in_window(self, key: str, now: float, window_seconds: float) -> int:
        start = now - window_seconds
        hits = self._hits.get(key, [])
        # keep only relevant timestamps to avoid unbounded growth
        kept = [t for t in hits if t > start]
        self._hits[key] = kept
        return sum(1 for t in kept if t <= now)
