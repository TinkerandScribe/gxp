"""Comprehensive tests for rate-limit service — verifies all spec criteria."""

import os
import tempfile
import unittest

from service.config import load_limits
from service.store import HitStore
from service.limiter import RateLimiter


class TestLoadLimits(unittest.TestCase):
    """Criteria 1-3: config loading and fail-closed behavior."""

    def test_none_returns_defaults(self):
        result = load_limits(None)
        self.assertEqual(result["max_requests"], 5)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_missing_file_fails_closed(self):
        result = load_limits("/nonexistent/path/config.ini")
        self.assertEqual(result["max_requests"], 0)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_invalid_content_fails_closed(self):
        # Content with unparseable values triggers exception → fail closed
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=not_a_number\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
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

    def test_valid_config_with_comments_and_blanks(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("# comment\n\nmax_requests=3\n\nwindow_seconds=15.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 3)
            self.assertAlmostEqual(result["window_seconds"], 15.0)
        finally:
            os.unlink(path)

    def test_reversed_order_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("window_seconds=25.0\nmax_requests=7\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 7)
            self.assertAlmostEqual(result["window_seconds"], 25.0)
        finally:
            os.unlink(path)

    def test_non_integer_max_requests_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=abc\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)

    def test_unrecognized_lines_ignored(self):
        # Lines without '=' are skipped, defaults remain for unset keys
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("garbage\nnot_valid\nmax_requests=42\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 42)
            # window_seconds stays at default since not specified
            self.assertAlmostEqual(result["window_seconds"], 60.0)
        finally:
            os.unlink(path)


class TestHitStore(unittest.TestCase):
    """Criteria 4-5: per-key isolation and sliding window."""

    def test_key_isolation(self):
        store = HitStore()
        store.record("a", 100.0)
        store.record("a", 101.0)
        self.assertEqual(store.hits_in_window("a", 102.0, 60.0), 2)
        self.assertEqual(store.hits_in_window("b", 102.0, 60.0), 0)

    def test_sliding_window_exclusive_left(self):
        store = HitStore()
        # Exactly at cutoff (now - window) should be EXCLUDED
        store.record("k", 100.0)
        now = 160.0
        window = 60.0
        self.assertEqual(store.hits_in_window("k", now, window), 0)

    def test_sliding_window_inclusive_right(self):
        store = HitStore()
        # Exactly at 'now' should be INCLUDED
        store.record("k", 160.0)
        now = 160.0
        window = 60.0
        self.assertEqual(store.hits_in_window("k", now, window), 1)

    def test_sliding_window_inside(self):
        store = HitStore()
        store.record("k", 159.0)
        store.record("k", 140.0)
        store.record("k", 139.9)
        now = 160.0
        window = 60.0
        # 159.0 > 100 and <= 160 → in
        # 140.0 > 100 and <= 160 → in
        # 139.9 > 100 and <= 160 → in
        self.assertEqual(store.hits_in_window("k", now, window), 3)

    def test_old_hits_excluded(self):
        store = HitStore()
        store.record("k", 50.0)   # too old
        store.record("k", 159.0)  # in window
        now = 160.0
        window = 60.0
        self.assertEqual(store.hits_in_window("k", now, window), 1)

    def test_empty_key_returns_zero(self):
        store = HitStore()
        self.assertEqual(store.hits_in_window("never_seen", 100.0, 60.0), 0)


class TestRateLimiter(unittest.TestCase):
    """Criteria 6-8: check-then-record, max_requests=0 denial, exact count."""

    def test_max_requests_exact_count(self):
        counter = [0.0]
        def clock():
            val = counter[0]
            counter[0] += 0.1
            return val
        rl = RateLimiter(3, 60.0, clock=clock)
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertFalse(rl.allow("user"))  # 4th denied

    def test_zero_max_requests_always_denies(self):
        rl = RateLimiter(0, 60.0, clock=lambda: 100.0)
        self.assertFalse(rl.allow("any_key"))
        self.assertFalse(rl.allow("any_key"))

    def test_zero_max_does_not_record(self):
        store = HitStore()
        rl = RateLimiter(0, 60.0, clock=lambda: 100.0, store=store)
        rl.allow("key")
        self.assertEqual(store.hits_in_window("key", 100.0, 60.0), 0)

    def test_key_isolation_in_limiter(self):
        counter = [0.0]
        def clock():
            val = counter[0]
            counter[0] += 0.1
            return val
        rl = RateLimiter(2, 60.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        # "b" should still be allowed
        self.assertTrue(rl.allow("b"))

    def test_window_expiry_allows_again(self):
        times = [100.0, 101.0, 200.0]
        idx = [0]
        def clock():
            val = times[idx[0]]
            idx[0] += 1
            return val
        rl = RateLimiter(2, 60.0, clock=clock)
        self.assertTrue(rl.allow("user"))  # t=100
        self.assertTrue(rl.allow("user"))  # t=101
        # At t=200, both old hits are outside window (200-60=140), so allow again
        self.assertTrue(rl.allow("user"))  # t=200, window expired, allowed

    def test_from_config_with_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 5)
        self.assertAlmostEqual(rl.window_seconds, 60.0)

    def test_from_config_missing_file_denies_all(self):
        rl = RateLimiter.from_config("/no/such/file", clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 0)
        self.assertFalse(rl.allow("any"))


if __name__ == "__main__":
    unittest.main()
