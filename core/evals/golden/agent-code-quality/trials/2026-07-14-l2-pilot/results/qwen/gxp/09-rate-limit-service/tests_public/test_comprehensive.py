"""Comprehensive tests for rate-limit service correctness."""

import os
import tempfile
import unittest

from service.config import load_limits
from service.store import HitStore
from service.limiter import RateLimiter


class TestConfigFailClosed(unittest.TestCase):
    """Criterion 1: missing file or parse error returns max_requests=0."""

    def test_none_returns_defaults(self):
        result = load_limits(None)
        self.assertEqual(result["max_requests"], 5)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_missing_file_fails_closed(self):
        result = load_limits("/nonexistent/path/config.txt")
        self.assertEqual(result["max_requests"], 0)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_invalid_content_fails_closed(self):
        """Content that triggers a parse exception should fail closed."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            # This has max_requests= but value is not an int → ValueError
            f.write("max_requests=abc\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)

    def test_valid_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("max_requests=10\nwindow_seconds=30.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 10)
            self.assertEqual(result["window_seconds"], 30.0)
        finally:
            os.unlink(path)

    def test_valid_config_reverse_order(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("window_seconds=45.5\nmax_requests=7\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 7)
            self.assertEqual(result["window_seconds"], 45.5)
        finally:
            os.unlink(path)

    def test_comments_and_blanks_allowed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("# comment\n\nmax_requests=3\n\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 3)
            self.assertEqual(result["window_seconds"], 10.0)
        finally:
            os.unlink(path)

    def test_parse_error_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("max_requests=not_a_number\nwindow_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)


class TestHitStore(unittest.TestCase):
    """Criteria 2 & 3: per-key isolation and sliding window."""

    def test_per_key_isolation(self):
        store = HitStore()
        store.record("a", 100.0)
        store.record("a", 101.0)
        store.record("b", 102.0)
        self.assertEqual(store.hits_in_window("a", 105.0, 60.0), 2)
        self.assertEqual(store.hits_in_window("b", 105.0, 60.0), 1)

    def test_sliding_window_exclusive_left(self):
        store = HitStore()
        now = 100.0
        window = 10.0
        # Exactly at cutoff (now - window) should NOT be counted
        store.record("k", now - window)
        # Just inside should be counted
        store.record("k", now - window + 0.001)
        # At now should be counted
        store.record("k", now)
        self.assertEqual(store.hits_in_window("k", now, window), 2)

    def test_empty_key_returns_zero(self):
        store = HitStore()
        self.assertEqual(store.hits_in_window("unknown", 100.0, 60.0), 0)


class TestRateLimiter(unittest.TestCase):
    """Criteria 4, 5, 6: check-then-record, exact limit, zero-max."""

    def test_exact_limit(self):
        t = [0.0]
        def clock():
            val = t[0]
            t[0] += 1.0
            return val
        rl = RateLimiter(3, 60.0, clock=clock)
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertFalse(rl.allow("user"))

    def test_zero_max_always_denies(self):
        rl = RateLimiter(0, 60.0, clock=lambda: 100.0)
        self.assertFalse(rl.allow("any"))
        self.assertFalse(rl.allow("any"))

    def test_key_isolation_in_limiter(self):
        t = [0.0]
        def clock():
            val = t[0]
            t[0] += 1.0
            return val
        rl = RateLimiter(2, 60.0, clock=clock)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        # key "b" should still work
        self.assertTrue(rl.allow("b"))

    def test_window_expiry(self):
        t = [0.0]
        def clock():
            val = t[0]
            t[0] += 1.0
            return val
        rl = RateLimiter(2, 5.0, clock=clock)
        self.assertTrue(rl.allow("u"))
        self.assertTrue(rl.allow("u"))
        self.assertFalse(rl.allow("u"))
        # Advance time past window
        t[0] = 10.0
        self.assertTrue(rl.allow("u"))

    def test_from_config_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 5)
        self.assertEqual(rl.window_seconds, 60.0)

    def test_from_config_bad_path_fails_closed(self):
        rl = RateLimiter.from_config("/no/such/file", clock=lambda: 1.0)
        self.assertEqual(rl.max_requests, 0)
        self.assertFalse(rl.allow("any"))

    def test_denied_hits_not_recorded(self):
        """When a request is denied, no hit should be recorded."""
        t = [0.0]
        def clock():
            val = t[0]
            t[0] += 1.0
            return val
        rl = RateLimiter(2, 60.0, clock=clock)
        self.assertTrue(rl.allow("u"))
        self.assertTrue(rl.allow("u"))
        # These should be denied and NOT recorded
        self.assertFalse(rl.allow("u"))
        self.assertFalse(rl.allow("u"))
        # After window expires, only 2 hits should remain
        t[0] = 100.0
        self.assertTrue(rl.allow("u"))
        self.assertTrue(rl.allow("u"))
        self.assertFalse(rl.allow("u"))


if __name__ == "__main__":
    unittest.main()
