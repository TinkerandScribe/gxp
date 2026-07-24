# Design brief — `gxp-refine` (bounded self-refinement mode)

**Date:** 2026-07-23  
**Task slug:** gxp-refine-design  
**Status:** design done — Option A implemented via PRs #3–#5 (see gxp-refine-implement.md)  
**Workflow:** full (this document is the deliverable)  
**Branch convention:** `brief/gxp-refine-design`

## Goal

Define an explicit, **operator-invoked** bounded-refinement mode named **`gxp-refine`**
that applies GXP to GXP itself: inspect accumulated evidence → name one recurring
methodology weakness → form one hypothesis → propose one reversible change to one
named artifact → compare candidate vs pinned baseline under a preregistered eval plan →
**stop for operator approval**. This is bounded self-refinement, **not** open-ended RSI,
unattended self-rewriting, or an always-on auto-orchestrator.

## Context (Phase 0 grounding)

**Exists now (do not invent):**

| Area | Path / fact |
|---|---|
| Canon workflow | `core/workflow.md` (v1.1) — L3/L4 bounded; approval gates; anti-loop; Verification ladder; live ratings placement |
| Weekly refine (manual) | `core/templates/weekly-refine.md` — skim ratings/failures/rules; “one change to try next week” (no eval protocol, no mutation budget) |
| Task brief template | `core/templates/task-brief.md` — Goal, Routing, 4–8 ISC, Out of scope, Verification, Approval gates |
| Routing rails | `core/routing.md` — privacy rail; stakes → verification depth; critic **recommended not shipped**; `exec_mode` auto vs recommend-to-human |
| Ratings | `core/ratings.jsonl` schema line + examples; live-for-fork-work in Phase 6 |
| Job-record schema | `core/templates/job-record.schema.json` — workshop/job fields; **not** a refine-run log |
| Evals | `core/evals/README.md`; golden `agent-code-quality/` PROTOCOL; canaries; regressions; trials **gitignored** / local-only |
| Rules | `core/rules/01-no-secrets-in-git.md`, `02-local-context-never-committed.md` |
| Failures | `core/failures/` + `core/templates/failure-capture.md` |
| Adapters | `adapters/{cursor,grok,claude,chatgpt,perplexity,cowork}/` — Cursor `rule.mdc` hand-authored; claude/chatgpt/grok/perplexity workflows generated from core + deltas |
| Roadmap | `ROADMAP.md` — Part A hardening done; M6 claim gate still closed; **explicitly out:** multi-provider critic product; whole-file workflow allowlists; tag/release automation without operator |
| Contributing / validate | `CONTRIBUTING.md`; `bash scripts/verify.sh` |
| Naming | README: Guided eXecution Protocol ≠ regulated GxP |

**Related but distinct:** weekly refine is a **calendar habit** for humans. `gxp-refine` is a
**named mode** with a mutation budget of 1 and a mandatory baseline-vs-candidate eval —
operator-invoked, never implicit during ordinary Phase 0–8 runs.

**Strategy/Model (this design PR):** documentation-only; no engine routing required.

## Routing (future implementation — not this PR)

When `gxp-refine` is later implemented as an invocable skill/command:

- **privacy_class:** follow the refine target’s sensitivity; default **public** for methodology docs  
- **stakes:** at least **high** when the target is `core/` or `routing.md`; **safety** if weakening gates is conceivable (must fail-closed — see risk ladder)  
- **exec_mode:** **recommend-to-human** for promotion; experiment runs may be `auto` only after operator approves the experiment plan  
- **forbidden:** silent auto-merge; changing evaluator and target in the same run  

## Definition / boundary

1. **Operator-invoked only.** Entering `gxp-refine` requires an explicit operator request
   (e.g. “run gxp-refine” / a dedicated skill). It must **never** start as a side effect of
   an ordinary GXP implement session, weekly calendar skim, or rating append.
2. **No self-selected goals.** The agent does not pick “what to improve next” as an open
   research agenda. It may **propose** a single weakness grounded in evidence; the operator
   approves the experiment before any candidate work proceeds.
3. **Bounded autonomy (L3/L4).** Same as `core/workflow.md`: work inside a written brief;
   pause at named approval gates; do not expand into L5 self-directed rewriting.
