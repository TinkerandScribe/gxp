"""Starter implementation — intentionally incomplete / wrong.

Replace this with a correct parse_kv per prompt.md.
"""


def parse_kv(text: str) -> dict:
    """Parse KEY=VALUE lines into a dict. See prompt.md for full spec."""
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue  # BUG: should error on invalid lines, not skip
        key, value = line.split("=", 1)
        key = key.strip()
        # BUG: does not validate key charset
        # BUG: strips value aggressively
        result[key] = value.strip()
    return result
