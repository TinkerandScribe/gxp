import re
def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9_]+", "-", s)
    return s.strip("-")
