# HANDOFF — Circuit Breaker Repair

## Summary
Fixed 3 files in the `service/` package to implement correct circuit breaker semantics.

## Bugs Fixed

### `service/config.py`
- **Bug**: Fail-open on missing/invalid config (returned `failure_threshold: 10**9, success_threshold: 1, open_seconds: 0.001`)
- **Fix**: Changed to fail-closed defaults (`failure_threshold: 1, success_threshold: 10**9, open_seconds: 1e9`) — opens after one failure, almost never closes

### `service/breaker.py`
- **Bug 1**: `allow_request()` always returned `True` regardless of state
- **Fix**: Implemented proper state machine:
  - `closed`: always allows
  - `open`: blocks until `open_seconds` elapsed, then transitions to `half_open` and allows
  - `half_open`: allows probe requests
- **Bug 2**: `record_failure()` incremented counter but never transitioned to open
- **Fix**: Transitions to `open` when failures >= `failure_threshold`, sets `opened_at = clock()`
- **Bug 3**: `record_success()` only reset failures, ignored half_open logic
- **Fix**: In `half_open`, increments success counter; transitions to `closed` when successes >= `success_threshold`
- **Bug 4**: No handling of failure in `half_open` state
- **Fix**: Any failure in `half_open` immediately re-opens with new `opened_at`

### `service/state.py`
- Minor: Added type annotations for clarity (no functional bug)

## Verification
- Public tests: 2/2 passing
- All 8 binary criteria verified via manual test script
- Edge cases tested: valid config, partial config, invalid values, missing file
