"""LineChunker: Stateful byte line splitter."""

from __future__ import annotations


class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"):
        if not isinstance(max_line, int) or max_line < 1:
            raise ValueError("max_line must be an integer >= 1")
        if not isinstance(newline, bytes) or len(newline) == 0:
            raise ValueError("newline must be a non-empty bytes delimiter")
        
        self.max_line = max_line
        self.newline = newline
        self._buffer = b""
        self._closed = False

    def feed(self, data: bytes) -> list[bytes]:
        if self._closed:
            raise ValueError("LineChunker is closed")
        
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")

        # Append new data to buffer
        self._buffer += data
        
        lines = []
        nl_len = len(self.newline)
        
        while True:
            # Find the first occurrence of the newline delimiter
            idx = self._buffer.find(self.newline)
            
            if idx == -1:
                # No complete line found in the current buffer
                break
            
            # Extract the line content (before the delimiter)
            line_content = self._buffer[:idx]
            
            # Check max_line constraint for the complete line
            if len(line_content) > self.max_line:
                raise ValueError(f"Line length {len(line_content)} exceeds max_line {self.max_line}")
            
            lines.append(line_content)
            
            # Remove the processed part (line + delimiter) from buffer
            self._buffer = self._buffer[idx + nl_len:]
            
        return lines

    def close(self) -> list[bytes]:
        if self._closed:
            return []
        
        self._closed = True
        
        if not self._buffer:
            return []
        
        # Check max_line constraint for the final fragment
        if len(self._buffer) > self.max_line:
            raise ValueError(f"Final line length {len(self._buffer)} exceeds max_line {self.max_line}")
            
        result = [self._buffer]
        self._buffer = b""
        return result
