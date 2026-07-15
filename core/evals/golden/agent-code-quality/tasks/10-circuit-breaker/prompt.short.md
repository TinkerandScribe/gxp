# Task: repair circuit breaker (underspecified)

## Deliverable

Fix the broken `service/` package so the circuit breaker works correctly.
Use tools. Stdlib only. Public verify:

```bash
python -m unittest discover -s tests_public -v
```

## Hints

There is a `CircuitBreaker` with `allow_request`, `record_success`, `record_failure`,
`mode`, and `from_config`. Config loading may be wrong. State transitions matter.

(Full edge-case rules are intentionally **not** listed here. Inspect the workspace.)
