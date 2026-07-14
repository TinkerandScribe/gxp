# Handoff — count_words

## What changed

- `count_words.py`: replaced the naive starter with a stdlib-only
  implementation.
  - `text.split()` (bare) — splits on any unicode whitespace.
  - `token.strip(string.punctuation)` — strips leading/trailing ASCII
    punctuation repeatedly from both ends; mid-word punctuation (hyphen,
    apostrophe) preserved.
  - Empty-after-strip tokens dropped.
  - `stripped.casefold()` used as the counting key.
  - Signature is `count_words(text: str) -> dict[str, int]`; only `string`
    imported.

## What I verified

Ran an inline assert script from the scratchpad (outside DEST) importing the
DEST module. All 8 Ideal State Criteria pass on Python 3.14.3:

- Empty and whitespace-only -> `{}`.
- Casefold merges `Hello/hello/HELLO` -> `{"hello": 3}`.
- Edge punctuation stripped: `hello, world!` -> `{"hello":1,"world":1}`.
- Mid-word hyphen kept; edges stripped repeatedly: `well-known well-known`
  -> `{"well-known":2}`, `--well-known--` -> `{"well-known":1}`.
- All-punctuation `!!! ??? ...` -> `{}`.
- Tab/newline/NBSP split into separate tokens.
- Extra sanity: `'don't'` -> `{"don't":1}`, `Cats cats, cat.` ->
  `{"cats":2,"cat":1}`, `Straße STRASSE` -> `{"strasse":2}`.

## What is not done / out of scope

- Iteration order is not preserved by design (spec says order is not graded).
- Only ASCII `string.punctuation` is stripped; unicode punctuation is left
  intact per spec.
- No rating-log entry, helper scripts, or tests written into DEST (scope rule).

## Notes / risk

- casefold is applied after strip; since `string.punctuation` is ASCII and
  casefold never produces ASCII punctuation, strip-then-casefold and
  casefold-then-strip are equivalent here.
