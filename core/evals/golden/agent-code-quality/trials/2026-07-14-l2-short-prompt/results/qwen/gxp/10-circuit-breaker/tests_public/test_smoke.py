"""Weak public smoke — green on buggy starter."""

import unittest

from service.breaker import CircuitBreaker


class TestSmoke(unittest.TestCase):
    def test_starts_closed_allows(self):
        b = CircuitBreaker(3, 2, 30.0, clock=lambda: 0.0)
        self.assertTrue(b.allow_request())
        self.assertEqual(b.mode(), "closed")

    def test_from_config_none(self):
        b = CircuitBreaker.from_config(None, clock=lambda: 1.0)
        self.assertTrue(b.allow_request())


if __name__ == "__main__":
    unittest.main()
