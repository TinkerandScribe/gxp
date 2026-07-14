# GXP brief — 09 public-green-vs-gxp

## Goal
Fully repair rate-limit package per prompt + `.ai/` (public tests insufficient).

## Phase 0
- PROGRAM: public unittest weak
- rules: stdlib only; fail-closed config
- failures: check-then-record; per-key; sliding window; no fail-open

## Ideal State Criteria
- [ ] check-then-record; never > max_requests in window
- [ ] max_requests 0 always deny
- [ ] per-key isolation
- [ ] sliding window (now-W, now]
- [ ] missing/invalid config → max_requests 0
- [ ] defaults when path None
- [ ] public verify exit 0
- [ ] stdlib only

## Out of scope
Hidden tests inventing; third-party deps.

## Verification
Public unittest + manual multi-key/config/window checks against criteria.
