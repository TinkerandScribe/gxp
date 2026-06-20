---
name: gxp-brief
description: Draft a GXP task brief — binary Ideal State Criteria, verification plan, self-evaluation gate — WITHOUT implementing. Use when the user says "draft a brief for X", "write a gxp brief", "what are the ideal state criteria for X", "draft an isc for X", "scope X gxp-style", "what would a gxp brief look like for X", or "let's spec this out before coding". Stop at presenting the brief; do not write code, do not edit files outside `tasks/`. If the brief reveals the task isn't understood (you can't write 4 strong binary criteria), ask clarifying questions instead of inventing criteria.
---

# GXP Brief Drafting (Phase 1 only)

Draft a GXP task brief for the task in the user's message. **Do not implement.** Present the brief and stop for approval before any code.

## Phase 0 (quick scan)

Before drafting, do a fast Phase 0:

- Skim `core/rules/`, `.ai/rules/`, or `rules/` (whichever exists) for binding rules that apply.
- Skim `core/failures/`, `.ai/failures/`, or `failures/` for known failure modes.
- Read the most relevant code files the user named (or that the task obviously touches).
- Note any test/lint/build commands the project standardizes on (read `PROGRAM.md` if present).

Name any rule or failure entry that applies in the brief's **Context** section.

## Phase 0.5 — Strategy and engine

Pick the least-capable engine that clears the criteria with comfortable margin. Record on a `**Strategy/Model:**` line with a one-line reason.

## Phase 1 — Draft the brief

Fill in `references/task-brief-template.md`. The template sections, briefly:

- **Goal** — one sentence on what success looks like.
- **Context** — related files, rule/failure entries, background needed.
- **Strategy/Model** — chosen engine + one-line reason.
- **Routing** (only when the job may dispatch externally) — privacy class, stakes, candidates, forbidden engines, exec mode, output contract.
- **Ideal State Criteria** — **4 to 8 binary, checkable statements**. Each must be clearly true or false — no weasel words. Prefer concrete checks: not "tests pass" but "`python -m pytest tests/foo -q` exits 0". Not "looks good" but "every public function has a docstring and `ruff check` exits 0".
- **Out of scope** — what you're deliberately not doing.
- **Verification plan** — how each criterion will be checked. Deterministic first.

**If you cannot write 4 strong binary criteria, stop and ask clarifying questions.** Do not invent criteria. State which dimension is unclear (the goal, the verification, the scope, the success bar) and what you need from the user.

## Phase 2 — Self-evaluation gate

Walk these gates and report each one explicitly:

- **Completeness** — does the brief cover the actual goal, or just the surface request?
- **Ambiguity** — every criterion strictly binary?
- **Scope trap** — any cleanup or "while we're here" smuggled in? Move to out-of-scope.
- **Verification** — every criterion has a concrete check?
- **Approval gates** — destructive, irreversible, public-facing, production-touching steps? Name them and mark them as pause points.

If any gate fails, fix the brief and re-walk.

## Save the brief

Write the finished brief to `tasks/<slug>.md` (or `core/tasks/<slug>.md` in a gxp repo). The slug should be the goal turned into kebab-case, max ~50 chars (truncate at a word boundary if longer).

## Hand back to the user

After saving, present:

1. The path to the saved brief.
2. The Ideal State Criteria, numbered.
3. Any approval gates the user will need to clear during implementation.
4. A single explicit question: "Approve this brief and implement (`gxp-workflow`)? Adjust the criteria? Clarify something?"

**Do not start implementing.** This skill ends at the user's approval prompt.

## What this skill is NOT

- Not for implementing — for that, the user invokes the full workflow (`gxp-workflow` skill, or "run gxp on X").
- Not for one-shot Q&A about GXP — for "what is gxp" or "explain the workflow", just answer from `references/workflow.md`.
- Not for trivial edits — lightweight workflow (phases 1, 2, 3, 5) doesn't need a written brief; just talk through it.

## References

- `references/task-brief-template.md` — the brief template.