4. **Naming.** Mode name is **`gxp-refine` only**. Do not call it `gxp-rsi`, `gxp-auto`,
   or describe unattended self-modification.

## Mutation budget = 1

Exactly one of each per refine run:

| Slot | Constraint |
|---|---|
| Weakness | One recurring methodology weakness, evidenced |
| Hypothesis | One causal/fixability claim about that weakness |
| Logical change | One coherent edit intent (may touch multiple hunks in **one** file only if they serve that single intent — prefer single-file) |
| Target | One named GXP artifact path (see risk ladder) |
| Eval plan | One preregistered primary metric + corpus + baseline pin |

If analysis surfaces multiple weaknesses, **park** the rest; do not batch them.

## Evidence inputs

**Exists now (readable today):**

- `core/ratings.jsonl` (and installed projects’ `.ai/ratings.jsonl` when dogfooding)  
- `core/failures/` and briefs’ Dead ends / Handoff notes under `core/tasks/`  
- `core/evals/` golden PROTOCOL, canaries, regressions docs; **local** trial trees when present  
- Sync / CI signals: `scripts/verify.sh`, adapter `check-core.*`, ROADMAP claim-gate notes  

**Proposed (not in tree yet — future implementation may add):**

- A `gxp-refine` run record (brief + experiment log) under `core/tasks/` or a dedicated
  refine log path — **design only here**; do not invent a new schema in this PR  
- Optional pin of baseline git SHA / release tag for the candidate comparison  

Always label statements in a refine run as **observed** vs **proposed**.

## Target risk ladder (increasing gates)

| Tier | Examples | Gate |
|---|---|---|
| 1 — Adapter surface | `adapters/*/…` non-core copy, Cursor `rule.mdc` compression | Operator experiment approve + promote approve; `verify.sh` / adapter sync |
| 2 — Templates / rules / evals docs | `core/templates/*`, `core/rules/*`, `core/evals/**` docs (not mid-campaign hidden-test edits) | Same + explicit note if eval corpus changes (evaluator independence) |
| 3 — Routing | `core/routing.md` | **stakes ≥ high**; cannot weaken privacy rail or stakes→verification depth |
| 4 — Core methodology | `core/workflow.md` | **stakes ≥ high**; separate promotion approval; cannot weaken approval gates, Verification ladder, anti-loop, or L3/L4 bounded autonomy |

**Hard prohibit (any tier):** changes that weaken approval gates, privacy/stakes rails,
Verification ladder, anti-loop, or bounded-autonomy language — even “temporarily.”

## Evaluator independence

1. **Pinned baseline** — record commit SHA and/or release tag before candidate work.  
2. **Fixed corpus** — name the eval set before the run (e.g. a listed canary script,
   regression doc check, or frozen golden task IDs).  
3. **Preregistered primary metric** — one primary success rule written before candidate
   edits (e.g. process-guarantee scorecard delta, or golden correctness mean with
   pre-registered gap — following patterns in `core/evals/` PROTOCOL / canaries).  
4. **Baseline vs candidate** — run the same corpus on baseline and candidate; report both.  
5. **No dual mutation** — the refine run that changes the **target** must not also change
   the **evaluator** (harness, metric definition, or corpus membership).  
6. **Raw evidence** — keep command outputs / score JSON / notes; do not discard unfavorable
   trials. If the agent/engine is stochastic, require **repeated trials** (N stated in the
   eval plan) before a promote recommendation.

## Capability vs regression

- **Capability set** — optional tasks/metrics allowed to improve under the primary metric.  
- **Regression set** — a named “must not degrade” pack (at minimum: `bash scripts/verify.sh`
  exit 0, and any listed canaries/regressions in the eval plan). Regression set expectation:
  **~100% hold** (no newly failing members). A capability win that breaks the regression set
  is a **reject**, not a promote.

## Approval sequence (fail-closed)

```
analyze evidence
  → propose (weakness + hypothesis + target + eval plan)
  → [GATE 1] operator approves experiment
  → evaluate baseline, then candidate (no promote yet)
  → recommend promote | reject | inconclusive
  → [GATE 2] separate operator promotion approval
  → apply only if GATE 2 passes (future implementation)
```

