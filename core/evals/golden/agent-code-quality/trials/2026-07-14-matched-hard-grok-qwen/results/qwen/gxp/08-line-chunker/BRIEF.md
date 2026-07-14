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
