from __future__ import annotations
import time
from service.config import load_breaker_config
from service.state import BreakerState
class CircuitBreaker:
    def __init__(self, failure_threshold, success_threshold, open_seconds, *, clock=None):
        self.failure_threshold=int(failure_threshold); self.success_threshold=int(success_threshold)
        self.open_seconds=float(open_seconds); self.clock=clock if clock is not None else time.monotonic
        self.state=BreakerState()
    def mode(self): return self.state.mode
    def allow_request(self):
        st=self.state
        if st.mode=="closed": return True
        if st.mode=="open":
            if st.opened_at is not None and self.clock()-st.opened_at>=self.open_seconds:
                st.mode="half_open"; st.successes=0; return True
            return False
        return True
    def record_success(self):
        st=self.state
        if st.mode=="closed": st.failures=0
        elif st.mode=="half_open":
            st.mode="closed"; st.failures=0; st.successes=0; st.opened_at=None
    def record_failure(self):
        st=self.state
        if st.mode=="closed":
            st.failures+=1
            if st.failures>=self.failure_threshold:
                st.mode="open"; st.opened_at=self.clock()
        elif st.mode=="half_open":
            st.mode="open"; st.opened_at=self.clock(); st.successes=0
    @classmethod
    def from_config(cls, path=None, *, clock=None):
        cfg=load_breaker_config(path)
        return cls(cfg["failure_threshold"], cfg["success_threshold"], cfg["open_seconds"], clock=clock)
