"""Safe path join constrained to a root directory."""

import os


def safe_join(root: str, *parts: str) -> str:
    root_abs = os.path.abspath(os.path.normpath(root))

    if not parts:
        return root_abs

    joined = os.path.join(root_abs, *parts)
    result = os.path.abspath(os.path.normpath(joined))

    try:
        common = os.path.commonpath([result, root_abs])
    except ValueError:
        raise ValueError("path would escape root") from None

    if common != root_abs:
        raise ValueError("path would escape root")

    return result
