### Brief

**Goal**: Implement a stateful byte-based line splitter (`LineChunker`) that buffers input, splits on a configurable multi-byte delimiter, enforces a maximum line length, and handles closure/idempotency correctly.

**Binary Criteria**:
1.  **Validation**: `__init__` raises `ValueError` if `max_line < 1` or `newline` is empty/invalid.
2.  **Buffering**: `feed()` appends to an internal buffer; lines are only emitted when a full delimiter is found.
3.  **Delimiter Handling**: The delimiter bytes are consumed and *not* included in the returned line content. Multi-byte delimiters must be handled correctly (no partial match false positives).
4.  **Max Line Enforcement**: `ValueError` is raised if any complete line (content only) exceeds `max_line`, or if the buffer grows beyond `max_line` without finding a delimiter.
5.  **Close Behavior**: `close()` returns remaining buffer content as a final line (if non-empty and within limits), clears state, and marks closed. Subsequent calls return `[]`.
6.  **Closed State**: Calling `feed()` after `close()` raises `ValueError` with "closed" in the message.
7.  **Empty Input**: `feed(b'')` returns `[]` unless it triggers a close-like behavior (which it doesn't, only `close()` does).
8.  **Bytes Only**: All operations are on `bytes`, no decoding to text.

**Out of Scope**: Text encoding handling, complex regex splitting, non-stdlib dependencies.

**Verification**: I will implement the logic using a simple buffer accumulation and search for the delimiter. I will carefully check the length constraints *before* emitting lines or raising errors. I will ensure the "closed" state is tracked via a flag.

### Implementation

```python
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
```