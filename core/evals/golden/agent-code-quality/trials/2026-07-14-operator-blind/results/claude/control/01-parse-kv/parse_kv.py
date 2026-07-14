"""Robust KEY=VALUE config parser. See prompt.md for the full spec."""

import re

_KEY_RE = re.compile(r"[A-Za-z0-9_]+\Z")


def parse_kv(text: str) -> dict:
    """Parse KEY=VALUE lines into a dict.

    - Blank lines and lines whose first non-whitespace char is '#' are ignored.
    - Keys are trimmed and must match [A-Za-z0-9_]+.
    - Values are everything after the first '=', kept verbatim except that a
      single pair of double quotes wrapping the whole value is stripped.
    - Duplicate keys: last occurrence wins.
    - Invalid lines are collected; if any exist, ValueError is raised with a
      message containing the count and the word 'invalid'.
    """
    result = {}
    errors = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in line:
            errors.append(line)
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not _KEY_RE.match(key):
            errors.append(line)
            continue
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        result[key] = value
    if errors:
        raise ValueError(f"{len(errors)} invalid line(s) found")
    return result
