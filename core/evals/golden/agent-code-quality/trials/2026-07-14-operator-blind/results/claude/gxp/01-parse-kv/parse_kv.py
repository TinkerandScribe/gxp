"""Robust KEY=VALUE config parser. See prompt.md for the full spec."""

import re

_KEY_RE = re.compile(r"[A-Za-z0-9_]+")


def parse_kv(text: str) -> dict:
    """Parse KEY=VALUE lines into a dict.

    - Blank lines and lines whose first non-whitespace char is ``#`` are ignored.
    - A key is the text left of the first ``=``, trimmed; it must match
      ``[A-Za-z0-9_]+``.
    - A value is the entire substring after the first ``=``. Interior spaces are
      preserved; a single pair of matching double quotes wrapping the whole value
      is removed. Unmatched/nested quotes are left as-is.
    - Duplicate keys: last occurrence wins.
    - Lines that are not blank, not comments, and not a valid ``KEY=VALUE`` are
      collected; if any exist, raise ``ValueError`` mentioning the count.
    """
    result: dict = {}
    invalid_count = 0

    for line in text.splitlines():
        if line.strip() == "":
            continue  # blank
        if line.lstrip()[:1] == "#":
            continue  # comment

        if "=" not in line:
            invalid_count += 1
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        if not _KEY_RE.fullmatch(key):
            invalid_count += 1
            continue

        # Strip a single pair of matching double quotes wrapping the whole value.
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]

        result[key] = value  # last key wins

    if invalid_count:
        raise ValueError(f"parse_kv: found {invalid_count} invalid line(s)")

    return result
