"""Join path parts under a root, rejecting any path that would escape it."""

import os


def safe_join(root: str, *parts: str) -> str:
    norm_root = os.path.normpath(os.path.abspath(root))

    for part in parts:
        if os.path.isabs(part):
            raise ValueError(f"escape: absolute path segment {part!r} is not allowed")

    joined = os.path.join(norm_root, *parts) if parts else norm_root
    result = os.path.normpath(os.path.abspath(joined))

    if result != norm_root and not result.startswith(norm_root + os.sep):
        raise ValueError(f"escape: {result!r} is outside root {norm_root!r}")

    return result
