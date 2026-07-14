Goal: Implement `count_words` to count word frequencies with specific normalization rules.
Criteria:
- Split input on whitespace using `str.split()`.
- Case-fold tokens using `str.casefold()`.
- Strip leading/trailing ASCII punctuation (`string.punctuation`) from each token.
- Drop empty tokens after stripping.
- Return a dictionary mapping normalized words to counts.
Out of Scope:
- Handling non-ASCII punctuation (only `string.punctuation` applies).
- Preserving original case or punctuation in keys.
Verify:
- Hidden tests pass against the specification.
