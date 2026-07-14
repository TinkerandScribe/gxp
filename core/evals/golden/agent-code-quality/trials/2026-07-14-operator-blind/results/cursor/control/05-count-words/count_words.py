"""Count words with casefold and edge punctuation stripping."""

import string


def count_words(text: str) -> dict[str, int]:
    punct = set(string.punctuation)
    counts: dict[str, int] = {}

    for token in text.split():
        while token and token[0] in punct:
            token = token[1:]
        while token and token[-1] in punct:
            token = token[:-1]
        if not token:
            continue
        word = token.casefold()
        counts[word] = counts.get(word, 0) + 1

    return counts
