"""Comprehensive tests for rate-limit service correctness."""

import os
import tempfile
import unittest

from service.config import load_limits
from service.store import HitStore
from service.limiter import RateLimiter


class TestLoadLimits(unittest.TestCase):
    def test_none_returns_defaults(self):
        result = load_limits(None)
        self.assertEqual(result["max_requests"], 5)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_missing_file_fails_closed(self):
        result = load_limits("/nonexistent/path/config.ini")
        self.assertEqual(result["max_requests"], 0)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_invalid_content_fails_closed(self):
        """File with unparseable values (e.g., non-integer max_requests) fails closed."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=abc\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)

    def test_valid_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=10\nwindow_seconds=30.5\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 10)
            self.assertAlmostEqual(result["window_seconds"], 30.5)
        finally:
            os.unlink(path)

    def test_valid_config_reversed_order(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("window_seconds=45.0\nmax_requests=20\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 20)
            self.assertAlmostEqual(result["window_seconds"], 45.0)
        finally:
            os.unlink(path)

    def test_comments_and_blanks_allowed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("# comment\n\nmax_requests=7\n\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 7)
            self.assertAlmostEqual(result["window_seconds"], 10.0)
        finally:
            os.unlink(path)

    def test_non_float_window_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("max_requests=5\nwindow_seconds=not_a_number\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)


class TestHitStore(unittest.TestCase):
    def test_record_and_count(self):
        store = HitStore()
        store.record("a", 1.0)
        store.record("a", 2.0)
        count = store.hits_in_window("a", 2.5, 5.0)
        self.assertEqual(count, 2)

    def test_key_isolation(self):
        store = HitStore()
        store.record("a", 1.0)
        store.record("b", 2.0)
        self.assertEqual(store.hits_in_window("a", 3.0, 5.0), 1)
        self.assertEqual(store.hits_in_window("b", 3.0, 5.0), 1)

    def test_window_excludes_old(self):
        store = HitStore()
        store.record("a", 1.0)   # old, outside window
        store.record("a", 9.0)   # inside window
        count = store.hits_in_window("a", 10.0, 5.0)
        self.assertEqual(count, 1)

    def test_left_exclusive_boundary(self):
        """Hit exactly at cutoff (now - W) should NOT be counted."""
        store = HitStore()
        store.record("a", 5.0)   # exactly at boundary: now=10, W=5 => cutoff=5
        count = store.hits_in_window("a", 10.0, 5.0)
        self.assertEqual(count, 0)  # left-exclusive

    def test_right_inclusive_boundary(self):
        """Hit exactly at now should be counted."""
        store = HitStore()
        store.record("a", 10.0)
        count = store.hits_in_window("a", 10.0, 5.0)
        self.assertEqual(count, 1)  # right-inclusive

    def test_empty_key_returns_zero(self):
        store = HitStore()
        self.assertEqual(store.hits_in_window("never_seen", 10.0, 5.0), 0)


class TestRateLimiter(unittest.TestCase):
    def test_exact_limit_enforcement(self):
        """Exactly max_requests calls return True, next returns False."""
        clock_val = [1000.0]
        def clock():
            val = clock_val[0]
            clock_val[0] += 1.0
            return val
        rl = RateLimiter(3, 60.0, clock=clock)
        for i in range(3):
            self.assertTrue(rl.allow("user"), f"call {i+1} should be allowed")
        self.assertFalse(rl.allow("user"), "4th call should be denied")

    def test_zero_max_always_denies(self):
        rl = RateLimiter(0, 60.0, clock=lambda: 1000.0)
        self.assertFalse(rl.allow("any_key"))
        self.assertFalse(rl.allow("another_key"))

    def test_sliding_window_expiry(self):
        """After window expires, requests are allowed again."""
        clock_val = [1000.0]
        def clock():
            return clock_val[0]
        rl = RateLimiter(2, 10.0, clock=clock)
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertFalse(rl.allow("user"))  # at limit
        # Advance time past window
        clock_val[0] = 1011.0
        self.assertTrue(rl.allow("user"))  # old hits expired

    def test_key_isolation_in_limiter(self):
        rl = RateLimiter(2, 60.0, clock=lambda: 1000.0)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))  # "a" at limit
        self.assertTrue(rl.allow("b"))   # "b" still allowed

    def test_from_config_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 5)
        self.assertAlmostEqual(rl.window_seconds, 60.0)

    def test_from_config_missing_file_fails_closed(self):
        rl = RateLimiter.from_config("/nonexistent", clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 0)
        self.assertFalse(rl.allow("any"))

    def test_deny_does_not_record(self):
        """When denied, no hit should be recorded."""
        clock_val = [1000.0]
        def clock():
            return clock_val[0]
        rl = RateLimiter(1, 60.0, clock=clock)
        self.assertTrue(rl.allow("user"))   # allowed, recorded
        self.assertFalse(rl.allow("user"))  # denied, NOT recorded
        # Advance past window
        clock_val[0] = 1061.0
        self.assertTrue(rl.allow("user"))   # should be allowed again


if __name__ == "__main__":
    unittest.main()
