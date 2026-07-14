"""Load rate-limit config — fixed: fail-closed on errors."""

from __future__ import annotations

from pathlib import Path

DEFAULTS = {"max_requests": 5, "window_seconds": 60.0}

FAIL_CLOSED = {"max_requests": 0, "window_seconds": 60.0}


def load_limits(path: str | None) -> dict:
    if path is None:
        return dict(DEFAULTS)
    p = Path(path)
    if not p.is_file():
        # Fail closed — deny all traffic when config file is missing
        return dict(FAIL_CLOSED)
    max_requests = DEFAULTS["max_requests"]
    window_seconds = DEFAULTS["window_seconds"]
    try:
        for raw in p.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            if k == "max_requests":
                max_requests = int(v)
            elif k == "window_seconds":
                window_seconds = float(v)
    except Exception:
        # Fail closed on parse errors
        return dict(FAIL_CLOSED)
    return {"max_requests": max_requests, "window_seconds": window_seconds}
