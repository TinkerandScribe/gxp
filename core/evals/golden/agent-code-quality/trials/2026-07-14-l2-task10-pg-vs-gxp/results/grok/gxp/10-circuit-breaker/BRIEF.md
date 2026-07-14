# GXP brief — circuit breaker
## Goal
Full multi-factor circuit breaker fix.
## Ideal State Criteria
- [ ] open after failure_threshold
- [ ] half_open after open_seconds
- [ ] success_threshold to close
- [ ] half_open failure reopens
- [ ] fail-closed config
- [ ] public green
## Out of scope
Hidden tests.
## Verification
Public unittest + criteria walkthrough.
