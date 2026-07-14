# Task: LineChunker (stateful byte line splitter)

## Deliverable

Implement class `LineChunker` in `line_chunker.py`.

## Spec

```python
class LineChunker:
    def __init__(self, max_line: int = 1024, newline: bytes = b"\n"): ...
    def feed(self, data: bytes) -> list[bytes]: ...
    def close(self) -> list[bytes]: ...
```

### Construction

- `max_line` must be an integer **≥ 1**; else `ValueError` message contains
  `max_line`.
- `newline` must be a non-empty `bytes` delimiter (length ≥ 1). Else
  `ValueError` message contains `newline`.
- Delimiter may be multi-byte (e.g. `b"\r\n"`). Matching is exact byte sequence.

### `feed(data: bytes) -> list[bytes]`

- Append `data` to an internal buffer (must accept any `bytes`, including empty).
- Extract and return **every complete line** found, in order.
- A complete line is the bytes **before** a delimiter occurrence; the delimiter
  itself is **consumed and not included** in the returned line.
- After extracting, the buffer holds only the incomplete trailing fragment
  (possibly empty).
- If at any point the buffer length **without a delimiter** would exceed
  `max_line`, raise `ValueError` whose message contains `max_line`. Check this
  whenever the buffer grows and still has no complete line, and also if a
  single complete line's content length (excluding delimiter) is `> max_line`.
- Empty `data` is allowed and may still return lines only if somehow complete
  (normally returns `[]`).
- After `close()` has been called, further `feed` must raise `ValueError`
  (message contains `closed`).

### `close() -> list[bytes]`

- Mark the chunker closed.
- If the buffer is non-empty, return it as a **single final line** (no delimiter
  required), then clear the buffer — **unless** that fragment length `> max_line`,
  then raise `ValueError` (`max_line` in message).
- If buffer empty, return `[]`.
- Idempotent: second `close()` returns `[]` and stays closed.

### Other

- Work in **bytes** only (not text encodings).
- Stdlib only.
- Edit only the starter tree; no hidden-test edits.

## Done means

Hidden tests pass. Multi-byte delimiter partial matches are the hard part —
verify carefully.
