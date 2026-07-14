"""Fail-closed breaker config."""

from __future__ import annotations

from pathlib import Path

DEFAULTS = {"failure_threshold": 3, "success_threshold": 2, "open_seconds": 30.0}
CLOSED = {"failure_threshold": 1, "success_threshold": 10**9, "open_seconds": 1e9}


def load_breaker_config(path: str | None) -> dict:
    if path is None:
        return dict(DEFAULTS)
    p = Path(path)
    if not p.is_file():
        return dict(CLOSED)
    ft = st = op = None
    try:
        for raw in p.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                return dict(CLOSED)
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            if k == "failure_threshold":
                ft = int(v)
            elif k == "success_threshold":
                st = int(v)
            elif k == "open_seconds":
                op = float(v)
            else:
                return dict(CLOSED)
    except Exception:
        return dict(CLOSED)
    if ft is None or st is None or op is None:
        return dict(CLOSED)
    if ft < 1 or st < 1 or op <= 0:
        return dict(CLOSED)
    return {"failure_threshold": ft, "success_threshold": st, "open_seconds": op}
