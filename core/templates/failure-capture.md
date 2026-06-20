# Failure capture

**Date:**
**Task / context:**

## Expected

What should have happened. Be concrete — exact output, exit code,
behavior, or invariant.

## Actual

What did happen. Error message, unexpected output, behavior that
diverged from intent. Paste the relevant log lines verbatim.

## Root cause

Why it happened, in one or two sentences. If you do not actually know,
say so; a guess labeled as such is fine. Distinguish proximate cause
("the regex didn't match") from underlying cause ("input format changed
upstream").

## Detection

A signal a future contributor (or AI agent) can use to notice this is
happening again: a log line, a failing test, a smell in a diff, a
specific symptom.

## Resolution

The change that fixed it this time. File(s) touched, commit/PR if
applicable.

## Prevention

The durable change in behavior or process that stops recurrence:

- a new test (preferred — converts the failure into a checked invariant)
- a doc update (when behavior is non-obvious but cannot be tested cheaply)
- a rule in `../rules/` (when the lesson generalizes to many tasks)

## Follow-up

The concrete next action and its status. Examples:

- [ ] Add regression test in `tests/...`
- [ ] Add rule to `.ai/rules/...`
- [ ] Update `.ai/PROGRAM.md` section X
- [ ] Open issue / PR: link

## Repeatable?

Yes / no. Only keep this file if yes. If the follow-up converts this
into a test or rule, this file can be deleted at the next weekly
refine.
