"""Hidden tests for 06-lru-ttl."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_cls():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "lru_ttl.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.LruTtlCache


class FakeClock:
    def __init__(self, t=0.0):
        self.t = float(t)

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


class TestLruTtl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.C = load_cls()

    def test_capacity_rejects_zero(self):
        with self.assertRaises(ValueError) as ctx:
            self.C(0)
        self.assertIn("capacity", str(ctx.exception).lower())

    def test_capacity_rejects_negative(self):
        with self.assertRaises(ValueError):
            self.C(-1)

    def test_basic_get_set(self):
        c = self.C(2, clock=FakeClock())
        c.set("a", 1)
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(len(c), 1)

    def test_lru_eviction_order(self):
        clock = FakeClock()
        c = self.C(2, clock=clock)
        c.set("a", 1)
        c.set("b", 2)
        c.get("a")  # a becomes MRU; b is LRU
        c.set("c", 3)  # evict b
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("c"), 3)
        with self.assertRaises(KeyError):
            c.get("b")

    def test_ttl_expire_on_get_removes(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=10.0, clock=clock)
        c.set("a", 1)
        clock.advance(11.0)
        with self.assertRaises(KeyError):
            c.get("a")
        # capacity free after expiry removal
        c.set("b", 2)
        c.set("c", 3)
        self.assertEqual(len(c), 2)
        self.assertEqual(c.get("b"), 2)

    def test_get_does_not_refresh_ttl(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=10.0, clock=clock)
        c.set("a", 1)
        clock.advance(8.0)
        self.assertEqual(c.get("a"), 1)  # must not extend TTL
        clock.advance(3.0)  # total 11 from set
        with self.assertRaises(KeyError):
            c.get("a")

    def test_set_refreshes_ttl_and_recency(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=10.0, clock=clock)
        c.set("a", 1)
        c.set("b", 2)
        clock.advance(8.0)
        c.set("a", 9)  # refresh TTL + MRU
        clock.advance(5.0)  # 13 from first set; 5 from refresh
        self.assertEqual(c.get("a"), 9)
        # b expired at t=10, now t=13
        with self.assertRaises(KeyError):
            c.get("b")

    def test_contains_no_recency_change(self):
        clock = FakeClock()
        c = self.C(2, clock=clock)
        c.set("a", 1)
        c.set("b", 2)
        self.assertTrue("a" in c)  # must not promote a
        c.set("c", 3)  # should evict a (still LRU), not b
        with self.assertRaises(KeyError):
            c.get("a")
        self.assertEqual(c.get("b"), 2)
        self.assertEqual(c.get("c"), 3)

    def test_contains_expired_false_and_reaps(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=5.0, clock=clock)
        c.set("a", 1)
        clock.advance(6.0)
        self.assertFalse("a" in c)
        self.assertEqual(len(c), 0)

    def test_len_reaps_expired(self):
        clock = FakeClock(0.0)
        c = self.C(3, ttl=5.0, clock=clock)
        c.set("a", 1)
        c.set("b", 2)
        clock.advance(6.0)
        self.assertEqual(len(c), 0)

    def test_delete_expired_still_true(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=5.0, clock=clock)
        c.set("a", 1)
        clock.advance(6.0)
        self.assertTrue(c.delete("a"))
        self.assertFalse(c.delete("a"))

    def test_reap_before_evict_when_expired_fill_capacity(self):
        clock = FakeClock(0.0)
        c = self.C(2, ttl=5.0, clock=clock)
        c.set("a", 1)
        c.set("b", 2)
        clock.advance(6.0)
        # both expired; new set should not need to keep them
        c.set("c", 3)
        self.assertEqual(len(c), 1)
        self.assertEqual(c.get("c"), 3)
