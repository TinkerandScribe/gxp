"""State"""
from __future__ import annotations
class BreakerState:
    def __init__(self):
        self.mode = "closed"
        self.failures = 0
        self.successes = 0
        self.opened_at = None
