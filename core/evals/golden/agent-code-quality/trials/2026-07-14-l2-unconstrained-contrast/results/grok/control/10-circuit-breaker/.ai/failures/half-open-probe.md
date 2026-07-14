# Failure: half-open and open timer bugs

**Symptoms:** breaker never opens; or stays open forever; or half-open success
does not require `success_threshold` probes.

**Fixes:** count consecutive failures only in closed; open until `open_seconds`
elapses then half_open; half_open needs `success_threshold` successes; any
failure in half_open re-opens.
