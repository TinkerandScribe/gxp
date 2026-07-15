"""Config loader — fail-closed on bad config."""

from __future__ import annotations

from pathlib import Path

DEFAULTS = {"failure_threshold": 3, "success_threshold": 2, "open_seconds": 30.0}

FAIL_CLOSED = {
    "failure_threshold": 1,
    "success_threshold": 10**9,
    "open_seconds": 1e9,
}


def load_breaker_config(path: str | None) -> dict:
    if path is None:
        return dict(DEFAULTS)
    p = Path(path)
    if not p.is_file():
        # Fail closed: opens immediately after one failure, almost never closes
        return dict(FAIL_CLOSED)
    cfg = dict(DEFAULTS)
    try:
        for raw in p.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            if k in cfg:
                cfg[k] = int(v) if k != "open_seconds" else float(v)
    except Exception:
        return dict(FAIL_CLOSED)
    return cfg
