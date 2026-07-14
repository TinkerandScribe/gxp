# GXP brief — 08-line-chunker

## Goal
Stateful byte LineChunker with multi-byte delimiter and max_line.

## Ideal State Criteria
- [ ] max_line < 1 and empty newline raise ValueError with field name
- [ ] feed buffers; returns complete lines without delimiter
- [ ] partial multi-byte delimiter kept in buffer
- [ ] max_line enforced on incomplete buffer and on line content length
- [ ] close flushes remainder; second close returns []
- [ ] feed after close raises ValueError containing closed

## Out of scope
Text encodings, async IO.

## Verification
Mental walk-through of \r\n partials and max_line; scorer later.
