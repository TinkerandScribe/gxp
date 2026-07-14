# BRIEF — Rate-Limit Service Repair

## Goal
Fix the broken rate-limit service so it correctly implements a sliding-window
rate limiter with per-key isolation, fail-closed config, and proper check-then-record logic.

## Binary Criteria (must all pass)

1. **Fail-closed config**: `load_limits(path)` returns `max_requests=0` when file is missing or invalid content.
2. **Default config**: `load_limits(None)` returns `{"max_requests": 5, "window_seconds": 60.0}`.
3. **Valid config parsing**: Two-line file with `max_requests=<int>` and `window_seconds=<float>` (any order) is parsed correctly; comments and blank lines are ignored.
4. **Per-key isolation**: Hits for key "a" never count toward key "b" in `HitStore`.
5. **Sliding window**: `hits_in_window(key, now, W)` counts timestamps in `(now - W, now]` (exclusive left, inclusive right).
6. **Check-then-record**: `allow(key)` checks current hits first; if `>= max_requests`, returns False without recording.
7. **Zero max_requests always denies**: When `max_requests == 0`, every call to `allow()` returns `False` and records nothing.
8. **from_config integration**: `RateLimiter.from_config(path)` correctly loads config and constructs a limiter.

## Out of Scope
- Adding third-party dependencies.
- Changing the public API signatures.
- Writing hidden tests (only `tests_public/`).

## Verification
Run: `python -m unittest discover -s tests_public -v`
Plus manual verification against all 8 criteria above.

