# GXP brief — unconstrained contrast
## Goal
Correct circuit breaker multi-factor behavior.
## Ideal State Criteria
- [ ] open after failure_threshold
- [ ] half_open after open_seconds
- [ ] success_threshold closes
- [ ] half_open failure reopens
- [ ] fail-closed config
- [ ] public green
## Out of scope
Hidden tests.
## Verification
Public unittest + criteria.
