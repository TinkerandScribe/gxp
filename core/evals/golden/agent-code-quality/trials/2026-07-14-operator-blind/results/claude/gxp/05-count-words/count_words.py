"""Count whitespace-split words, casefolded, with edge punctuation stripped."""

import string


def count_words(text: str) -> dict[str, int]:
    """Return a mapping of word -> count.

    Tokens are produced by ``str.split()`` (any unicode whitespace). Each token
    has leading/trailing ASCII punctuation (``string.punctuation``) stripped
    repeatedly from both ends; mid-word punctuation such as the hyphen in
    ``well-known`` is preserved. Counting keys are casefolded. Tokens that are
    empty after stripping are dropped, so empty or all-punctuation/whitespace
    input yields ``{}``.
    """
    counts: dict[str, int] = {}
    for token in text.split():
        stripped = token.strip(string.punctuation)
        if not stripped:
            continue
        key = stripped.casefold()
        counts[key] = counts.get(key, 0) + 1
    return counts
