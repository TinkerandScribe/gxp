## Handoff — Circuit Breaker Fix

### Bugs Fixed

1. **`service/breaker.py` — `allow_request()` always returned True**
   - Now checks current mode: closed→allow, open→reject, half_open→allow (probe).

2. **`service/breaker.py` — `record_failure()` never opened the circuit**
   - Now increments failure count in closed state and transitions to "open" when failures >= failure_threshold.
   - Records `opened_at` timestamp for timeout tracking.

3. **`service/breaker.py` — no half-open logic**
   - `mode()` now checks elapsed time since opening; if >= open_seconds, transitions to half_open.
   - In half_open: counts consecutive successes; when >= success_threshold, closes the circuit.
   - Any failure in half_open immediately re-opens (resets timer).

4. **`service/config.py` — fail-open on missing/bad config**
   - Previously returned `failure_threshold=10**9` (effectively never opens) for missing files or parse errors.
   - Now returns safe defaults (`failure_threshold=3, success_threshold=2, open_seconds=30.0`) — fail-closed behavior.

### State Machine Summary
- **closed**: allows requests; tracks consecutive failures; opens at threshold.
- **open**: rejects all requests; after `open_seconds`, transitions to half_open.
- **half_open**: allows probe requests; needs `success_threshold` consecutive successes to close; any failure re-opens.

### Verification
- Public tests pass: `python -m unittest discover -s tests_public -v` → OK
- All 8 binary criteria verified via manual test script.
