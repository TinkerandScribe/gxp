"""Fail-closed config."""
from __future__ import annotations
from pathlib import Path
DEFAULTS={'max_requests':5,'window_seconds':60.0}
CLOSED={'max_requests':0,'window_seconds':60.0}
def load_limits(path: str | None) -> dict:
    if path is None: return dict(DEFAULTS)
    p=Path(path)
    if not p.is_file(): return dict(CLOSED)
    mr=ws=None
    try:
        for raw in p.read_text(encoding='utf-8').splitlines():
            line=raw.strip()
            if not line or line.startswith('#'): continue
            if '=' not in line: return dict(CLOSED)
            k,v=line.split('=',1); k,v=k.strip(),v.strip()
            if k=='max_requests': mr=int(v)
            elif k=='window_seconds': ws=float(v)
            else: return dict(CLOSED)
    except Exception: return dict(CLOSED)
    if mr is None or ws is None or mr<0 or ws<=0: return dict(CLOSED)
    return {'max_requests':mr,'window_seconds':ws}
