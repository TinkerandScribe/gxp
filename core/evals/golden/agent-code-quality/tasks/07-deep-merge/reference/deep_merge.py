"""Reference deep_merge."""

from __future__ import annotations

import copy


def _clone(value):
    if isinstance(value, dict):
        return {k: _clone(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_clone(v) for v in value]
    return value


def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    if list_mode not in ("replace", "extend", "unique"):
        raise ValueError(f"unknown list_mode: {list_mode}")

    result: dict = {}
    keys = set(base) | set(override)
    for key in keys:
        in_b = key in base
        in_o = key in override
        if in_b and not in_o:
            result[key] = _clone(base[key])
            continue
        if in_o and not in_b:
            result[key] = _clone(override[key])
            continue
        # both
        b = base[key]
        o = override[key]
        if o is None:
            continue  # delete
        if isinstance(b, dict) and isinstance(o, dict) and type(b) is dict and type(o) is dict:
            result[key] = deep_merge(b, o, list_mode=list_mode)
        elif isinstance(b, list) and isinstance(o, list):
            if list_mode == "replace":
                result[key] = _clone(o)
            elif list_mode == "extend":
                result[key] = _clone(b) + _clone(o)
            else:  # unique
                acc = _clone(b)
                for item in o:
                    if item not in acc:
                        acc.append(_clone(item))
                result[key] = acc
        else:
            result[key] = _clone(o)
    return result
