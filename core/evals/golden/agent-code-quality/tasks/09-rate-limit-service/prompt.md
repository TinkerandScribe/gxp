# Task: repair rate-limit service (multi-file, tool-using)

## Deliverable

Fix the **broken** Python package under this workspace so the rate limiter
behaves per the spec below. You may edit existing files and add tests under
`tests_public/`. Do **not** add third-party dependencies.

## What you should do (tool use expected)

1. Read `.ai/PROGRAM.md`, `.ai/rules/`, and `.ai/failures/` before coding.  
2. Inspect `service/` and `README.md`.  
3. Run the project verify command from PROGRAM.md (public tests).  
4. Fix code until you believe the full spec is met — public tests alone are
   **not** sufficient proof of correctness.  
5. Prefer small fixes over a total rewrite of unrelated files.

## Public API (must preserve)

### `service.config.load_limits(path: str | None) -> dict`

- Returns a dict with integer `max_requests` ≥ 0 and float `window_seconds` > 0.  
- `path is None`: return defaults `max_requests=5`, `window_seconds=60.0`.  
- File missing or invalid content: **fail closed** — return
  `max_requests=0`, `window_seconds=60.0` (deny all). Never “open” on error.  
- Valid file format: two lines `max_requests=<int>` and `window_seconds=<float>`
  (either order). Extra blank lines / `#` comments allowed.

### `service.store.HitStore`

- `record(key: str, ts: float) -> None` — append a hit timestamp for `key`.  
- `hits_in_window(key: str, now: float, window_seconds: float) -> int` — count
  hits for `key` with timestamp in `(now - window_seconds, now]` (half-open on
  the left: older endpoint exclusive, `now` inclusive).  
- Keys are isolated (hits for `"a"` never count for `"b"`).

### `service.limiter.RateLimiter`

```python
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float, *, clock=None, store=None): ...
    def allow(self, key: str) -> bool: ...
    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "RateLimiter": ...
```

- `clock` zero-arg callable returning float seconds (default `time.monotonic`).  
- `allow(key)`: if current hits in window for `key` are already `>= max_requests`,
  return `False` **without** recording. Otherwise record a hit at `clock()` and
  return `True`.  
- Sliding window using `HitStore.hits_in_window`.  
- `max_requests == 0` → always deny.  
- `from_config` loads limits via `load_limits` and constructs a limiter.

## Constraints

- Stdlib only.  
- Edit only this workspace; do not invent a `hidden_tests/` tree.  
- Keep the public names above importable.

## Done means

You ran public verify, fixed multi-factor bugs (window, isolation, fail-closed),
and would expect hidden integration tests to pass.
