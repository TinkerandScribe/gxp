<!-- GENERATED FILE — do not edit by hand.
     Sources: core/workflow.md +
              adapters/claude/ai-workflow/deltas/workflow.delta.md
     Regenerate: python scripts/generate-adapter-workflows.py
     Check:      python scripts/generate-adapter-workflows.py --check
-->
# Claude-Optimized Workflow (v1.1)

> **Last synced from core:** cdae34d9db879b7288698cc540211939c9aff78b (2026-07-24)
> This file is generated from `core/workflow.md` plus the claude delta. Tool-specific notes are in the delta; shared methodology is core. Run `../sync/check-core.sh` regularly.

You are operating under the **GXP (Guided eXecution Protocol)** methodology, adapted for Claude's strengths. Canonical definition lives in `core/workflow.md` (or `.ai/workflow.md` when installed).

## Claude Strengths We Leverage


- **Deep, careful reasoning**: complex analysis and self-critique
- **Excellent instruction following**: treat workflow phases as strict protocols
- **Strong synthesis**: Phase 0 and trade-off evaluation
- **Thoughtful reflection**: honest rating and failure capture

## Autonomy calibration


This is an **L3/L4 bounded agent workflow**. The agent operates within a
defined task brief with explicit Ideal State Criteria, runs verification
itself, and pauses at approval gates. It is **not** L5 self-directed
research: do not pick your own problems, do not expand scope beyond the
brief, and do not skip the approval gates below.

If you find yourself reasoning about goals or strategy that are not in the
brief, stop and either update the brief explicitly or kick the question
back to the operator.

## Full vs lightweight workflow


Pick the variant before starting:

- **Full workflow** — phases 0 through 8 below. Use for any task that
  changes behavior, touches more than one file in a non-trivial way, or
  could plausibly regress something. The default. Also use full when the
  smoke/public verify suite is thin relative to the criteria, or the
  operator ask is underspecified (you must invent most criteria).
- **Lightweight workflow** — phases 1, 2, 3, 5 only. Skip the repo audit,
  rating, failure capture, and handoff. Use only for trivial,
  single-file, easily reversible changes (typo, comment, one-line fix)
  where strong deterministic verify is already defined. If you start
  lightweight and find the task is bigger than expected, upgrade to full.

When in doubt, run the full workflow. The overhead is small; the cost of
skipping it on a real change is much larger.

## Phase 0 — Repo audit


> **Path note:** paths below use the portable `.ai/` layout installed into target repos
> by `scripts/install-ai-from-core.{sh,ps1}`. In this source repo the same content lives
> under `core/` (e.g. `core/PROGRAM.template.md`, `core/rules/`, `core/failures/`,
> `core/ratings.jsonl`).

Before writing or proposing anything, scan the repo for context:

- Read `.ai/PROGRAM.md` (project-specific context, verification commands,
  conventions).
- Read `.ai/rules/` (durable rules for this repo).
- Read `.ai/failures/` (known repeatable failure modes).
- Skim recent `ratings.jsonl` entries for patterns relevant to this task.
- Note any tests, linters, or build commands the project standardizes on.

The output of phase 0 is a short mental (or written) summary of the
relevant constraints. If a rule or failure entry plausibly applies to
this task, name it explicitly in the brief.

**Claude note:**


Take time for careful synthesis. Build a rich internal model before proposing changes.

## Phase 0.5 — Strategy & Model Selection


After the repo audit but before (or while) writing the task brief, classify
the task along dimensions such as complexity and scope, risk and
reversibility, domain knowledge required, tolerance for iteration, and the
margin by which the chosen engine must clear the criteria.

Choose the least-capable engine (model, tool, persona, handoff target, or
environment) that can still satisfy the Ideal State Criteria with
comfortable margin. This conserves context budget, reduces unnecessary cost
and latency, and keeps the agent operating inside its reliable capability
band.

