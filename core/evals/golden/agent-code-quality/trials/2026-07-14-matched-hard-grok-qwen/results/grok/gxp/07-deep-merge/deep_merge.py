"""deep_merge — GXP implement (criteria-first)."""

from __future__ import annotations


def _deepcopy(value):
    if isinstance(value, dict):
        return {k: _deepcopy(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deepcopy(v) for v in value]
    return value


def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    if list_mode not in ("replace", "extend", "unique"):
        raise ValueError(f"bad list_mode: {list_mode}")

    result: dict = {}
    keys = set(base.keys()) | set(override.keys())
    for key in keys:
        has_b = key in base
        has_o = key in override
        if has_b and not has_o:
            result[key] = _deepcopy(base[key])
            continue
        if has_o and not has_b:
            result[key] = _deepcopy(override[key])
            continue

        left, right = base[key], override[key]
        if right is None:
            # delete
            continue
        if type(left) is dict and type(right) is dict:
            result[key] = deep_merge(left, right, list_mode=list_mode)
        elif isinstance(left, list) and isinstance(right, list):
            if list_mode == "replace":
                result[key] = _deepcopy(right)
            elif list_mode == "extend":
                result[key] = _deepcopy(left) + _deepcopy(right)
            else:  # unique
                acc = _deepcopy(left)
                for item in right:
                    if item not in acc:
                        acc.append(_deepcopy(item))
                result[key] = acc
        else:
            result[key] = _deepcopy(right)
    return result
