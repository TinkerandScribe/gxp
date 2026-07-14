"""Starter — decode-as-text splitlines; fails bytes/max/close contract."""

from __future__ import annotations


class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        self.max_line = max_line
        self.newline = newline
        self._parts: list[bytes] = []

    def feed(self, data: bytes) -> list[bytes]:
        # BUG: treats each feed independently; text splitlines; no buffer
        try:
            text = data.decode("utf-8", errors="replace")
        except Exception:
            text = ""
        lines = text.splitlines()
        # drop empties incorrectly sometimes
        return [ln.encode() for ln in lines if ln]

    def close(self) -> list[bytes]:
        return []
