"""Comprehensive tests for rate-limit service correctness."""

import os
import tempfile
import unittest

from service.config import load_limits
from service.store import HitStore
from service.limiter import RateLimiter


class TestConfigFailClosed(unittest.TestCase):
    """Criterion 1: fail-closed on missing/invalid config."""

    def test_none_returns_defaults(self):
        result = load_limits(None)
        self.assertEqual(result["max_requests"], 5)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_missing_file_fails_closed(self):
        result = load_limits("/nonexistent/path/config.ini")
        self.assertEqual(result["max_requests"], 0)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_invalid_content_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("garbage\nnot_valid\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)

    def test_empty_file_uses_defaults(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 5)
            self.assertEqual(result["window_seconds"], 60.0)
        finally:
            os.unlink(path)

    def test_valid_config_parsed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=10\nwindow_seconds=30.5\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 10)
            self.assertAlmostEqual(result["window_seconds"], 30.5)
        finally:
            os.unlink(path)

    def test_comments_and_blanks_allowed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("# comment\n\nmax_requests=7\n\nwindow_seconds=15.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 7)
            self.assertAlmostEqual(result["window_seconds"], 15.0)
        finally:
            os.unlink(path)

    def test_reversed_order(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("window_seconds=20.0\nmax_requests=3\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 3)
            self.assertAlmostEqual(result["window_seconds"], 20.0)
        finally:
            os.unlink(path)


class TestHitStoreIsolation(unittest.TestCase):
    """Criterion 2: per-key isolation."""

    def test_keys_are_isolated(self):
        store = HitStore()
        store.record("a", 100.0)
        store.record("a", 101.0)
        store.record("b", 100.5)
        self.assertEqual(store.hits_in_window("a", 102.0, 60.0), 2)
        self.assertEqual(store.hits_in_window("b", 102.0, 60.0), 1)

    def test_unknown_key_returns_zero(self):
        store = HitStore()
        self.assertEqual(store.hits_in_window("never_seen", 100.0, 60.0), 0)


class TestHitStoreWindow(unittest.TestCase):
    """Criterion 3: sliding window (now-W, now]."""

    def test_exact_boundary_exclusive_left(self):
        store = HitStore()
        # ts=100.0 is exactly at cutoff when now=200.0, W=100.0 → excluded
        store.record("k", 100.0)
        self.assertEqual(store.hits_in_window("k", 200.0, 100.0), 0)

    def test_exact_boundary_inclusive_right(self):
        store = HitStore()
        # ts=200.0 is exactly at now → included
        store.record("k", 200.0)
        self.assertEqual(store.hits_in_window("k", 200.0, 100.0), 1)

    def test_just_inside_window(self):
        store = HitStore()
        store.record("k", 100.01)  # just after cutoff of 100.0
        self.assertEqual(store.hits_in_window("k", 200.0, 100.0), 1)

    def test_old_hits_excluded(self):
        store = HitStore()
        store.record("k", 50.0)
        store.record("k", 90.0)
        store.record("k", 150.0)
        self.assertEqual(store.hits_in_window("k", 200.0, 60.0), 1)  # only 150.0


class TestRateLimiterAllow(unittest.TestCase):
    """Criteria 4, 5, 6: check-then-record, zero deny, exact limit."""

    def test_exact_limit(self):
        t = [0.0]
        def clock():
            t[0] += 1.0
            return t[0]
        rl = RateLimiter(3, 60.0, clock=clock)
        self.assertTrue(rl.allow("u"))
        self.assertTrue(rl.allow("u"))
        self.assertTrue(rl.allow("u"))
        self.assertFalse(rl.allow("u"))
        self.assertFalse(rl.allow("u"))

    def test_zero_max_always_denies(self):
        rl = RateLimiter(0, 60.0, clock=lambda: 100.0)
        self.assertFalse(rl.allow("any"))
        self.assertFalse(rl.allow("any"))

    def test_different_keys_independent(self):
        t = [0.0]
        def clock():
            t[0] += 1.0
            return t[0]
        rl = RateLimiter(2, 60.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        # key "b" should still work
        self.assertTrue(rl.allow("b"))

    def test_window_expiry_allows_again(self):
        t = [0.0]
        def clock():
            t[0] += 1.0
            return t[0]
        rl = RateLimiter(2, 5.0, clock=clock)
        self.assertTrue(rl.allow("u"))  # t=1
        self.assertTrue(rl.allow("u"))  # t=2
        self.assertFalse(rl.allow("u"))  # t=3, full
        # advance past window
        t[0] = 8.0
        self.assertTrue(rl.allow("u"))  # old hits expired

    def test_from_config_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 5)
        self.assertAlmostEqual(rl.window_seconds, 60.0)

    def test_from_config_missing_file_fails_closed(self):
        rl = RateLimiter.from_config("/no/such/file", clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 0)
        self.assertFalse(rl.allow("any"))


if __name__ == "__main__":
    unittest.main()
