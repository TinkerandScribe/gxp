"""Word counting with casefold and punctuation stripping."""

import string


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in text.split():
        word = token.casefold().strip(string.punctuation)
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts
