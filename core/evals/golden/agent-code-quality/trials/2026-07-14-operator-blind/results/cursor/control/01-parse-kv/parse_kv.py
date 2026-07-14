"""Parse KEY=VALUE config text into a dict."""

from __future__ import annotations

import re

_KEY_RE = re.compile(r"^[A-Za-z0-9_]+$")


def _unwrap_quotes(value: str) -> str:
    """Strip one optional matching pair of double quotes around the whole value."""
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


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

        raw_key, value = line.split("=", 1)
        key = raw_key.strip()
        if not key or not _KEY_RE.fullmatch(key):
            invalid += 1
            continue

        result[key] = _unwrap_quotes(value)

    if invalid:
        raise ValueError(f"{invalid} invalid line(s) in config")

    return result
