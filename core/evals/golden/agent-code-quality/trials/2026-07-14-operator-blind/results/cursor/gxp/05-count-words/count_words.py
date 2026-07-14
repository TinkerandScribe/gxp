"""Count words in text with case-folding and edge punctuation stripping."""

import string


def _strip_edge_punctuation(token: str) -> str:
    punct = string.punctuation
    while token and token[0] in punct:
        token = token[1:]
    while token and token[-1] in punct:
        token = token[:-1]
    return token


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for token in text.split():
        word = _strip_edge_punctuation(token.casefold())
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts
