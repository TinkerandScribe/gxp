# HANDOFF — Circuit Breaker Repair

## Summary
Fixed 3 files in the `service/` package to implement correct circuit breaker semantics.

## Bugs Fixed

### `service/config.py`
- **Bug**: Fail-open on missing/invalid config (returned `failure_threshold: 10**9, success_threshold: 1, open_seconds: 0.001`)
- **Fix**: Changed to fail-closed defaults: `{failure_threshold: 1, success_threshold: 10**9, open_seconds: 1e9}` — opens immediately after one failure, almost never closes

### `service/breaker.py`
- **Bug 1**: `allow_request()` always returned `True` regardless of state
- **Fix**: Implemented proper state machine:
  - **closed**: always allows
  - **open**: denies until `open_seconds` elapsed, then transitions to half_open and allows
  - **half_open**: allows probe requests
- **Bug 2**: `record_failure()` incremented counter but never transitioned to open
- **Fix**: Transitions to open when failures >= threshold; in half_open, any failure re-opens immediately
- **Bug 3**: `record_success()` only reset failures (no half_open logic)
- **Fix**: In closed state resets failures; in half_open increments successes and transitions to closed at threshold

### `service/state.py`
- No functional bug, but added docstrings clarifying each attribute's purpose

## Verification
- Public tests: 2/2 passing
- All 9 binary criteria verified via manual test script:
  1. Config defaults ✓
  2. Fail-closed on missing file ✓
  3. Fail-closed on invalid file ✓
  4. Closed→open at failure threshold ✓
  5. Open→half_open after timeout ✓
  6. Half_open→closed at success_threshold ✓
  7. Half_open failure→open ✓
  8. Success resets failures in closed ✓
  9. from_config with valid file ✓
