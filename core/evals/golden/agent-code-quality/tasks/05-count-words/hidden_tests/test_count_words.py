"""Hidden tests for 05-count-words."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_fn():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "count_words.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.count_words


class TestCountWords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fn = load_fn()

    def cw(self, t):
        return type(self)._fn(t)

    def test_basic(self):
        self.assertEqual(self.cw("a b a"), {"a": 2, "b": 1})

    def test_casefold(self):
        d = self.cw("Hello hello HELLO")
        self.assertEqual(d.get("hello"), 3)

    def test_punctuation_edges(self):
        d = self.cw("Hello, world!")
        self.assertEqual(d.get("hello"), 1)
        self.assertEqual(d.get("world"), 1)

    def test_internal_hyphen_kept(self):
        d = self.cw("well-known")
        self.assertEqual(d.get("well-known"), 1)

    def test_empty(self):
        self.assertEqual(self.cw(""), {})
        self.assertEqual(self.cw("   "), {})

    def test_only_punct(self):
        self.assertEqual(self.cw("... !!!"), {})

    def test_mixed(self):
        d = self.cw("Foo foo FOO bar.")
        self.assertEqual(d.get("foo"), 3)
        self.assertEqual(d.get("bar"), 1)