- **No auto-apply. No auto-merge.**  
- Abort without GATE 1 is success (fail-closed), not a bug.  
- Ordinary GXP runs must not enter this sequence.

## Ideal State Criteria (this design document)

Document-verifiable only — **not** implementation claims.

- [x] 1. The document names the mode **`gxp-refine`** and states it is
      **operator-invoked only** and never implicit during ordinary GXP runs.  
- [x] 2. The document forbids naming/framing as `gxp-rsi`, `gxp-auto`, or unattended
      self-rewriting.  
- [x] 3. The document states a **mutation budget of 1** (one weakness, one hypothesis,
      one logical change, one target, one eval plan).  
- [x] 4. The document separates **exists now** vs **proposed** evidence inputs with
      concrete current-repo paths.  
- [x] 5. The document defines a **target risk ladder** (adapter → templates/rules/evals →
      routing → core) and lists hard prohibits (gates, rails, Verification ladder,
      anti-loop, L3/L4).  
- [x] 6. The document requires **evaluator independence**: pinned baseline, fixed corpus,
      preregistered primary metric, baseline-vs-candidate comparison, no same-run
      evaluator+target change, raw evidence retention, repeated trials if stochastic.  
- [x] 7. The document distinguishes **capability** improvement from **regression-set**
      non-degradation (~100% hold) and ties reject to regression failure.  
- [x] 8. The document specifies a **fail-closed dual approval sequence** (experiment
      approve, then separate promotion approve) with no auto-apply / no auto-merge.

## Out of scope (this PR and the designed mode’s first ship)

- Implementing CLI, skills, adapters, scripts, or harness code for `gxp-refine`.  
- Changing `core/workflow.md`, `core/routing.md`, schemas, ratings format, or generators.  
- Replacing or deleting `core/templates/weekly-refine.md` (complementary, not superseded here).  
- Autonomous promotion, continuous self-rewrite, or always-on “orchestrator” loops.  
- Shipping a multi-provider critic product (ROADMAP explicitly out).  
- Mid-campaign edits to golden `hidden_tests/` to “win” a refine eval.  
- Merging this PR without operator review.

## Verification plan (for this design PR)

1. **Deterministic:** `bash scripts/verify.sh` exits 0 on the branch (no methodology
   files changed — expect same as main).  
2. **Deterministic:** `git diff --name-only origin/main...HEAD` lists **exactly** this file.  
3. **Behavioral / doc walkthrough:** each Ideal State Criterion above has a matching
   explicit section or sentence in this document (reader checklist).  
4. **Subjective (last):** prose is clear enough that an implementer could open a follow-up
   brief without inventing mutation budget or approval gates.

## Approval gates

### This PR (design-only)

- **Gate A:** Operator review of this design brief before merge to `main`.  
- **Gate B:** No implementation work claimed under this PR.

### Future implementation (after this design is accepted)

- **Gate 1 (experiment):** Operator approves weakness + hypothesis + target + eval plan
  before candidate edits.  
- **Gate 2 (promotion):** Separate operator approval after baseline/candidate results;
  required before any merge of the candidate change.  
- **Gate 3 (tier):** Targets in routing/core require elevated stakes language and cannot
  weaken hard prohibits.

## Self-evaluation gate (design authoring)

- [x] Completeness — boundary, budget, evidence, ladder, evaluator, capability/regression,
  approvals covered.  
- [x] Ambiguity — ISC are document-checkable.  
- [x] Scope trap — no second artifact; no code.  
- [x] Verification — verify.sh + single-file diff + doc checklist.  
- [x] Approval gates — named for this PR and future implement.

## Dead ends

- None in design authoring. Parked: whether refine run records reuse task-brief shape
  vs a new template (decide at implementation brief time).

## Handoff notes

- **Artifact:** this file only.  
- **Relation to weekly refine:** weekly refine remains the lightweight human skim;
  `gxp-refine` is the heavier, eval-gated, mutation-budget-1 mode.  
- **Next (operator-gated):** if accepted, open a **separate** implementation brief with
  binary criteria for a thin invocable surface — still no auto-promote.
