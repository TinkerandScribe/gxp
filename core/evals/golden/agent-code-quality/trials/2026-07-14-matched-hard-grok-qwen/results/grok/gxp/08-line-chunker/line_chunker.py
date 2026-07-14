"""LineChunker — GXP implement (criteria-first)."""

from __future__ import annotations


class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        if not isinstance(max_line, int) or isinstance(max_line, bool) or max_line < 1:
            raise ValueError("max_line invalid")
        if not isinstance(newline, (bytes, bytearray)) or len(newline) < 1:
            raise ValueError("newline invalid")
        self.max_line = max_line
        self.newline = bytes(newline)
        self._buf = bytearray()
        self._closed = False

    def feed(self, data: bytes) -> list[bytes]:
        if self._closed:
            raise ValueError("closed")
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        self._buf.extend(data)
        out: list[bytes] = []
        nl = self.newline
        nlen = len(nl)
        while True:
            pos = self._buf.find(nl)
            if pos < 0:
                if len(self._buf) > self.max_line:
                    raise ValueError("max_line exceeded")
                break
            if pos > self.max_line:
                raise ValueError("max_line exceeded")
            out.append(bytes(self._buf[:pos]))
            del self._buf[: pos + nlen]
        return out

    def close(self) -> list[bytes]:
        if self._closed:
            return []
        self._closed = True
        if not self._buf:
            return []
        if len(self._buf) > self.max_line:
            raise ValueError("max_line exceeded")
        line = bytes(self._buf)
        self._buf.clear()
        return [line]
