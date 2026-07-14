"""Hidden tests for 10-circuit-breaker."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


def _root() -> Path:
    return Path(os.environ.get("RESULT_ROOT") or os.environ.get("IMPL_PATH") or ".")


def _import():
    root = _root().resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    for name in list(sys.modules):
        if name == "service" or name.startswith("service."):
            del sys.modules[name]
    import service.breaker as breaker
    import service.config as config

    return config, breaker


class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = float(t)

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


class TestCircuitBreaker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.breaker = _import()

    def test_opens_after_threshold_failures(self):
        c = FakeClock(0.0)
        b = self.breaker.CircuitBreaker(3, 2, 10.0, clock=c)
        for _ in range(3):
            self.assertTrue(b.allow_request())
            b.record_failure()
        self.assertEqual(b.mode(), "open")
        self.assertFalse(b.allow_request())

    def test_success_resets_failure_streak(self):
        c = FakeClock()
        b = self.breaker.CircuitBreaker(3, 2, 10.0, clock=c)
        b.record_failure()
        b.record_failure()
        b.record_success()
        b.record_failure()
        b.record_failure()
        self.assertEqual(b.mode(), "closed")
        b.record_failure()
        self.assertEqual(b.mode(), "open")

    def test_open_to_half_open_after_timer(self):
        c = FakeClock(0.0)
        b = self.breaker.CircuitBreaker(1, 2, 5.0, clock=c)
        self.assertTrue(b.allow_request())
        b.record_failure()
        self.assertEqual(b.mode(), "open")
        self.assertFalse(b.allow_request())
        c.advance(5.0)
        self.assertTrue(b.allow_request())
        self.assertEqual(b.mode(), "half_open")

    def test_half_open_needs_success_threshold(self):
        c = FakeClock(0.0)
        b = self.breaker.CircuitBreaker(1, 2, 1.0, clock=c)
        b.record_failure()
        c.advance(1.0)
        self.assertTrue(b.allow_request())
        b.record_success()
        self.assertEqual(b.mode(), "half_open")
        b.record_success()
        self.assertEqual(b.mode(), "closed")

    def test_half_open_failure_reopens(self):
        c = FakeClock(0.0)
        b = self.breaker.CircuitBreaker(1, 2, 1.0, clock=c)
        b.record_failure()
        c.advance(1.0)
        self.assertTrue(b.allow_request())
        b.record_failure()
        self.assertEqual(b.mode(), "open")
        self.assertFalse(b.allow_request())

    def test_missing_config_fail_closed(self):
        cfg = self.config.load_breaker_config("no_such_breaker_cfg.conf")
        self.assertEqual(cfg["failure_threshold"], 1)
        self.assertGreaterEqual(cfg["success_threshold"], 10**6)
        b = self.breaker.CircuitBreaker.from_config(
            "no_such_breaker_cfg.conf", clock=FakeClock(0.0)
        )
        self.assertTrue(b.allow_request())
        b.record_failure()
        self.assertEqual(b.mode(), "open")

    def test_invalid_config_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.conf"
            p.write_text("not=valid=config\n", encoding="utf-8")
            cfg = self.config.load_breaker_config(str(p))
            self.assertEqual(cfg["failure_threshold"], 1)

    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ok.conf"
            p.write_text(
                "failure_threshold=2\nsuccess_threshold=1\nopen_seconds=10\n",
                encoding="utf-8",
            )
            cfg = self.config.load_breaker_config(str(p))
            self.assertEqual(cfg["failure_threshold"], 2)
            self.assertEqual(cfg["success_threshold"], 1)
            self.assertEqual(cfg["open_seconds"], 10.0)

    def test_defaults_none(self):
        cfg = self.config.load_breaker_config(None)
        self.assertEqual(cfg["failure_threshold"], 3)
        self.assertEqual(cfg["success_threshold"], 2)

    def test_stdlib_only(self):
        root = _root()
        banned = []
        for path in (root / "service").rglob("*.py"):
            for line in path.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if not (s.startswith("import ") or s.startswith("from ")):
                    continue
                if "service" in s or s.startswith("from __future__"):
                    continue
                mod = s.split()[1].split(".")[0]
                if mod in {"time", "pathlib", "os", "sys", "collections", "typing"}:
                    continue
                banned.append((path.name, s))
        self.assertEqual(banned, [])

    def test_open_does_not_allow_before_timer(self):
        c = FakeClock(100.0)
        b = self.breaker.CircuitBreaker(1, 1, 10.0, clock=c)
        b.record_failure()
        c.advance(9.9)
        self.assertFalse(b.allow_request())
        self.assertEqual(b.mode(), "open")
