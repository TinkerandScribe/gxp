# BRIEF — Rate-Limit Service Repair

## Goal
Fix 3 buggy modules in `service/` so the rate limiter correctly implements:
- Sliding window `(now - W, now]`
- Per-key isolation
- Fail-closed config parsing
- Check-then-record logic (no off-by-one)

## Binary Criteria
1. **Fail-closed config**: missing/invalid file → `max_requests=0`, not huge number.
2. **Per-key storage**: hits for key "a" never counted for key "b".
3. **Sliding window**: only timestamps in `(now - window_seconds, now]` count (left-exclusive, right-inclusive).
4. **Check-then-record**: `allow()` checks current count first; if `>= max_requests`, deny without recording.
5. **max_requests=0 always denies**: no hits recorded, always returns False.
6. **Exact limit enforcement**: with `max_requests=N`, exactly N calls return True, then all subsequent return False within the window.
7. **from_config(None)**: returns limiter with defaults (max_requests=5, window_seconds=60.0).
8. **Config parsing**: handles comments, blank lines, either order of keys.

## Out of Scope
- Adding third-party dependencies
- Changing public API signatures
- Adding hidden_tests/

## Verification
Run: `python -m unittest discover -s tests_public -v`
Plus manual integration checks for fail-closed, isolation, window boundary.
