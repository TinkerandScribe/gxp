# BRIEF — Circuit Breaker Repair

## Goal
Fix the broken circuit breaker package so it correctly implements closed → open → half_open → closed state transitions with proper thresholds and timing.

## Binary Criteria
1. **Config defaults**: `load_breaker_config(None)` returns `{failure_threshold: 3, success_threshold: 2, open_seconds: 30.0}`
2. **Fail-closed config**: Missing/invalid file returns `{failure_threshold: 1, success_threshold: 1e9, open_seconds: 1e9}` (opens immediately, almost never closes)
3. **Closed state**: `allow_request()` always True; failures increment counter; at threshold → open with timestamp
4. **Open state**: `allow_request()` False until `open_seconds` elapsed, then transitions to half_open and returns True
5. **Half-open probes**: Each success increments consecutive successes; at `success_threshold` → closed with reset
6. **Half-open failure**: Any failure immediately re-opens (new timestamp, reset success streak)
7. **Success in closed**: Resets consecutive failure counter to 0
8. **Clock injection**: Custom clock works for deterministic testing

## Out of Scope
- Async support
- Metrics/logging
- Third-party dependencies

## Verification
Run `python -m unittest discover -s tests_public -v` and manually verify all criteria above.
