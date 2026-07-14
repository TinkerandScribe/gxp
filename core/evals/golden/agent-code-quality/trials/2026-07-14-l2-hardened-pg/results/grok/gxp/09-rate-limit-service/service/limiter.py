"""RateLimiter GXP."""
from __future__ import annotations
import time
from service.config import load_limits
from service.store import HitStore
class RateLimiter:
    def __init__(self,max_requests,window_seconds,*,clock=None,store=None):
        self.max_requests=int(max_requests); self.window_seconds=float(window_seconds)
        self.clock=clock if clock is not None else time.monotonic
        self.store=store if store is not None else HitStore()
    def allow(self,key):
        if self.max_requests<=0: return False
        now=self.clock()
        if self.store.hits_in_window(key,now,self.window_seconds)>=self.max_requests: return False
        self.store.record(key,now); return True
    @classmethod
    def from_config(cls,path=None,*,clock=None):
        lim=load_limits(path); return cls(lim['max_requests'],lim['window_seconds'],clock=clock)
