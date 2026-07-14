"""Hidden tests for 04-safe-join."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


def load_fn():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "safe_join.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.safe_join


class TestSafeJoin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._fn = load_fn()

    def sj(self, root, *parts):
        return type(self)._fn(root, *parts)

    def test_basic(self):
        with tempfile.TemporaryDirectory() as d:
            out = self.sj(d, "a", "b.txt")
            self.assertTrue(out.startswith(os.path.abspath(d)))
            self.assertTrue(out.endswith(os.path.join("a", "b.txt")) or out.endswith("a\\b.txt") or "a" in out)

    def test_empty_parts(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.sj(d), os.path.abspath(d))

    def test_dotdot_escape(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError) as ctx:
                self.sj(d, "..", "etc", "passwd")
            self.assertIn("escape", str(ctx.exception).lower())

    def test_nested_ok(self):
        with tempfile.TemporaryDirectory() as d:
            out = self.sj(d, "x", "..", "y")
            # x/../y stays under d
            self.assertTrue(
                out == os.path.abspath(os.path.join(d, "y"))
                or out.startswith(os.path.abspath(d) + os.sep)
            )

    def test_absolute_part_escape(self):
        with tempfile.TemporaryDirectory() as d:
            # absolute second part should not leave root unchecked
            abs_other = os.path.abspath(os.sep + "tmp")
            try:
                out = self.sj(d, abs_other)
            except ValueError as e:
                self.assertIn("escape", str(e).lower())
                return
            # If implementation joins oddly, must still be under root
            root = os.path.abspath(d)
            self.assertTrue(out == root or out.startswith(root + os.sep))
