"""Count words with case-folding and ASCII punctuation stripping."""

import string


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in text.split():
        word = token.strip(string.punctuation)
        if not word:
            continue
        word = word.casefold()
        counts[word] = counts.get(word, 0) + 1
    return counts
