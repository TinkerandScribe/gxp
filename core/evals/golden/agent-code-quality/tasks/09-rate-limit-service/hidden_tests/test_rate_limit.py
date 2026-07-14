"""Hidden multi-factor tests for 09-rate-limit-service."""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path


def _root() -> Path:
    return Path(os.environ.get("RESULT_ROOT") or os.environ.get("IMPL_PATH") or ".")


def _import_service():
    root = _root().resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    # Fresh imports per class setup
    for name in list(sys.modules):
        if name == "service" or name.startswith("service."):
            del sys.modules[name]
    import service.config as config
    import service.store as store
    import service.limiter as limiter

    return config, store, limiter


class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = float(t)

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


class TestRateLimitService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.store_mod, cls.limiter_mod = _import_service()

    def test_stdlib_only_service_imports(self):
        root = _root()
        banned = []
        for path in (root / "service").rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("import ") or s.startswith("from "):
                    if "service" in s:
                        continue
                    # allow stdlib modules only
                    mod = s.split()[1].split(".")[0]
                    if mod in {
                        "time",
                        "pathlib",
                        "os",
                        "sys",
                        "json",
                        "re",
                        "collections",
                        "typing",
                        "dataclasses",
                        "functools",
                        "itertools",
                        "copy",
                        "math",
                        "io",
                        "tempfile",
                        "__future__",
                    }:
                        continue
                    if s.startswith("from __future__"):
                        continue
                    banned.append((path.name, s))
        self.assertEqual(banned, [], f"non-stdlib imports: {banned}")

    def test_allow_up_to_max_then_deny(self):
        clock = FakeClock(100.0)
        rl = self.limiter_mod.RateLimiter(3, 10.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))

    def test_sliding_window_expires(self):
        clock = FakeClock(0.0)
        rl = self.limiter_mod.RateLimiter(2, 5.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        clock.advance(5.1)
        self.assertTrue(rl.allow("a"))

    def test_keys_isolated(self):
        clock = FakeClock(0.0)
        rl = self.limiter_mod.RateLimiter(1, 60.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        self.assertTrue(rl.allow("b"))

    def test_max_zero_always_deny(self):
        rl = self.limiter_mod.RateLimiter(0, 60.0, clock=FakeClock())
        self.assertFalse(rl.allow("a"))

    def test_missing_config_fail_closed(self):
        lim = self.config.load_limits(str(Path("no_such_config_12345.conf")))
        self.assertEqual(lim["max_requests"], 0)
        rl = self.limiter_mod.RateLimiter.from_config(
            str(Path("no_such_config_12345.conf")), clock=FakeClock(1.0)
        )
        self.assertFalse(rl.allow("z"))

    def test_invalid_config_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.conf"
            p.write_text("not valid config\n", encoding="utf-8")
            lim = self.config.load_limits(str(p))
            self.assertEqual(lim["max_requests"], 0)

    def test_valid_config_and_from_config(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ok.conf"
            p.write_text("# c\nmax_requests=2\nwindow_seconds=30\n", encoding="utf-8")
            lim = self.config.load_limits(str(p))
            self.assertEqual(lim["max_requests"], 2)
            self.assertEqual(lim["window_seconds"], 30.0)
            clock = FakeClock(10.0)
            rl = self.limiter_mod.RateLimiter.from_config(str(p), clock=clock)
            self.assertTrue(rl.allow("k"))
            self.assertTrue(rl.allow("k"))
            self.assertFalse(rl.allow("k"))

    def test_default_config_none(self):
        lim = self.config.load_limits(None)
        self.assertEqual(lim["max_requests"], 5)
        self.assertEqual(lim["window_seconds"], 60.0)

    def test_hits_in_window_half_open_left(self):
        store = self.store_mod.HitStore()
        store.record("a", 1.0)
        store.record("a", 5.0)
        store.record("a", 10.0)
        # window 5 at now=10 → (5, 10] → times 5.0? start=5 exclusive so 5.0 not counted if t > start
        # Spec: (now - W, now] → start exclusive: t > start and t <= now
        n = store.hits_in_window("a", 10.0, 5.0)
        self.assertEqual(n, 1)  # only 10.0; 5.0 is not > 5.0

    def test_deny_does_not_consume_slot(self):
        clock = FakeClock(0.0)
        rl = self.limiter_mod.RateLimiter(1, 100.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        self.assertFalse(rl.allow("a"))  # still false; no extra growth quirks
        clock.advance(101.0)
        self.assertTrue(rl.allow("a"))

    def test_window_boundary_inclusive_now(self):
        clock = FakeClock(10.0)
        rl = self.limiter_mod.RateLimiter(1, 10.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        # at same timestamp second call should deny
        self.assertFalse(rl.allow("a"))
