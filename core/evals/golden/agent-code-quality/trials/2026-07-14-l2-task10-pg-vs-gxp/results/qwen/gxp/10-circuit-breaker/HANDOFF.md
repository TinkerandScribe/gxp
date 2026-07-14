# HANDOFF — Circuit Breaker Repair

## Summary
Fixed 3 files in the `service/` package to implement correct circuit breaker semantics.

## Bugs Fixed

### `service/config.py`
- **Bug**: Missing/invalid config returned fail-open defaults (`failure_threshold: 10**9, success_threshold: 1, open_seconds: 0.001`) — the opposite of safe.
- **Fix**: Changed to fail-closed defaults (`failure_threshold: 1, success_threshold: 10**9, open_seconds: 1e9`). Opens after just 1 failure; almost never auto-closes. Added validation for parsed values (must be ≥ 1 for thresholds, > 0 for open_seconds).

### `service/state.py`
- **Bug**: Used generic `failures`/`successes` names without clear separation of closed vs half-open counters.
- **Fix**: Renamed to `consecutive_failures` and `consecutive_successes` for clarity. State class is correct as-is; the logic bugs were in `breaker.py`.

### `service/breaker.py`
- **Bug 1**: `allow_request()` always returned `True` — never blocked in open state.
- **Fix**: Implemented proper state machine: closed → allows all; open → blocks until timeout then transitions to half_open; half_open → allows probes.
- **Bug 2**: `record_failure()` incremented counter but never transitioned to open.
- **Fix**: Transitions to open when `consecutive_failures >= failure_threshold`, setting `opened_at = clock()`.
- **Bug 3**: `record_success()` only reset failures, ignoring half-open logic.
- **Fix**: In closed state, resets consecutive failures. In half_open state, increments consecutive successes; transitions to closed when `>= success_threshold`.
- **Bug 4**: No handling of failure in half_open state.
- **Fix**: Any failure in half_open immediately re-opens (resets success streak, sets new `opened_at`).

## Verification
- Public tests: ✅ PASS (2/2)
- All 8 binary criteria: ✅ PASS
- Edge cases (invalid config, partial config, comments, re-open timing): ✅ PASS
