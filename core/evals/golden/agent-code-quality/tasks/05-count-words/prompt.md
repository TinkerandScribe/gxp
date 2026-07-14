# Task: count_words

## Deliverable

Implement `count_words(text: str) -> dict[str, int]` in `count_words.py`.

## Spec

- Split on **whitespace** (any unicode whitespace via `str.split()` with no args).
- Words are case-**folded** with `str.casefold()` for counting keys.
- Strip leading/trailing ASCII punctuation from each token using characters in
  `string.punctuation` only (not mid-word hyphens: `well-known` stays one token
  after edge strip — if both edges are punctuation, strip repeatedly from ends).
- Empty tokens after stripping are dropped.
- Return a dict mapping word → count. Iteration order is not graded.
- Empty input or all-punctuation/whitespace → `{}`.
- Stdlib only.

## Constraints

Starter tree only; no hidden-test edits.

## Done means

Hidden tests pass.
