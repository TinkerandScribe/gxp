"""Reference safe_join."""

import os


def safe_join(root: str, *parts: str) -> str:
    root_abs = os.path.abspath(root)
    candidate = os.path.abspath(os.path.join(root_abs, *parts))
    root_norm = os.path.normpath(root_abs)
    cand_norm = os.path.normpath(candidate)
    if cand_norm == root_norm or cand_norm.startswith(root_norm + os.sep):
        return cand_norm
    raise ValueError("path escape outside root")
