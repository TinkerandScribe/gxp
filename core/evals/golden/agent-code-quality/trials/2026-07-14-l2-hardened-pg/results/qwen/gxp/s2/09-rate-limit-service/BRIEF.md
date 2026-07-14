# BRIEF — Rate-Limit Service Repair

## Goal
Fix 3 buggy modules in `service/` so the rate limiter correctly implements:
- Sliding window with half-open interval `(now - W, now]`
- Per-key isolation in HitStore
- Fail-closed config (missing/bad file → max_requests=0)
- Check-then-record logic (deny when hits >= max_requests)

## Binary Criteria
1. `load_limits(None)` returns `{max_requests: 5, window_seconds: 60.0}`
2. `load_limits("/nonexistent")` returns `{max_requests: 0, window_seconds: 60.0}` (fail closed)
3. `load_limits` with invalid content returns `{max_requests: 0, window_seconds: 60.0}` (fail closed)
4. `HitStore.record("a", t)` does NOT affect `hits_in_window("b", ...)` — keys isolated
5. `hits_in_window` counts only timestamps in `(now - W, now]` (exclusive left, inclusive right)
6. `RateLimiter.allow(key)` returns False when hits already >= max_requests (no extra recording)
7. `max_requests=0` always denies (returns False, no recording)
8. Exactly `max_requests` calls to `allow()` succeed before denial

## Out of Scope
- Adding third-party dependencies
- Changing public API signatures
- Modifying test structure beyond adding tests

## Verification
Run: `python -m unittest discover -s tests_public -v`
