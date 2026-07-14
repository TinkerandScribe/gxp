# Task brief — count_words

**Strategy/Model:** Single small pure-function implementation, stdlib only.
Lowest-capable engine suffices (deterministic string logic); no external
tools/handoff needed. Full-ish workflow (brief + impl + own checks + handoff),
but scope forbids ratings.jsonl / helper scripts in DEST.

## Goal

Implement `count_words(text: str) -> dict[str, int]` in `count_words.py` that
tallies whitespace-split tokens, casefolded, with leading/trailing ASCII
punctuation stripped.

## Context

- Spec: `tasks/05-count-words/prompt.md`.
- Starter `count_words.py` is naive (no casefold, no punctuation strip).
- Only `count_words.py` (plus BRIEF/HANDOFF) may be written in DEST.

## Ideal State Criteria (binary)

1. `count_words("")` and whitespace-only input (`"   \t\n "`) return `{}`.
2. `count_words("Hello hello HELLO")` == `{"hello": 3}` (casefold merges cases).
3. Edge ASCII punctuation stripped: `count_words("hello, world!")`
   == `{"hello": 1, "world": 1}`.
4. Mid-word hyphen preserved and edges stripped repeatedly:
   `count_words("well-known well-known")` == `{"well-known": 2}` and
   `count_words("--well-known--")` == `{"well-known": 1}`.
5. All-punctuation input returns `{}`:
   `count_words("!!! ??? ...")` == `{}`.
6. Splits on any unicode whitespace via bare `str.split()` — tab/newline/NBSP
   separated tokens each counted (e.g. `"a\tb\nc"` -> three keys).
7. Stdlib only: the module imports nothing beyond `string`; no third-party deps.
8. Signature is exactly `count_words(text: str) -> dict[str, int]`.

## Out of scope

- Preserving insertion/iteration order (explicitly not graded).
- Stripping non-ASCII / unicode punctuation (only `string.punctuation`).
- Any stemming, tokenization beyond `str.split()`, or CLI.
- Rating log, helper scripts, or tests written into DEST.

## Verification plan

- Deterministic: run each ISC above as inline asserts in a scratchpad script
  (outside DEST) against the implementation; all must pass.
- Confirm `import` line references only `string` (ISC 7) by reading the file.
- Confirm signature line matches ISC 8 by reading the file.
