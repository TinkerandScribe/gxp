---
name: gxp-workflow
description: Run the full GXP verification-first workflow on a non-trivial task. Use when the user says "run gxp on X", "use gxp methodology", "use the gxp workflow", "verification-first on X", "apply gxp discipline", "do this gxp-style", or when a task changes behavior, touches multiple files, or could plausibly regress something. Also use as the default discipline for any non-trivial coding, configuration, or analysis task in a repo that has a `core/workflow.md`, `.ai/PROGRAM.md`, `rules/`, or `ratings.jsonl` — those are GXP repos. Walks Phases 0–8: repo audit, strategy/model, task brief with 4–8 binary Ideal State Criteria, self-evaluation gate, smallest viable implementation, anti-loop rule (stop after two failed attempts), verification (deterministic→behavioral→subjective), honest rating to `ratings.jsonl`, failure capture, handoff. Pause at every approval gate. Do NOT use for trivial single-file reversible edits (typo, one-liner) — those use lightweight (phases 1, 2, 3, 5) and don't need this skill.
---

# GXP Workflow (full)

Run the full GXP loop on the task in the user's message. You are an **L3/L4 bounded agent**: work within the brief, do not self-direct, do not expand scope, pause at approval gates.

## Decide variant first

- **Full** (phases 0–8, this skill's default) — task changes behavior, touches multiple files, or could plausibly regress something. Default when in doubt.
- **Lightweight** (phases 1, 2, 3, 5) — only for trivial single-file easily-reversible edits (typo, comment, one-liner). If you start lightweight and discover the task is bigger, upgrade to full.

State the variant choice in one line before Phase 0.

## Phase 0 — Repo audit

Scan for context **before** writing or proposing anything. Look for and read (whichever exist in the current working folder):

- `core/PROGRAM.template.md` or a filled `PROGRAM.md` — project context and verification commands
- `core/rules/` or `.ai/rules/` or `rules/` — binding rules for this repo
- `core/failures/` or `.ai/failures/` or `failures/` — known repeatable failure modes
- `core/ratings.jsonl` or `ratings.jsonl` — recent ratings for patterns
- `CLAUDE.md` or `AGENTS.md` at the repo root — repo-specific instructions

If any rule or failure entry plausibly applies, **name it explicitly** in the brief. Output of Phase 0 is a short paragraph naming the constraints that apply.

## Phase 0.5 — Strategy and engine selection

Classify the task on: complexity/scope, risk/reversibility, domain knowledge required, iteration tolerance, and the margin the chosen engine must clear the criteria by. Pick the **least-capable engine** that clears the criteria with comfortable margin — conserves context budget, reduces cost/latency, keeps the agent in its reliable band.

Record the choice on a `**Strategy/Model:**` line in the brief with a one-line rationale.

If the job may leave the current tool (privacy class, stakes, cost, or location), also read `core/routing.md` if present and fill the **Routing** block in the brief.

Re-evaluate at the Phase 4 anti-loop gate if the chosen engine is failing to make progress.

## Phase 1 — Task brief

Copy `references/task-brief-template.md` (from this skill's references — or use the repo's `core/templates/task-brief.md` if present) and fill in:

- **Goal** — one sentence on what success looks like.
- **Context** — related files, prior PRs/tickets, anything surfaced in Phase 0, any rule/failure entry that applies.
- **Strategy/Model** — chosen engine + one-line reason (from Phase 0.5).
- **Routing** (only if job may dispatch externally) — privacy_class, stakes, engine_candidates, forbidden_engines, exec_mode, output_contract.
- **Ideal State Criteria** — **4 to 8 binary, checkable statements** that will all be true when the task is done. Each must be clearly true or false — no weasel words. Prefer concrete checks: not "tests pass" but "`python -m pytest tests/foo -q` exits 0".
- **Out of scope** — what you're deliberately not doing.
- **Verification plan** — how each criterion will be checked. Deterministic checks first.

**If you cannot write 4 strong binary criteria, stop and ask the user clarifying questions. Do not invent criteria.**

Save the brief at `tasks/<slug>.md` (or `core/tasks/<slug>.md` in a gxp repo).

## Phase 2 — Self-evaluation gate

Walk these gates explicitly. Each must pass before any code is written:

- **Completeness** — does the brief cover the actual goal, or just the surface request? Anything load-bearing missing?
- **Ambiguity** — every criterion strictly binary? Rewrite or drop weasel words.
- **Scope trap** — any cleanup, refactor, or "while we're here" items that aren't strictly required? Move to out-of-scope.
- **Verification** — every criterion has a concrete check? If a criterion can only be confirmed by eyeballing, state how and accept the lower confidence.
- **Approval gates** — destructive, irreversible, public-facing, or production-touching steps? Name each one in the brief and **stop at each until the user approves**.

If any gate fails, fix the brief and re-walk the gates.

## Phase 3 — Implementation

Make the change. Hard constraints:

- Diff stays focused on the brief. Anything outside goes to a follow-up list.
- Smallest viable change. No opportunistic refactor.
- Follow conventions surfaced in Phase 0.
- No new dependencies, abstractions, or files unless the brief calls for them.
- Non-obvious decisions get a one-line note somewhere durable (commit message, brief, comment) — not just chat.

## Phase 4 — Anti-loop rule

If the same approach fails twice — same test failing for the same reason, same lint error reappearing after a fix attempt, same build break — **stop**. Do not try the same shape of fix a third time.

- Write down the dead end in the brief's **Dead ends** section: what you tried, why it failed, what you now believe is true.
- Switch strategy: re-read the failing output, change the hypothesis, ask the user if the brief itself is wrong, or re-evaluate the Phase 0.5 engine choice.
- Persistent dead ends become `failures/` entries at handoff time (Phase 7).

This rule is the single most important defense against the most expensive failure mode: grinding on a broken approach.

## Phase 5 — Verification

Walk through each Ideal State Criterion and confirm it is met. **Run in this order:**

1. **Deterministic checks first** — type checking, linting, unit tests, build, schema validation. Cheap, unambiguous. Run them before anything subjective.
2. **Behavioral checks** — run the actual feature, follow the golden path, hit edge cases named in the brief.
3. **Subjective checks** — code quality, UX, anything that needs judgment. Only after deterministic and behavioral pass.

If a criterion can't be checked mechanically, state how you confirmed it and accept the lower confidence.

Report results criterion-by-criterion ("Criterion 1: PASS — `pytest` exit code 0; 189 collected, 186 passed, 2 skipped, 1 failed in `test_llm_router` (pre-existing, not caused by this change)"). Do **not** report aggregate "all passed" when some failed.

## Phase 6 — Rate

Append **one JSON object per line** to `ratings.jsonl` (or `core/ratings.jsonl` in a gxp repo). Required fields:

```json
{"ts": "2026-06-19T22:00:00Z", "task": "<slug>", "brief": "tasks/<slug>.md", "criteria_met": 6, "criteria_total": 7, "rating": 8, "mode": "full", "notes": "<honest one-line summary>", "failure_ref": ""}
```

- `rating` is an integer 1–10. **Be honest.** A low rating on a real run is more useful than a generous one. If criteria slipped, the rating drops. Do not stamp a flat 8 on every run.
- `mode` is `full` or `lightweight`.
- `failure_ref` is the path under `failures/` if a failure was captured this run; otherwise empty string.
- **Never** wrap multiple runs in one line. **Never** use a JSON array.

See `references/ratings-schema.md` for the full schema.

## Phase 7 — Failure capture

If a repeatable failure showed up — something that would trip you (or a future contributor) again — copy `references/failure-capture-template.md` (or `core/templates/failure-capture.md` in a gxp repo) into `failures/<slug>.md`. Fill in: Expected, Actual, Root cause, Detection, Resolution, Prevention, Follow-up.

Goal is not to log every bug — only patterns worth remembering.

## Phase 8 — Handoff

Before declaring done, summarize:

- **What changed** — files, key decisions.
- **What was verified** — which criteria, how (deterministic / behavioral / subjective).
- **Explicitly not done / parked / follow-ups** — anything pushed out of scope.
- **Approval gates hit** — and the outcome at each.
- **Dead ends** — from Phase 4 worth remembering.
- **Rating reference** — pointer to the `ratings.jsonl` line just appended.
- **New `failures/` entry** — if any.

Optimize the handoff for the next reader (human or agent), not for completeness.

## Output style

- Run the phases in order. Announce each phase with a `## Phase N — <name>` heading in your response so the user can follow along.
- For Phases 1 and 6, **write the files** (`tasks/<slug>.md`, `ratings.jsonl` append). Don't just describe them in chat.
- Stop and wait for user input at each approval gate named in Phase 2.
- Match the rigor to the variant: lightweight skips Phases 0, 4, 6, 7, 8 unless something surfaces.

## What this skill is NOT

- Not a substitute for actually understanding the task. If the user's request is ambiguous, Phase 1 asks clarifying questions instead of inventing binary criteria.
- Not a way to make a run look successful. The rating, the success report, the criteria walk-through must all be honest.
- Not for trivial edits. Lightweight (phases 1, 2, 3, 5) is the right tool for a typo or one-liner.

## References

- `references/workflow.md` — the canonical GXP workflow (v1.1) text in full.
- `references/task-brief-template.md` — the brief template to copy in Phase 1.
- `references/failure-capture-template.md` — the failure-capture template for Phase 7.
- `references/ratings-schema.md` — the `ratings.jsonl` line schema for Phase 6.
- `references/rules-summary.md` — the default repo rules that ship with GXP.
