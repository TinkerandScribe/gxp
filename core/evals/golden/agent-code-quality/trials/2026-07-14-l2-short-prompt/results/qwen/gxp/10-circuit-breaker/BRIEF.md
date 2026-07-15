# BRIEF — Circuit Breaker Repair

## Goal
Fix the `service/` package so the circuit breaker correctly implements closed → open → half-open → closed state transitions.

## Binary Criteria
1. **Closed state**: allows requests; counts consecutive failures; opens when failures >= failure_threshold.
2. **Open state**: rejects all requests; after `open_seconds` elapses, transitions to half-open.
3. **Half-open state**: allows probe requests; needs `success_threshold` consecutive successes to close; any failure re-opens (resetting timer).
4. **record_success in closed**: resets failure counter to 0.
5. **record_failure in closed**: increments failure counter.
6. **from_config with None path**: uses safe defaults (failure_threshold=3, success_threshold=2, open_seconds=30.0).
7. **from_config with missing/bad file**: fails CLOSED (uses same safe defaults), NOT fail-open.
8. **State isolation**: each CircuitBreaker instance has independent state.

## Out of Scope
- Async support
- Distributed circuit breakers
- Custom serialization

## Verification
`python -m unittest discover -s tests_public -v` must pass (exit 0).
