"""LineChunker: stateful byte line splitter."""

from __future__ import annotations


class LineChunker:
    """A stateful byte-based line splitter that respects max_line limits and multi-byte delimiters."""

    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        # Validate max_line
        if not isinstance(max_line, int) or isinstance(max_line, bool):
            raise ValueError("max_line must be an integer >= 1")
        if max_line < 1:
            raise ValueError("max_line must be an integer >= 1")

        # Validate newline
        if not isinstance(newline, bytes):
            raise ValueError("newline must be a non-empty bytes delimiter")
        if len(newline) < 1:
            raise ValueError("newline must be a non-empty bytes delimiter")

        self.max_line = max_line
        self.newline = newline
        self._buffer = b""
        self._closed = False

    def feed(self, data: bytes) -> list[bytes]:
        """Append data to internal buffer and return all complete lines found."""
        if self._closed:
            raise ValueError("LineChunker is closed")

        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")

        # Append new data to buffer
        self._buffer += data

        result = []
        nl = self.newline
        nl_len = len(nl)

        while True:
            # Find the next occurrence of the delimiter in the buffer
            idx = self._buffer.find(nl)

            if idx == -1:
                # No complete line found. Check if the current buffer (which is all incomplete)
                # exceeds max_line. Since there's no delimiter, the entire buffer is a potential
                # line fragment. If it exceeds max_line, raise error.
                if len(self._buffer) > self.max_line:
                    raise ValueError(
                        f"Line length {len(self._buffer)} exceeds max_line {self.max_line}"
                    )
                break

            # Found a delimiter at idx
            line_content = self._buffer[:idx]

            # Check if the line content (excluding delimiter) exceeds max_line
            if len(line_content) > self.max_line:
                raise ValueError(
                    f"Line length {len(line_content)} exceeds max_line {self.max_line}"
                )

            # Add the line to results
            result.append(line_content)

            # Remove the processed part (line + delimiter) from buffer
            self._buffer = self._buffer[idx + nl_len :]

        return result

    def close(self) -> list[bytes]:
        """Mark chunker closed and return any remaining buffer as final line."""
        if self._closed:
            return []

        self._closed = True
        result = []

        if self._buffer:
            # Check if the remaining fragment exceeds max_line
            if len(self._buffer) > self.max_line:
                raise ValueError(
                    f"Line length {len(self._buffer)} exceeds max_line {self.max_line}"
                )
            result.append(self._buffer)

        # Clear buffer
        self._buffer = b""

        return result
