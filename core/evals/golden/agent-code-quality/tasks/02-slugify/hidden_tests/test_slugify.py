"""Hidden tests for 02-slugify."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_fn():
    p = os.environ.get("IMPL_PATH") or os.environ.get("PARSE_KV_PATH")
    if p:
        path = Path(p)
    else:
        path = Path(__file__).resolve().parent / "slugify.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.slugify


class TestSlugify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fn = load_fn()

    def s(self, t):
        return type(self)._fn(t)

    def test_basic(self):
        self.assertEqual(self.s("Hello World"), "hello-world")

    def test_punctuation(self):
        self.assertEqual(self.s("Hello, World!"), "hello-world")

    def test_collapse(self):
        self.assertEqual(self.s("a---b"), "a-b")

    def test_trim(self):
        self.assertEqual(self.s("  --Hi--  "), "hi")

    def test_empty(self):
        self.assertEqual(self.s("***"), "")

    def test_numbers(self):
        self.assertEqual(self.s("Item 42"), "item-42")

    def test_unicode_dropped(self):
        self.assertEqual(self.s("café"), "caf")

    def test_mixed(self):
        self.assertEqual(self.s("Foo_Bar/Baz"), "foo-bar-baz")
