# Failures

Captured patterns of things that went wrong and how to avoid them next time.

Use `../templates/failure-capture.md` as the starting point. One failure per
file. Filename should describe the symptom (`flaky-clock-in-tests.md`,
`silent-truncation-on-import.md`).

A failure entry is worth keeping only if it is **repeatable** — something a
future contributor could plausibly hit again. One-off mistakes don't belong
here.

## Regression check

A repeatable failure capture must name or link a matching regression
check: a path a future run can open and follow. Use
`core/evals/regressions/<slug>.md` in this repo, or `regressions/<slug>.md`
beside the capture in a fleet store. The check may be a documented
procedure or a stub that names the future command. A repeatable capture
with no regression path is incomplete. See `fleet/README.md` for the
store layout. Example pairing:
`verification-wrapper-swallows-exit-codes.md` →
`core/evals/regressions/verification-wrapper-must-fail-on-drift.md`.

During weekly refine, prune entries that no longer apply and promote durable
ones into `../rules/`.
