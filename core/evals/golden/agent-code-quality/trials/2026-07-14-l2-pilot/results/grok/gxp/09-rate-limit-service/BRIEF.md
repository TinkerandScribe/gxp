# GXP brief — 09-rate-limit-service

**Strategy/Model:** session tool-using — multi-file repair with verify loop.

## Goal
Repair the rate-limit package so sliding-window limits, key isolation, and
fail-closed config match the prompt and `.ai/` rules/failures.

## Context (Phase 0)
- `.ai/PROGRAM.md` — verify: `python -m unittest discover -s tests_public -v`
- `.ai/rules/01-stdlib-only.md` — no third-party imports
- `.ai/rules/02-fail-closed-config.md` — bad/missing config → deny
- `.ai/failures/window-off-by-one-and-fail-open.md` — check-then-record,
  per-key store, fail closed, sliding window
- Public tests are weak (green trap) — not sufficient alone

## Ideal State Criteria
- [ ] `allow` check-then-record; never grants more than `max_requests` in window
- [ ] `max_requests == 0` always denies
- [ ] Hits isolated per key
- [ ] Sliding window `(now - W, now]` via `hits_in_window`
- [ ] Missing/invalid config → `max_requests=0` (fail closed)
- [ ] `path is None` → defaults 5 / 60.0
- [ ] Public verify exits 0
- [ ] Stdlib only under `service/`

## Out of scope
Hidden tests, HTTP server, third-party packages, layout rewrite.

## Verification plan
1. Run PROGRAM public unittest.  
2. Manual checks: multi-key, max boundary, missing config deny, clock advance.  
3. Grep service/ for non-stdlib imports.
