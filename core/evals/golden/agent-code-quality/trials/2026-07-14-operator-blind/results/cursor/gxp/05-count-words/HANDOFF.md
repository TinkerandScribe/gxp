# Handoff — count_words (Trial 12)

## What changed

- Replaced naive starter `count_words.py` with full implementation:
  - Split on whitespace via `str.split()`.
  - Case-fold each token with `str.casefold()` before counting.
  - Strip leading/trailing ASCII punctuation (`string.punctuation`) repeatedly from token ends.
  - Drop empty tokens after stripping.
  - Accumulate counts in `dict[str, int]`.

## Verified

Deterministic inline Python checks (not official hidden tests):

| Input | Expected | Result |
|-------|----------|--------|
| `""` | `{}` | pass |
| `"   ...  "` | `{}` | pass |
| `"Hello hello HELLO"` | `{"hello": 3}` | pass |
| `"well-known."` | `{"well-known": 1}` | pass |
| `"...word..."` | `{"word": 1}` | pass |
| `"a! b? c."` | `{"a": 1, "b": 1, "c": 1}` | pass |
| `"can't"` | `{"can't": 1}` | pass |
| `"can't stop"` | `{"can't": 1, "stop": 1}` | pass |

## Not done

- Official hidden test suite not run (per trial protocol).
- No `ratings.jsonl` entry in DEST (GXP trial scope).

## Files

- `BRIEF.md` — task brief with 8 binary criteria
- `count_words.py` — implementation
- `HANDOFF.md` — this file