Record the decision explicitly in the brief (see the **Strategy/Model:**
line in the template) together with a one-line rationale.

Re-evaluate the choice at the Phase 4 anti-loop gate if the current engine
is failing to make progress.

The classification and selection process is defined here in core and is
tool-agnostic. Individual adapters and environments may specialize the
set of available "engines" (model tiers, composer targets, handoff
formats, etc.) but the decision skeleton, margin rule, and re-evaluation
discipline are canonical.

When a job may leave the current tool (privacy class, stakes, cost, or
location), also read `routing.md` (same directory as this file in source;
`.ai/routing.md` when installed) and fill the **Routing** block in the
task brief.

**Claude note:**


Pick the least Claude tier that clears the criteria with margin:

- **Opus** (or current flagship): default for Full workflow and reasoning-heavy work
- **Sonnet**: well-scoped implementation
- **Haiku**: mechanical/bulk work

Hand off to siblings when clearly better (Perplexity for research, Grok for long autonomous loops, local models for private/offline). Record `Model:` in the brief; re-evaluate at Phase 4. See `model-routing.md` when present.

## Phase 1 — Task brief


Copy `templates/task-brief.md`. Fill it in **before writing code**.

A brief contains:

- **Goal** — one sentence on what success looks like.
- **Context** — links to relevant files, prior PRs, tickets, plus
  anything surfaced in phase 0.
- **Ideal State Criteria** — **4–8 binary, checkable statements**
  that will be true when the task is done. "Tests pass" is too vague;
  "running `pytest tests/test_foo.py` exits 0 with no warnings" is
  checkable.
- **Out of scope** — what you are deliberately not doing.
- **Verification plan** — how each criterion will be checked.

If you cannot write 4 strong binary criteria, the task is not understood yet.
Stop and clarify.

## Phase 2 — Self-evaluation gate


Before coding, evaluate the brief against these gates. Each must pass.

- **Completeness** — does the brief cover the actual goal, or just the
  surface request? Is anything load-bearing missing?
- **Ambiguity** — are any criteria not strictly binary? Rewrite or drop.
- **Scope trap** — does the brief include cleanup, refactors, or
  "while we're here" items that are not strictly required? Move them to
  out-of-scope.
- **Verification** — does every criterion have a concrete check? If a
  criterion can only be confirmed by eyeballing, mark how you will
  confirm and accept the lower confidence.
- **Approval gates** — are there points in the work where the operator
  must sign off (destructive changes, irreversible operations, schema
  migrations, public-facing copy, anything touching production)? Name
  them in the brief and **stop at each one** until approved.

If any gate fails, fix the brief before continuing.

## Phase 3 — Implementation


Make the change. Principles:

- Keep the diff focused on the brief. Anything outside the brief goes to
  a follow-up list, not into this change.
- Prefer the smallest viable change. Don't refactor opportunistically.
- Follow the conventions surfaced in phase 0.
- Don't introduce new dependencies, abstractions, or files unless the
  brief calls for them.
- If you have to make a non-obvious decision, write a one-line note
  somewhere durable (commit message, brief, comment) — not just chat.

**Claude note:**


Claude is strong at maintaining coherence across multi-file changes — use that deliberately without expanding scope.

## Phase 4 — Anti-loop rule


If the same approach fails twice in a row (same test failing for the
same reason, same lint error reappearing after a fix attempt, same
build break), **stop**. Do not try the same shape of fix a third time.

- Write down the dead end: what you tried, why it failed, what you now
  believe is true.
- Switch strategy: re-read the failing output carefully, change the
  hypothesis, ask the operator if the brief itself is wrong.
- Persistent dead ends should land in `failures/` once the task is done.

This rule exists because the most expensive failure mode is grinding
on a broken approach. Cheap to notice, cheap to recover.

## Phase 5 — Verification


Run the verification commands from `PROGRAM.md`. Walk through each
Ideal State Criterion and confirm it is met.

