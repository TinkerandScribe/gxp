"""Starter — unsafe join (no abspath, no escape check)."""

import os


def safe_join(root: str, *parts: str) -> str:
    # BUG: relative join only; no containment / escape checks
    return os.path.join(root, *parts)
