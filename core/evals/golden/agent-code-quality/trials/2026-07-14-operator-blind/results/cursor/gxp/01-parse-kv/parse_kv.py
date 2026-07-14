"""Parse multi-line KEY=VALUE config text into a dict."""

from __future__ import annotations

import re

_KEY_RE = re.compile(r"^[A-Za-z0-9_]+$")


def parse_kv(text: str) -> dict[str, str]:
    """Parse KEY=VALUE lines into a dict. See prompt.md for full spec."""
    result: dict[str, str] = {}
    invalid = 0

    for line in text.splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue

        if "=" not in line:
            invalid += 1
            continue

        key_part, value = line.split("=", 1)
        key = key_part.strip()
        if not key or _KEY_RE.fullmatch(key) is None:
            invalid += 1
            continue

        if (
            len(value) >= 2
            and value[0] == '"'
            and value[-1] == '"'
            and '"' not in value[1:-1]
        ):
            value = value[1:-1]

        result[key] = value

    if invalid:
        raise ValueError(f"{invalid} invalid line(s) found")

    return result
