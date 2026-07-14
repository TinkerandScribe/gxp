"""LineChunker — control implement from prompt."""

from __future__ import annotations


class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        if not isinstance(max_line, int) or isinstance(max_line, bool) or max_line < 1:
            raise ValueError("max_line must be >= 1")
        if not isinstance(newline, (bytes, bytearray)) or len(newline) < 1:
            raise ValueError("newline must be non-empty bytes")
        self.max_line = max_line
        self.newline = bytes(newline)
        self._buf = bytearray()
        self._closed = False

    def _check(self, n: int) -> None:
        if n > self.max_line:
            raise ValueError("max_line exceeded")

    def feed(self, data: bytes) -> list[bytes]:
        if self._closed:
            raise ValueError("chunker is closed")
        self._buf.extend(data)
        lines: list[bytes] = []
        nl = self.newline
        while True:
            idx = self._buf.find(nl)
            if idx < 0:
                self._check(len(self._buf))
                break
            self._check(idx)
            lines.append(bytes(self._buf[:idx]))
            del self._buf[: idx + len(nl)]
        return lines

    def close(self) -> list[bytes]:
        if self._closed:
            return []
        self._closed = True
        if not self._buf:
            return []
        self._check(len(self._buf))
        out = [bytes(self._buf)]
        self._buf.clear()
        return out
