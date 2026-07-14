"""Reference LineChunker."""

from __future__ import annotations


class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        if not isinstance(max_line, int) or isinstance(max_line, bool) or max_line < 1:
            raise ValueError("max_line must be an integer >= 1")
        if not isinstance(newline, (bytes, bytearray)) or len(newline) < 1:
            raise ValueError("newline must be non-empty bytes")
        self.max_line = max_line
        self.newline = bytes(newline)
        self._buf = bytearray()
        self._closed = False

    def _check_max_content(self, n: int) -> None:
        if n > self.max_line:
            raise ValueError("max_line exceeded")

    def feed(self, data: bytes) -> list[bytes]:
        if self._closed:
            raise ValueError("chunker is closed")
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        self._buf.extend(data)
        lines: list[bytes] = []
        nl = self.newline
        nlen = len(nl)
        while True:
            idx = self._buf.find(nl)
            if idx < 0:
                self._check_max_content(len(self._buf))
                break
            self._check_max_content(idx)
            lines.append(bytes(self._buf[:idx]))
            del self._buf[: idx + nlen]
        return lines

    def close(self) -> list[bytes]:
        if self._closed:
            return []
        self._closed = True
        if not self._buf:
            return []
        self._check_max_content(len(self._buf))
        out = [bytes(self._buf)]
        self._buf.clear()
        return out
