# BRIEF — Circuit Breaker Repair

## Goal
Fix the broken circuit breaker package so it correctly implements closed → open → half_open → closed state transitions with proper thresholds and timing.

## Binary Criteria
1. **Config defaults**: `load_breaker_config(None)` returns `{failure_threshold: 3, success_threshold: 2, open_seconds: 30.0}`
2. **Fail-closed config**: Missing/invalid file returns `{failure_threshold: 1, success_threshold: 1e9, open_seconds: 1e9}` (opens after 1 failure, almost never closes)
3. **Closed state**: `allow_request()` always True; failures counted consecutively; successes reset failure count
4. **Open transition**: After `failure_threshold` consecutive failures in closed, transitions to open with `opened_at = clock()`
5. **Open state**: `allow_request()` returns False until `clock() - opened_at >= open_seconds`, then transitions to half_open and returns True
6. **Half-open success**: Needs `success_threshold` consecutive successes to transition back to closed; resets counters
7. **Half-open failure**: Any single failure immediately re-opens (resets success streak, sets new `opened_at`)
8. **Clock injection**: Default is `time.monotonic`; injectable via `clock` parameter

## Out of Scope
- Async support
- Metrics/logging
- Third-party dependencies

## Verification
Run: `python -m unittest discover -s tests_public -v`
