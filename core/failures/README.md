# Failures

Captured patterns of things that went wrong and how to avoid them next time.

Use `../templates/failure-capture.md` as the starting point. One failure per
file. Filename should describe the symptom (`flaky-clock-in-tests.md`,
`silent-truncation-on-import.md`).

A failure entry is worth keeping only if it is **repeatable** — something a
future contributor could plausibly hit again. One-off mistakes don't belong
here.

During weekly refine, prune entries that no longer apply and promote durable
ones into `../rules/`.
