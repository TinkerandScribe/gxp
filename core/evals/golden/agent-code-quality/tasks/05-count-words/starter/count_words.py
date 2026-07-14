"""Starter — naive split, no casefold/punct."""


def count_words(text: str) -> dict:
    # BUG: no casefold; no punctuation strip
    counts = {}
    for w in text.split():
        counts[w] = counts.get(w, 0) + 1
    return counts
