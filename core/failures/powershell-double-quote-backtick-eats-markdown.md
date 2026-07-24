# Failure capture

**Date:** 2026-07-23
**Task / context:** Implementing `gxp-refine` docs/templates on Windows PowerShell;
writing markdown that contained backticks (code fences, `` `gxp-refine` ``,
inline paths) via PowerShell string literals / expandable here-strings.

## Expected

File contents on disk match the intended markdown byte-for-byte, including
backticks used for inline code and fenced blocks.

## Actual

PowerShell treated backtick as its escape character inside double-quoted
strings and `@"..."@` expandable here-strings. Sequences such as `` `a ``
became BEL (0x07), `` `r `` / `` `n `` were consumed as carriage-return /
newline escapes, and other `` `X `` pairs vanished or mutated. The written
markdown was corrupted before any git commit review could catch it easily.

## Root cause

PowerShell's string escape is `` ` `` (backtick), not `\`. Double-quoted
content and expandable here-strings interpret escapes; markdown authors
routinely need literal backticks. Using the wrong quoting layer for content
that *is* markdown guarantees silent corruption.

## Detection

- Diff shows missing backticks, odd control characters, or broken fence
  markers in newly written `.md` files.
- `git diff` / hex view reveals `0x07` (BEL) where `` `a `` was intended.
- Symptom clusters on Windows hosts after agent "wrote files via PowerShell".

## Resolution

Rewrote affected files with a path that does not interpret backticks:
single-quoted here-string (`@'...'@ | Set-Content`) feeding a small Python
`Path.write_text`, or Git Bash / an editor Write tool. Re-verified markers
with `bash scripts/eval-gxp-refine-selftest.sh`.

## Prevention

On Windows PowerShell hosts:

- Prefer **single-quoted** here-strings (`@'...'@`) plus Python `write_text`,
  or bash/`Write` tooling, for any content that contains backticks.
- **Never** use PowerShell double-quoted strings or `@"..."@` expandable
  here-strings to emit markdown/code that needs literal `` ` ``.
- Keep post-write marker greps (as in `eval-gxp-refine-selftest.sh`) so
  missing fence/trigger text fails closed.

## Follow-up

- [x] Document this failure under `core/failures/` (this file).
- [ ] Optional: agent operator notes / AGENTS.md one-liner if Windows agents
      keep hitting the same trap (parked — process note already in session
      instructions).

## Repeatable?

Yes — any Windows PowerShell agent writing markdown with backticks through
double-quoted strings will hit this again.
