"""Reference solution for 01-parse-kv (not shown to agents under test)."""

import re

_KEY = re.compile(r"^[A-Za-z0-9_]+$")


def parse_kv(text: str) -> dict:
    result = {}
    invalid = 0
    for raw in text.splitlines():
        if not raw.strip():
            continue
        if raw.lstrip().startswith("#"):
            continue
        if "=" not in raw:
            invalid += 1
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key or not _KEY.match(key):
            invalid += 1
            continue
        # value: only strip matching wrapping double quotes; do not strip interior
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        result[key] = value
    if invalid:
        raise ValueError(f"{invalid} invalid line(s) in kv text")
    return result
