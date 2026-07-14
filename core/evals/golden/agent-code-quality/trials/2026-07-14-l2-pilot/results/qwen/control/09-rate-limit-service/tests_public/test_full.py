"""Comprehensive tests for rate-limit service spec."""

import os
import tempfile
import unittest

from service.config import load_limits
from service.store import HitStore
from service.limiter import RateLimiter


class TestConfig(unittest.TestCase):
    def test_none_returns_defaults(self):
        result = load_limits(None)
        self.assertEqual(result["max_requests"], 5)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_missing_file_fails_closed(self):
        result = load_limits("/nonexistent/path")
        self.assertEqual(result["max_requests"], 0)
        self.assertEqual(result["window_seconds"], 60.0)

    def test_valid_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write("max_requests=10\n")
            f.write("window_seconds=30.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 10)
            self.assertEqual(result["window_seconds"], 30.0)
        finally:
            os.unlink(path)

    def test_valid_config_reversed_order(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write("window_seconds=45.0\n")
            f.write("max_requests=20\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 20)
            self.assertEqual(result["window_seconds"], 45.0)
        finally:
            os.unlink(path)

    def test_config_with_comments_and_blanks(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write("# comment\n")
            f.write("\n")
            f.write("max_requests=3\n")
            f.write("# another comment\n")
            f.write("window_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 3)
            self.assertEqual(result["window_seconds"], 10.0)
        finally:
            os.unlink(path)

    def test_invalid_config_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write("max_requests=notanumber\n")
            f.write("window_seconds=10.0\n")
            path = f.name
        try:
            result = load_limits(path)
            self.assertEqual(result["max_requests"], 0)
        finally:
            os.unlink(path)

    def test_empty_file_fails_closed(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write("")
            path = f.name
        try:
            result = load_limits(path)
            # Empty file: max_requests stays at default 5, window at 60.0
            # This is valid (no parse error), just no overrides
            self.assertEqual(result["max_requests"], 5)
            self.assertEqual(result["window_seconds"], 60.0)
        finally:
            os.unlink(path)


class TestHitStore(unittest.TestCase):
    def test_record_and_count(self):
        store = HitStore()
        store.record("a", 100.0)
        store.record("a", 110.0)
        # now=120, window=30 => cutoff=90, interval (90, 120]
        # Both 100 and 110 are in range
        count = store.hits_in_window("a", 120.0, 30.0)
        self.assertEqual(count, 2)

    def test_record_and_count_one_expires(self):
        store = HitStore()
        store.record("a", 85.0)   # outside (90, 120]
        store.record("a", 110.0)  # inside (90, 120]
        count = store.hits_in_window("a", 120.0, 30.0)
        self.assertEqual(count, 1)

    def test_key_isolation(self):
        store = HitStore()
        store.record("a", 100.0)
        store.record("b", 105.0)
        self.assertEqual(store.hits_in_window("a", 110.0, 30.0), 1)
        self.assertEqual(store.hits_in_window("b", 110.0, 30.0), 1)

    def test_half_open_window(self):
        store = HitStore()
        # ts=90 is exactly at cutoff (now-window_seconds), should be excluded
        store.record("a", 90.0)
        store.record("a", 90.01)
        now = 120.0
        window = 30.0
        count = store.hits_in_window("a", now, window)
        self.assertEqual(count, 1)  # only 90.01 is in (90, 120]

    def test_empty_key(self):
        store = HitStore()
        self.assertEqual(store.hits_in_window("nokey", 100.0, 30.0), 0)


class TestRateLimiter(unittest.TestCase):
    def test_basic_allow_deny(self):
        t = 1000.0
        rl = RateLimiter(2, 60.0, clock=lambda: t)
        self.assertTrue(rl.allow("user"))
        self.assertTrue(rl.allow("user"))
        self.assertFalse(rl.allow("user"))

    def test_zero_max_requests_always_deny(self):
        rl = RateLimiter(0, 60.0, clock=lambda: 1000.0)
        self.assertFalse(rl.allow("user"))
        # Should not record any hits
        self.assertEqual(rl.store.hits_in_window("user", 1000.0, 60.0), 0)

    def test_sliding_window_expiry(self):
        times = [1000.0]
        def clock():
            return times[0]
        rl = RateLimiter(2, 30.0, clock=clock)
        self.assertTrue(rl.allow("user"))  # t=1000
        self.assertTrue(rl.allow("user"))  # t=1000
        self.assertFalse(rl.allow("user"))  # t=1000, at limit
        # Advance time past window
        times[0] = 1031.0
        self.assertTrue(rl.allow("user"))  # old hits expired

    def test_key_isolation(self):
        rl = RateLimiter(2, 60.0, clock=lambda: 1000.0)
        self.assertTrue(rl.allow("a"))
        self.assertTrue(rl.allow("a"))
        self.assertFalse(rl.allow("a"))
        # "b" should still be allowed
        self.assertTrue(rl.allow("b"))

    def test_from_config_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1000.0)
        self.assertEqual(rl.max_requests, 5)
        self.assertEqual(rl.window_seconds, 60.0)

    def test_from_config_missing_file_fails_closed(self):
        rl = RateLimiter.from_config("/nonexistent", clock=lambda: 1000.0)
        self.assertEqual(rl.max_requests, 0)
        self.assertFalse(rl.allow("user"))

    def test_no_extra_request_beyond_max(self):
        """Ensure exactly max_requests are allowed, not max+1."""
        rl = RateLimiter(3, 60.0, clock=lambda: 1000.0)
        for i in range(3):
            self.assertTrue(rl.allow("user"), f"Request {i+1} should be allowed")
        self.assertFalse(rl.allow("user"), "4th request should be denied")


if __name__ == "__main__":
    unittest.main()
