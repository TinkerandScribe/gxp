"""Starter — unsafe join (no abspath, no escape check)."""

import os


def safe_join(root: str, *parts: str) -> str:
    root_abs = os.path.abspath(os.path.normpath(root))
    result = root_abs

    for part in parts:
        if os.path.isabs(part):
            raise ValueError("Escape attempt: absolute path component")

        candidate = os.path.normpath(os.path.join(result, part))
        if candidate != root_abs and not candidate.startswith(root_abs + os.sep):
            raise ValueError("Escape attempt: path would escape root")

        result = candidate

    return result
