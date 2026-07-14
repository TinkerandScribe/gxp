"""Per-key store."""
from __future__ import annotations
from collections import defaultdict
class HitStore:
    def __init__(self): self._hits=defaultdict(list)
    def record(self,key,ts): self._hits[key].append(ts)
    def hits_in_window(self,key,now,window_seconds):
        start=now-window_seconds
        kept=[t for t in self._hits.get(key,[]) if t>start]
        self._hits[key]=kept
        return sum(1 for t in kept if t<=now)
