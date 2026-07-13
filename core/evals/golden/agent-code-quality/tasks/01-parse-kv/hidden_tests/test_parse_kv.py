"""Hidden tests — used by score_trial.py; keep out of agent prompts."""

import importlib.util
import sys
import unittest
from pathlib import Path


def load_parse_kv(module_path: Path):
    spec = importlib.util.spec_from_file_location("parse_kv_under_test", module_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.parse_kv


# Injected by scorer via env PARSE_KV_PATH; default for direct unittest.
def _path() -> Path:
    import os

    p = os.environ.get("PARSE_KV_PATH") or os.environ.get("IMPL_PATH")
    if p:
        return Path(p)
    # Scorer copies parse_kv.py next to this file during grading.
    sibling = Path(__file__).resolve().parent / "parse_kv.py"
    if sibling.is_file():
        return sibling
    return Path(__file__).resolve().parent.parent / "parse_kv.py"


class TestParseKv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Store as plain function — do not assign to instance method name
        # (that would inject self as first arg).
        cls._fn = load_parse_kv(_path())

    def pk(self, text: str):
        return type(self)._fn(text)

    def test_basic(self):
        d = self.pk("A=1\nB=2\n")
        self.assertEqual(d["A"], "1")
        self.assertEqual(d["B"], "2")

    def test_ignore_blank_and_comment(self):
        d = self.pk("\n# c\nK=v\n  # x\n")
        self.assertEqual(d, {"K": "v"})

    def test_last_key_wins(self):
        d = self.pk("K=1\nK=2\n")
        self.assertEqual(d["K"], "2")

    def test_value_keeps_interior_spaces(self):
        d = self.pk("MSG=hello world\n")
        self.assertEqual(d["MSG"], "hello world")

    def test_quoted_value_strips_outer_quotes_only(self):
        d = self.pk('MSG="hello world"\n')
        self.assertEqual(d["MSG"], "hello world")

    def test_unmatched_quote_left_intact(self):
        d = self.pk('MSG="hello\n')
        self.assertEqual(d["MSG"], '"hello')

    def test_invalid_line_raises(self):
        with self.assertRaises(ValueError) as ctx:
            self.pk("noequals\nA=1\n")
        msg = str(ctx.exception).lower()
        self.assertIn("invalid", msg)

    def test_invalid_key_charset_raises(self):
        with self.assertRaises(ValueError):
            self.pk("bad-key=1\n")

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            self.pk("=value\n")

    def test_valid_underscore_keys(self):
        d = self.pk("A_B1=x\n")
        self.assertEqual(d["A_B1"], "x")


if __name__ == "__main__":
    unittest.main()
