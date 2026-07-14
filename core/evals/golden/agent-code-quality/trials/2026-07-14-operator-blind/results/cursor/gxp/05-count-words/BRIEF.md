# Task Brief — count_words

**Goal:** Implement `count_words(text: str) -> dict[str, int]` that counts whitespace-delimited tokens after edge punctuation strip and case-folding.

**Strategy/Model:** Cursor agent (full GXP workflow). Single-file stdlib implementation; no external deps.

## Ideal State Criteria

1. `count_words("")` returns `{}`.
2. `count_words("   ...  ") ` returns `{}` (whitespace-only or all-punctuation input).
3. `count_words("Hello hello HELLO")` returns `{"hello": 3}` (case-folded keys).
4. `count_words("well-known.")` returns `{"well-known": 1}` (mid-word hyphen preserved; trailing punct stripped).
5. `count_words("...word...")` returns `{"word": 1}` (repeated edge punctuation stripped).
6. `count_words("a! b? c.")` returns `{"a": 1, "b": 1, "c": 1}` (per-token edge strip).
7. Implementation uses only stdlib (`string.punctuation`, `str.split()`, `str.casefold()`).
8. Return type is `dict[str, int]` with integer counts ≥ 1 for every key.

## Out of scope

- Mid-word punctuation handling beyond spec (e.g. splitting `don't` into two words).
- Unicode punctuation outside `string.punctuation`.
- Helper scripts, tests files, or ratings in DEST.
- Running official hidden tests or opening reference solutions.

## Verification plan

1. Run inline Python checks for criteria 1–6 with representative inputs.
2. Confirm `import string` and edge-strip loop only touch `string.punctuation` characters at token ends.
3. Inspect return types and key folding on mixed-case samples.
