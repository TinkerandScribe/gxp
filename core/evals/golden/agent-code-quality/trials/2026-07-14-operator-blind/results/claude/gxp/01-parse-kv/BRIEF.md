# Task brief — robust KEY=VALUE parser

## Goal
Implement `parse_kv(text: str) -> dict[str, str]` in `parse_kv.py` so it meets the
spec in `tasks/01-parse-kv/prompt.md`: parse effective `KEY=VALUE` lines, ignore
blanks/comments, validate keys, strip one wrapping quote pair, last-key-wins, and
raise `ValueError` (message containing "invalid" + a count) when invalid lines exist.

## Strategy / Model
Small, self-contained pure-stdlib string task. Lowest-capable engine (current model,
no tools beyond editor + a scratch Python check) clears the criteria with margin.
Full workflow, but no external deps, no new files beyond impl + the two `.md`.

## Context
- Starter `parse_kv.py` skips invalid lines, doesn't validate key charset, and
  over-strips values — all three are wrong per spec.
- Only editable root: this DEST dir. No network, stdlib only.

## Ideal State Criteria (binary)
1. `parse_kv("A=1\nB=2")` returns `{"A": "1", "B": "2"}`.
2. Blank lines and lines whose first non-whitespace char is `#` are ignored
   (contribute no keys and no errors); `KEY=#x` keeps value `#x`.
3. Key validation: only `[A-Za-z0-9_]+` (after trimming surrounding whitespace)
   is accepted; a line with no `=`, an empty key, or a key with any other char
   is collected as an error.
4. When ≥1 invalid line exists, `parse_kv` raises `ValueError` whose message
   contains the substring `invalid` **and** the integer count of invalid lines;
   with zero invalid lines it never raises.
5. Value handling: value is the entire substring after the first `=`; interior
   spaces are preserved (`K=a b` → `a b`); exactly one wrapping pair of matching
   double quotes is removed (`K="a b"` → `a b`, `K=""` → ``), while an unmatched
   or single leading/trailing quote is left as-is (`K="a` → `"a`).
6. Duplicate keys: last occurrence wins (`A=1\nA=2` → `{"A": "2"}`).
7. Return value is a plain `dict`.

## Out of scope
- Preserving/guaranteeing a specific dict ordering (spec: not graded).
- Stripping surrounding (non-quote) whitespace from values — spec defines value as
  the raw rest-of-line after the first `=`; only quotes are stripped.
- Any file other than `parse_kv.py`, `BRIEF.md`, `HANDOFF.md`.

## Verification plan
- Deterministic: run a scratch Python snippet (outside DEST) exercising each
  criterion above — golden pairs, comments/blanks, `#`-value, invalid-line count in
  the `ValueError` message, quote stripping variants, duplicate last-wins, `dict`
  type. Confirm all assertions pass.
- No official hidden tests available; accept that gap explicitly.
