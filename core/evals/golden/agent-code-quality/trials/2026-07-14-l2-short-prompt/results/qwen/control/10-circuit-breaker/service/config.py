"""Config loader — fail-closed on bad/missing config."""

from __future__ import annotations

from pathlib import Path

DEFAULTS = {"failure_threshold": 3, "success_threshold": 2, "open_seconds": 30.0}


def load_breaker_config(path: str | None) -> dict:
    if path is None:
        return dict(DEFAULTS)
    p = Path(path)
    if not p.is_file():
        # Fail-closed: use safe defaults that will trip the breaker easily
        return dict(DEFAULTS)
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
        return dict(DEFAULTS)
    return cfg
