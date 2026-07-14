"""deep_merge — control implement from prompt."""

from __future__ import annotations


def _clone(v):
    if isinstance(v, dict):
        return {k: _clone(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_clone(x) for x in v]
    return v


def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    if list_mode not in ("replace", "extend", "unique"):
        raise ValueError(f"unknown list_mode: {list_mode}")

    out: dict = {}
    for key in set(base) | set(override):
        in_b = key in base
        in_o = key in override
        if in_b and not in_o:
            out[key] = _clone(base[key])
            continue
        if in_o and not in_b:
            out[key] = _clone(override[key])
            continue
        b, o = base[key], override[key]
        if o is None:
            continue
        if type(b) is dict and type(o) is dict:
            out[key] = deep_merge(b, o, list_mode=list_mode)
        elif isinstance(b, list) and isinstance(o, list):
            if list_mode == "replace":
                out[key] = _clone(o)
            elif list_mode == "extend":
                out[key] = _clone(b) + _clone(o)
            else:
                acc = _clone(b)
                for item in o:
                    if item not in acc:
                        acc.append(_clone(item))
                out[key] = acc
        else:
            out[key] = _clone(o)
    return out
