"""Load rate-limit config — starter has fail-open bug."""

from __future__ import annotations

from pathlib import Path

DEFAULTS = {"max_requests": 5, "window_seconds": 60.0}


def load_limits(path: str | None) -> dict:
    if path is None:
        return dict(DEFAULTS)
    p = Path(path)
    if not p.is_file():
        # BUG: fail open — treat missing as generous defaults
        return {"max_requests": 10**9, "window_seconds": 60.0}
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
        # BUG: fail open on parse errors
        return {"max_requests": 10**9, "window_seconds": 60.0}
    return {"max_requests": max_requests, "window_seconds": window_seconds}
