"""Weak public smoke tests."""

import unittest

from service.limiter import RateLimiter


class TestSmoke(unittest.TestCase):
    def test_first_allow(self):
        rl = RateLimiter(5, 60.0, clock=lambda: 1000.0)
        self.assertTrue(rl.allow("user"))

    def test_from_config_none(self):
        rl = RateLimiter.from_config(None, clock=lambda: 1.0)
        self.assertTrue(rl.allow("x"))


if __name__ == "__main__":
    unittest.main()
