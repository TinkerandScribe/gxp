---
name: gxp-failure-capture
description: Capture a repeatable failure in the `failures/` directory so it gets noticed and prevented next time. Use when the user says "capture this failure", "log this as a failure", "add to failures", "write a failure entry", "record this bug for next time", or when a GXP run hits a repeatable failure mode worth remembering (anti-loop trigger, surprising bug, footgun the next contributor would also hit). Fills in Expected / Actual / Root cause / Detection / Resolution / Prevention / Follow-up.
---

# GXP Failure Capture (Phase 7)

Write a failure entry to `failures/<slug>.md` (or `core/failures/<slug>.md` in a gxp repo). The goal is **not** to log every bug — only patterns worth remembering.

## When to capture

- A repeatable failure: future contributors (human or agent) would plausibly hit this again.
- An anti-loop trigger from Phase 4 — same approach failed twice, you switched strategy. The dead end is the lesson.
- A surprising bug whose detection is non-obvious. The future signal matters.
- A footgun in the codebase or environment (CRLF normalization, stale mock targets, ENAMETOOLONG on long-string paths, etc.).

**Do not** capture: one-off typos, a passing failing test you fixed in the same session with no lesson, anything that's already in `failures/`.

## Gather the inputs

Walk the user (or your own context) through each section before writing:

- **Expected** — what should have happened. Concrete: exact output, exit code, behavior, or invariant.
- **Actual** — what did happen. Error message, unexpected output, divergent behavior. Paste relevant log lines verbatim.
- **Root cause** — why, in one or two sentences. If you don't know, **say so** (a labeled guess is fine). Distinguish proximate ("the regex didn't match") from underlying ("input format changed upstream").
- **Detection** — the signal a future contributor can use to notice this is happening again: a log line, a failing test, a smell in a diff, a specific symptom.
- **Resolution** — the change that fixed it this time. Files touched, commit/PR if applicable.
- **Prevention** — the durable change in behavior or process that stops recurrence. Order of preference:
  1. A new test (preferred — converts the failure into a checked invariant).
  2. A doc update (when the behavior is non-obvious but can't be tested cheaply).
  3. A rule in `rules/` (when the lesson generalizes to many tasks).
- **Follow-up** — concrete next action. Link to the test PR, doc PR, or rule that prevents recurrence.

## Filename

Use a short kebab-case slug that names the failure mode, not the task that hit it. Good:

- `crlf-phantom-diff-on-windows-checkout.md`
- `stale-mock-target-after-refactor.md`
- `enametoolong-on-path-exists-with-long-string.md`

Bad: `bug-from-last-tuesday.md`, `pytest-failure.md`.

## Write the file

Copy `references/failure-capture-template.md` and fill it in. Stamp the date. Reference the brief that hit it (`Task / context:`).

## After writing

- Show the user the path and the first ~10 lines of the entry.
- Suggest the prevention step concretely: "I'd recommend adding a test at `tests/test_xyz.py::test_no_phantom_diff` that asserts `git diff --ignore-cr-at-eol` is empty after a fresh checkout. Want me to draft it?"
- If a `rules/` rule would generalize the lesson, propose it as a follow-up.

## What this skill is NOT

- Not a substitute for fixing the bug. Failure capture is **in addition to** the fix, not instead.
- Not a place to dump every error log. Only patterns worth a future read.
- Not for venting. Stay neutral — the next reader (often Claude) needs the facts.

## Reference

- `references/failure-capture-template.md` — the templ