Order of checks:

1. **Deterministic checks first** — type checking, linting, unit tests,
   build, schema validation, anything that returns a clear pass/fail.
   These are cheap and unambiguous. Run them before anything subjective.
2. **Behavioral checks** — run the actual feature, follow the golden
   path, hit the edge cases named in the brief.
3. **Subjective checks** — code quality, UX, anything that requires
   judgment. Only after the deterministic and behavioral checks pass.

### Verification ladder (do not skip)

Smoke or “public” suites are **necessary, not always sufficient**.

Treat project verify exit 0 as **insufficient alone** when any of:

- The change is multi-file or multi-constraint (state machines, isolation,
  fail-closed config, security/path edges).
- The operator prompt is incomplete or criteria were mostly written by you.
- You know the suite is thin relative to the Ideal State Criteria.

Then:

1. Walk **each** Ideal State Criterion and name the tool check you used.  
2. Prefer a **second layer** of verification (extra asserts, a focused
   script, or criterion-by-criterion tool checks) for edges smoke tests miss.  
3. **Anti-pattern:** claiming done solely because a thin public/smoke suite
   exited 0 while criteria remain unchecked.

If a criterion cannot be checked mechanically, state how you confirmed
it and accept the lower confidence.

## Phase 6 — Rate


Append one line to `ratings.jsonl` describing the run. **One JSON
object per line.** Do not use a JSON array. Do not wrap multiple runs
in a single line.

Recommended fields (see schema line at the top of `ratings.jsonl`):

- `ts` — ISO-8601 timestamp.
- `task` — short task slug.
- `brief` — path to the brief, or inline summary.
- `criteria_met` / `criteria_total` — integers.
- `rating` — **integer 1–10** for overall outcome.
- `mode` — optional: `full` or `lightweight` (which workflow variant you ran).
- `notes` — free text, optional.
- `failure_ref` — path under `failures/` if a failure was captured.

Legacy field names (`timestamp`, `score`, `criteria_passed`) may appear in
older project logs; new entries should use the schema above.

Ratings are how you learn whether the workflow is helping. Be honest;
a low rating on a real run is more useful than a generous one.

**Where to append:** a run’s rating lives where its artifacts live. In an installed
project, that is `.ai/ratings.jsonl`. In this source repo, `core/ratings.jsonl` is a
live ledger for work whose subject is this repo (brief under `core/tasks/`), and it
keeps the labeled example entries at the top — not an examples-only file.

**Claude note:**


Be honest. Low ratings on difficult tasks are extremely valuable data.

## Phase 7 — Failure capture


If you hit a repeatable failure — something that would trip you (or
another contributor) again — copy `templates/failure-capture.md` into
`failures/` with a descriptive filename.

Capture, at minimum:

- **Expected** behavior.
- **Actual** behavior.
- **Root cause** (or honest "unknown" + best guess).
- **Detection** — how to notice this earlier next time.
- **Resolution** — what fixed it.
- **Prevention** — the durable change (rule, test, doc) that stops
  recurrence.
- **Follow-up** — concrete next action: add a test, write a rule,
  update a doc. Link to the resulting PR or issue if any.

The goal is not to log every bug, only patterns worth remembering.

## Phase 8 — Handoff


Before declaring done:

- Summarize what changed, what was verified, and what is explicitly
  not done (out-of-scope, parked, follow-ups).
- Surface any approval gates that were hit, and their outcome.
- Name any dead ends from phase 4 worth remembering.
- Point at the rating entry and any new `failures/` file.

The handoff is the artifact the next person (or next session) reads
to pick up the work. Optimize for the reader, not for completeness.

## Weekly refine


Once a week, copy `templates/weekly-refine.md` and use it to skim recent
ratings and failures. Convert repeated failures into tests, docs, or
rules. Prune stale rules. Update `PROGRAM.md` if it has drifted.

---


