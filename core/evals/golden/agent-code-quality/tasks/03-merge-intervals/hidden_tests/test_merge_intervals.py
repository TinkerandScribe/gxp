"""Hidden tests for 03-merge-intervals."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_fn():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "merge_intervals.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.merge_intervals


class TestMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fn = load_fn()

    def m(self, xs):
        return type(self)._fn(xs)

    def test_empty(self):
        self.assertEqual(self.m([]), [])

    def test_single(self):
        self.assertEqual(self.m([[1, 3]]), [[1, 3]])

    def test_overlap(self):
        self.assertEqual(self.m([[1, 3], [2, 6], [8, 10]]), [[1, 6], [8, 10]])

    def test_touching(self):
        self.assertEqual(self.m([[1, 2], [2, 3]]), [[1, 3]])

    def test_unsorted(self):
        self.assertEqual(self.m([[5, 6], [1, 3], [2, 4]]), [[1, 4], [5, 6]])

    def test_contained(self):
        self.assertEqual(self.m([[1, 10], [2, 3], [4, 5]]), [[1, 10]])

    def test_no_mutate(self):
        src = [[2, 3], [1, 2]]
        copy = [x[:] for x in src]
        self.m(src)
        self.assertEqual(src, copy)

    def test_disjoint(self):
        self.assertEqual(self.m([[1, 2], [4, 5]]), [[1, 2], [4, 5]])
