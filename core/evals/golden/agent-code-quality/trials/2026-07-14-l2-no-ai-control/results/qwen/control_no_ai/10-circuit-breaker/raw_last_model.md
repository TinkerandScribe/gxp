All tests pass — both the public smoke tests and my comprehensive inline verification of all state transitions, config loading, and fail-closed behavior. The fixes were:

1. **`service/config.py`**: Changed the fallback for missing/invalid files from fail-open (`failure_threshold: 10**9`) to fail-closed (`failure_threshold: 1`, `success_threshold: 10**9`, `open_seconds: 1e9`).

2. **`service/breaker.py`**: Rewrote the full state machine:
   - `allow_request()`: properly checks mode — closed allows, open blocks (unless timeout elapsed → transitions to half_open), half_open allows probes.
   - `record_success()`: resets failures in closed; increments successes in half_open and transitions to closed when threshold met.
   - `record_failure()`: increments failures in closed and opens at threshold; immediately re-opens from half_open on any failure.

{"action":"done"}