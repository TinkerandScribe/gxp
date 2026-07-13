"""Control arm — one-shot slugify."""


def slugify(text: str) -> str:
    text = text.lower()
    out = []
    prev_dash = False
    for ch in text:
        if ch.isalnum() and ord(ch) < 128:
            out.append(ch)
            prev_dash = False
        else:
            if not prev_dash:
                out.append("-")
                prev_dash = True
    s = "".join(out).strip("-")
    return s
