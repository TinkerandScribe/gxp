# Handoff — 01-parse-kv (GXP arm)

## What changed
- Rewrote `parse_kv.py` `parse_kv(text)` to meet the spec. Fixes the three seeded
  starter bugs: (1) invalid lines are now counted and raised instead of skipped,
  (2) keys are validated against `[A-Za-z0-9_]+`, (3) values are no longer
  over-stripped — interior spaces are preserved and only one wrapping double-quote
  pair is removed.

## Design decisions
- Value = raw substring after the first `=`. Surrounding non-quote whitespace is
  **preserved** (spec defines value as "rest of the line after the first `=`" and
  says only to strip interior-space handling / a wrapping quote pair). Only a
  single matching `"..."` pair (len ≥ 2) is stripped; unmatched/nested quotes stay.
- Comment test uses first non-whitespace char (`line.lstrip()[:1] == "#"`), so
  `KEY=#x` is a valid pair with value `#x`, not a comment.
- Invalid lines are counted (not stored) since only the count is needed for the
  `ValueError` message: `parse_kv: found N invalid line(s)` — contains `invalid`
  and the integer count.
- Last-key-wins falls out of plain dict assignment.

## What I verified
Ran a scratch script (in the session scratchpad, not in DEST) with assertions for
every Ideal State Criterion:
- golden pairs; blanks/comments ignored; `#`-value kept; `dict` return type;
- value variants: interior spaces, `"a b"`→`a b`, `""`→``, unmatched `"a`/`a"`
  left as-is, nested `"a"b"`→`a"b`, lone `"` left as-is;
- duplicate last-wins; key trimming + charset;
- `ValueError` on no-`=`, empty key, space-in-key, dash-in-key; count = 2 with a
  mix of invalid + valid lines; message contains `invalid` + count; zero-invalid
  never raises.

Result: **ALL PASS**.

## Not done / notes
- No official hidden tests were run (not provided to this arm); confidence rests on
  the scratch checks above.
- Dict ordering is first-seen insertion order (spec: not graded).
- Per GXP-arm scope rules, no `ratings.jsonl` or helper scripts were written into
  DEST.
