# HANDOFF — Circuit Breaker Repair

## Summary
Fixed the broken `service/` circuit breaker package with three key changes:

### 1. `service/config.py` — Fail-closed on bad config
- **Bug**: Missing/bad config files returned fail-open values (`failure_threshold=10**9`, effectively never opening).
- **Fix**: All error paths now return safe defaults (`failure_threshold=3, success_threshold=2, open_seconds=30.0`).

### 2. `service/breaker.py` — Full state machine implementation
- **Bug**: `allow_request()` always returned `True`; `record_failure()` counted but never opened the circuit.
- **Fix**: Implemented proper closed → open → half_open → closed transitions:
  - **Closed**: allows requests; counts consecutive failures; opens when `failures >= failure_threshold`.
  - **Open**: rejects all requests; auto-transitions to half_open after `open_seconds` elapsed (checked lazily in `mode()`).
  - **Half-open**: allows probe requests; needs `success_threshold` consecutive successes to close; any failure re-opens.
  - **record_success** in closed resets failure counter; in half_open increments success counter.
  - **record_failure** in closed increments failure counter; in half_open immediately re-opens.

### 3. `service/state.py` — No changes needed
- State class already had all required fields (`mode`, `failures`, `successes`, `opened_at`).

## Verification
- Public tests pass: `python -m unittest discover -s tests_public -v` → OK (2/2)
- All 8 binary criteria verified via manual test script.
