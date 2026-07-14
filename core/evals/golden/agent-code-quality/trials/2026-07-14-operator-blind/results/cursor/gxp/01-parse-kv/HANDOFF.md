# Handoff — parse_kv (Cursor / gxp / 01-parse-kv)

## What changed

- Replaced starter `parse_kv.py` with a correct `parse_kv` implementation:
  - Ignores blank (whitespace-only) lines and comment lines (first non-whitespace `#`)
  - Requires `KEY=VALUE` with trimmed key matching `[A-Za-z0-9_]+`
  - Preserves value text after first `=`; unwraps only a whole-value matching `"..."` with no interior `"`
  - Duplicate keys: last wins
  - Collects invalid lines and raises `ValueError` whose message includes `invalid` and the count
- Added `BRIEF.md` (goal, 6 ISC, out of scope, verification plan)

## Verified

Inline deterministic checks (temp script outside DEST; not committed):

- Happy path + `dict` type
- Blanks / comments ignored; `#a=1` ignored; `k=#notcomment` kept
- Key trim + charset; value spaces; quote unwrap / nested left as-is; empty value
- Last-wins duplicates
- Invalid lines → `ValueError` with `invalid` + count (`3` and `1` cases)
- Stdlib only (`re`)

## Not done / out of scope

- Official hidden tests / `score_trial.py` (forbidden by arm)
- `ratings.jsonl` / helper scripts in DEST (forbidden by arm)
- No approval gates hit; no phase-4 dead ends
