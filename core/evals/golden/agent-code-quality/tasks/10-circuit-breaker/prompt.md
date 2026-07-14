# Task: repair circuit breaker (multi-file, tool-using)

## Deliverable

Fix the broken package so the circuit breaker matches the spec. Stdlib only.

## Tool use expected

1. Read `.ai/PROGRAM.md`, `.ai/rules/`, `.ai/failures/`.  
2. Run public verify; know public tests may be weak.  
3. Fix multi-file bugs (state, thresholds, half-open probes).

## Public API

### `service.config.load_breaker_config(path: str | None) -> dict`

Returns `failure_threshold` (int ≥ 1), `success_threshold` (int ≥ 1),
`open_seconds` (float > 0).

- `path is None` → defaults `{failure_threshold: 3, success_threshold: 2, open_seconds: 30.0}`  
- Missing/invalid file → **fail closed**: `{failure_threshold: 1, success_threshold: 10**9, open_seconds: 1e9}`  
  (opens immediately after one failure; almost never closes — safe default for bad config)  
- Valid file: lines `key=value` for the three keys (either order); `#` comments / blanks ok.

### `service.state.BreakerState`

```python
class BreakerState:
    def __init__(self): ...
    # internal: track consecutive failures, consecutive successes in half-open,
    # opened_at timestamp or None, and mode: "closed" | "open" | "half_open"
```

Used only by the breaker; may be a simple class with attributes.

### `service.breaker.CircuitBreaker`

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int, success_threshold: int, open_seconds: float, *, clock=None): ...
    def allow_request(self) -> bool: ...
    def record_success(self) -> None: ...
    def record_failure(self) -> None: ...
    def mode(self) -> str: ...  # closed | open | half_open
    @classmethod
    def from_config(cls, path: str | None = None, *, clock=None) -> "CircuitBreaker": ...
```

### Semantics

- Start **closed**.  
- **closed:** `allow_request` always True. Each `record_failure` increments consecutive failures; at `>= failure_threshold`, transition to **open** and set `opened_at = clock()`. `record_success` resets consecutive failures to 0.  
- **open:** `allow_request` is False until `clock() - opened_at >= open_seconds`, then transition to **half_open** and return True for that probe.  
- **half_open:** allow requests (probes). `record_success` increments consecutive successes; at `>= success_threshold`, go **closed** and reset counters. `record_failure` immediately goes **open** again (reset success streak; set new `opened_at`).  
- `clock` injectable; default `time.monotonic`.  
- `from_config` uses `load_breaker_config`.

## Constraints

Stdlib only; no inventing `hidden_tests/`.

## Done means

Public verify green **and** multi-factor behavior above is correct.
