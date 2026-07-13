"""Starter — incomplete slugify."""


def slugify(text: str) -> str:
    # BUG: only replaces spaces; leaves other punctuation; no lowercase
    return text.replace(" ", "-")
