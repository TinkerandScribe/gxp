from __future__ import annotations
def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    out = dict(base)
    out.update(override)
    return out
