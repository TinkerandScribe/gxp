"""Hidden tests for 08-line-chunker."""

import importlib.util
import os
import unittest
from pathlib import Path


def load_cls():
    p = os.environ.get("IMPL_PATH")
    path = Path(p) if p else Path(__file__).resolve().parent / "line_chunker.py"
    spec = importlib.util.spec_from_file_location("under_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.LineChunker


class TestLineChunker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.C = load_cls()

    def test_rejects_bad_max_line(self):
        with self.assertRaises(ValueError) as ctx:
            self.C(max_line=0)
        self.assertIn("max_line", str(ctx.exception).lower())

    def test_rejects_empty_newline(self):
        with self.assertRaises(ValueError) as ctx:
            self.C(newline=b"")
        self.assertIn("newline", str(ctx.exception).lower())

    def test_basic_single_feed(self):
        c = self.C()
        self.assertEqual(c.feed(b"a\nb\n"), [b"a", b"b"])
        self.assertEqual(c.close(), [])

    def test_split_across_feeds(self):
        c = self.C()
        self.assertEqual(c.feed(b"hel"), [])
        self.assertEqual(c.feed(b"lo\nwor"), [b"hello"])
        self.assertEqual(c.feed(b"ld\n"), [b"world"])
        self.assertEqual(c.close(), [])

    def test_close_flushes_remainder(self):
        c = self.C()
        self.assertEqual(c.feed(b"no-newline-yet"), [])
        self.assertEqual(c.close(), [b"no-newline-yet"])
        self.assertEqual(c.close(), [])

    def test_empty_lines(self):
        c = self.C()
        self.assertEqual(c.feed(b"\n\n"), [b"", b""])

    def test_crlf_multibyte(self):
        c = self.C(newline=b"\r\n")
        self.assertEqual(c.feed(b"a\r\nb\r\n"), [b"a", b"b"])

    def test_partial_multibyte_delimiter(self):
        c = self.C(newline=b"\r\n")
        self.assertEqual(c.feed(b"ab\r"), [])
        self.assertEqual(c.feed(b"\ncd\r\n"), [b"ab", b"cd"])

    def test_max_line_on_buffer_without_delim(self):
        c = self.C(max_line=3)
        with self.assertRaises(ValueError) as ctx:
            c.feed(b"abcd")
        self.assertIn("max_line", str(ctx.exception).lower())

    def test_max_line_exact_ok(self):
        c = self.C(max_line=3)
        self.assertEqual(c.feed(b"abc\n"), [b"abc"])

    def test_max_line_content_too_long_with_delim(self):
        c = self.C(max_line=3)
        with self.assertRaises(ValueError):
            c.feed(b"abcd\n")

    def test_feed_after_close(self):
        c = self.C()
        c.close()
        with self.assertRaises(ValueError) as ctx:
            c.feed(b"x\n")
        self.assertIn("closed", str(ctx.exception).lower())

    def test_binary_safe(self):
        c = self.C(newline=b"\x00")
        self.assertEqual(c.feed(b"a\x00b\x00"), [b"a", b"b"])

    def test_empty_feed(self):
        c = self.C()
        self.assertEqual(c.feed(b""), [])
