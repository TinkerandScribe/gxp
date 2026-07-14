# BRIEF — Rate-Limit Service Repair

## Goal
Fix 3 buggy modules so the rate limiter correctly enforces per-key sliding-window limits with fail-closed config.

## Binary Criteria (must all pass)
1. **Fail-closed config**: `load_limits(path)` returns `max_requests=0` when file missing or invalid.
2. **Per-key isolation**: `HitStore` stores hits per key; hits for "a" never count for "b".
3. **Sliding window**: `hits_in_window` counts only timestamps in `(now - W, now]` (left-exclusive, right-inclusive).
4. **Check-then-record**: `allow()` checks current hits first; if `>= max_requests`, returns False without recording.
5. **Exact limit enforcement**: exactly `max_requests` calls return True, the next returns False.
6. **Zero max denies all**: `max_requests=0` always returns False from `allow()`.
7. **from_config works**: constructs RateLimiter from config file or None (defaults).
8. **Default config**: `load_limits(None)` returns `{max_requests: 5, window_seconds: 60.0}`.

## Out of Scope
- Adding third-party dependencies.
- Changing public API signatures.
- Hidden tests (we don't create them).

## Verification
Run: `python -m unittest discover -s tests_public -v`
Plus manual checks for fail-closed, isolation, window boundary, and zero-max behavior.
