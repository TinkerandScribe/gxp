# Task brief

**Date:** 2026-01-18
**Task slug:** fix-login-redirect-loop
**Workflow:** full

> Example brief. Shows a GXP brief for a bug fix — note the criteria pin down the *root
> cause being gone*, not just "it seems to work now."

## Goal

Stop the infinite login→redirect loop that hits users whose session cookie has expired.

## Context

- Related files: `auth/middleware.py`, `auth/session.py`, `tests/test_auth.py`
- Related PRs / tickets: #517 (bug report with repro)
- Relevant `.ai/failures/` entries: none yet — capture one if the cause is non-obvious.
- Background: an expired session cookie is still *present*, so the middleware treats the
  user as "has session," tries to refresh, fails, and redirects to login — which re-reads
  the same stale cookie. The fix must clear the stale cookie before redirecting.

**Strategy/Model:** mid-tier — localized bug, clear repro, needs a regression test.

## Routing

- **privacy_class:** public
- **stakes:** high — auth path; a wrong fix can lock users out.
- **engine_candidates:** [claude-code]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human
- **output_contract:** minimal diff in `auth/` + regression test

## Ideal State Criteria

- [ ] A request with an expired session cookie receives exactly one redirect to `/login`
      (not a loop) — asserted by a test that follows redirects and counts them.
- [ ] After that redirect, the stale session cookie is cleared (`Set-Cookie` with an
      expired/empty value in the response).
- [ ] A request with a valid session is unaffected (still reaches the app, no redirect).
- [ ] A new regression test reproduces the original loop and fails on the pre-fix code.
- [ ] `pytest tests/test_auth.py -q` exits 0.

## Out of scope

- Reworking the session-refresh strategy.
- Changing cookie lifetimes or the login UI.

## Verification plan

1. **Deterministic:** `pytest tests/test_auth.py -q`; confirm the new test fails when
   reverted against the old middleware (proves it catches the real bug).
2. **Behavioral:** manual repro from #517 — expired cookie now lands on `/login` once.
3. **Subjective:** read the diff; confirm it clears the cookie and nothing else.

## Self-evaluation gate

- [x] **Completeness** — fix + cookie-clear + valid-session safety + regression test.
- [x] **Ambiguity** — every criterion is binary.
- [x] **Scope trap** — session-refresh redesign parked.
- [x] **Verification** — each criterion has a concrete check; the regression test is the key one.
- [x] **Approval gates** — high-stakes auth path: pause for human review of the diff before merge.

## Approval gates

- Human review of the `auth/` diff before merge (auth path, lockout risk).

## Dead ends

- (none)

## Handoff notes

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Approval gates hit and outcomes:
- Rating entry reference:
