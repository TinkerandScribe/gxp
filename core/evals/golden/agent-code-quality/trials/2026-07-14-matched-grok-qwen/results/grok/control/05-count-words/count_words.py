import string


def count_words(text: str) -> dict:
    counts = {}
    for raw in text.split():
        w = raw
        while w and w[0] in string.punctuation:
            w = w[1:]
        while w and w[-1] in string.punctuation:
            w = w[:-1]
        if not w:
            continue
        key = w.casefold()
        counts[key] = counts.get(key, 0) + 1
    return counts
