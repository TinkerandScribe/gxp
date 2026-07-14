"""Safe path join constrained to a root directory."""

import os


def safe_join(root: str, *parts: str) -> str:
    abs_root = os.path.abspath(os.path.normpath(root))

    if not parts:
        return abs_root

    candidate = os.path.join(abs_root, *parts)
    result = os.path.abspath(os.path.normpath(candidate))

    try:
        common = os.path.commonpath([abs_root, result])
    except ValueError:
        raise ValueError("path would escape root") from None

    if common != abs_root:
        raise ValueError("path would escape root")

    return result
