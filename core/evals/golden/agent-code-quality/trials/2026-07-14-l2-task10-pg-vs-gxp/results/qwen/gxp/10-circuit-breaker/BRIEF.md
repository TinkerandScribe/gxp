# BRIEF — Circuit Breaker Repair

## Goal
Fix the broken circuit breaker package so it correctly implements closed → open → half_open → closed state transitions with proper thresholds and timing.

## Binary Criteria
1. **Config defaults**: `load_breaker_config(None)` returns `{failure_threshold: 3, success_threshold: 2, open_seconds: 30.0}`
2. **Fail-closed config**: Missing/invalid file returns `{failure_threshold: 1, success_threshold: 1e9, open_seconds: 1e9}` (opens after 1 failure, almost never closes)
3. **Closed state**: `allow_request()` always True; failures increment counter; at threshold → open with `opened_at = clock()`
4. **Open state**: `allow_request()` False until `clock() - opened_at >= open_seconds`, then transitions to half_open and returns True
5. **Half-open probes**: Each success increments consecutive successes; at `>= success_threshold` → closed, reset counters
6. **Half-open failure**: Any failure in half_open immediately re-opens (reset success streak, set new `opened_at`)
7. **Success in closed resets failures**: `record_success()` in closed state resets failure counter to 0
8. **Clock injection**: Custom clock works for deterministic testing; default is `time.monotonic`

## Out of Scope
- Async support
- Metrics/logging
- Third-party dependencies

## Verification
- Run `python -m unittest discover -s tests_public -v` (must pass)
- Manual verification of all 8 criteria above
