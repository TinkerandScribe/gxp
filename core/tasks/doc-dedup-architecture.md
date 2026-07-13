# Task brief — doc dedup architecture (ROADMAP P2-4)

**Date:** 2026-07-13  
**Task slug:** doc-dedup-architecture  
**Workflow:** full (this session: plan + brief only)  
**Status:** **awaiting operator approval** — do not migrate without sign-off  

## Goal

Design (not implement) how GXP collapses duplicated methodology prose across
`core/workflow.md` and the adapter restatements, while **keeping** the structural
floor, live sync markers, CI negative-drift test, and tool-specific adapter value.

## Context (Phase 0)

| Source | Finding |
|---|---|
| `ROADMAP.md` | P2-4 deferred until M1 made deltas verifiable; floor now exists. Option B (build-time generation) named as candidate end-state. |
| `core/workflow.md` | ~256 lines; canonical Phases 0–8 + autonomy + ratings schema. |
| Adapter workflows | chatgpt ~162, claude ~161, grok ~142, perplexity ~163 lines; cursor uses `rule.mdc` ~167 with Phase -1 capability gate. |
| Structural floor | claude/chatgpt/grok `check-core`: Phases 0–8, 4–8 criteria, anti-loop, deterministic-first, ratings fields `ts`/`criteria_met`/`criteria_total`/`rating`. Must keep passing. |
| `update-sync-markers.sh` | Rewrites `> **Last synced from core:**` lines in adapter `instructions/workflow.md` (and perplexity). Generated files must keep a stable marker line location. |
| CI negative test | Deletes Phase 8 from **claude** workflow text; expects `verify.sh` fail. Thinning must not remove Phase 8 detectability. |
| `adapters/cowork/build.sh` | **Option B in miniature:** `plugin-src/` holds adapter-only content; build copies `core/workflow.md` + templates + rules into `references/`. No full workflow rewrite checked into git under plugin-src. |
| `real-diff-sync-checks.md` | Option B (generation) was out of scope for P0-2; now appropriate as architecture choice for P2-4. |

### What is duplicated today

- Phase loop narrative (0–8) restated per adapter with small wording deltas.  
- Autonomy / L3–L4 calibration repeated.  
- Ratings field guidance partially repeated (now required by floor).  
- Tool-specific content is real value: Grok strategy/personas, Claude model tiers,
  ChatGPT Knowledge notes, Perplexity research phases, Cursor Phase -1 connectors.

### What must never be “deduped away”

- Structural floor markers (or equivalent generated text that still matches them).  
- Live sync marker line format and path set used by `update-sync-markers.sh`.  
- Cursor capability gate and install-path dual-mode notes.  
- Cowork’s build-time core copy model (already correct for packaging).

---

## Architecture decision (recommendation)

### Recommended: **Hybrid — core is canonical; adapters become delta + thin shell**

**Not** pure full-file generation of every adapter workflow in v1 (too much risk for
Cursor `rule.mdc` shape and Perplexity research rewrite). **Not** pure hand-thinning
without a generator for the shared phase skeleton (drift returns).

| Layer | Owner | In git? |
|---|---|---|
| Canonical methodology | `core/workflow.md` | yes |
| Shared phase skeleton (optional extract) | e.g. `core/docs/workflow-phase-skeleton.md` **or** sections marked in core | yes |
| Adapter **delta** | `adapters/<tool>/ai-workflow/deltas/workflow.delta.md` (tool strengths, routing, path notes only) | yes |
| Adapter **published** workflow | `instructions/workflow.md` | **generated** for claude/chatgpt/grok/perplexity **or** hand-maintained thin file that `#include`s core by convention for agents that can read multi-file |
| Cursor | Keep `rule.mdc` hand-authored compressed form; floor-style structural check already exists | yes (not full core dump) |
| Cowork | Keep build-time `cp core → references/` | yes |

### Option comparison

| Approach | Pros | Cons | Verdict |
|---|---|---|---|
| **A. Hand-thinned adapters only** | Small PR; no generator | Drift returns; every core edit needs N ports | Reject as end-state |
| **B. Full generate from core + delta (cowork-like)** | Single edit surface; CI can regen | Generator bugs; Cursor/rule.mdc awkward; marker rewrite must run post-gen | **End-state for text adapters** |
| **C. Hybrid (recommended)** | Ship generator for claude/chatgpt/grok/perplexity first; leave cursor/cowork patterns | Two maintenance modes temporarily | **Adopt** |

### What each adapter keeps as genuine delta

| Adapter | Keep in delta (examples) |
|---|---|
| Grok | Tool-use aggression, strategy-selection / personas, Grok Build notes |
| Claude | Model tier guidance (Opus/Sonnet/Haiku), careful synthesis notes |
| ChatGPT | Knowledge files, non-repo verification honesty |
| Perplexity | Research-first phases, handoff-to-coding-agent framing |
| Cursor | Phase -1 capability gate, dual `.ai` vs `core/` paths, Composer notes — **stay in rule.mdc** |
| Cowork | Skill packaging; core pulled at build — **no second workflow novel** |

### Migration order (implementation session — not this brief)

1. Spec generator input/output + golden “expected thin workflow” for **one** adapter (grok).  
2. Implement `scripts/generate-adapter-workflows.sh` (or `.py`) + `--check` mode for CI.  
3. Generate grok → structural floor + verify.sh + marker update.  
4. Roll claude, chatgpt, perplexity.  
5. Document “edit core + delta, never hand-edit generated body”.  
6. Optional later: cursor remains structural-only; do not force full core into rule.mdc.

### Interaction with markers and CI

| Mechanism | Interaction |
|---|---|
| `update-sync-markers.sh` | Must run **after** generation (or generator emits placeholder marker line that update script rewrites). CI bump job already commits marker-only diffs — keep that. |
| CI negative-drift | Keep sabotaging **claude** published `instructions/workflow.md` (generated or not). Generator must not re-run mid-negative-test step. Current workflow order is fine: verify → negative mutate live file → restore. |
| Structural floor | Generator output **must** include Phase 0–8 headings and required tokens; add a unit test that generated fixture passes `check_workflow_structure` markers. |
| Whole-file allowlist | **Never** reintroduce “Workflow Definition” whole-file ALLOW. |

---

## Ideal State Criteria (for the **implementation** of P2-4 — not met in this planning session)

- [ ] 1. A documented generator (or explicit “no generator” rejection with rationale) lives under `scripts/` with `--check` that fails if published adapter workflows drift from generation inputs.  
- [ ] 2. For each of claude/chatgpt/grok/perplexity: tool-specific content lives only in a delta file (or clearly marked non-generated section); shared phase prose is not copy-pasted by hand.  
- [ ] 3. `bash scripts/verify.sh` exits 0 on clean tree after migration.  
- [ ] 4. Structural floor still fails when Phase 8 is deleted from claude published workflow (local + CI negative test).  
- [ ] 5. `bash scripts/update-sync-markers.sh` still rewrites the standard bold marker line in all four workflow paths.  
- [ ] 6. Cursor `rule.mdc` and cowork build model remain green without forcing them onto the same generator.  
- [ ] 7. ROADMAP P2-4 marked done with link to generator + delta layout.  
- [ ] 8. No whole-file workflow allowlist returns.

## Out of scope (this brief / first implementation)

- Actually running the full migration without operator approval.  
- Rewriting Cursor rule into full core.  
- Changing structural floor markers.  
- Doc dedup of README / adapter READMEs (optional follow-up).

## Verification plan (implementation session)

1. Generator `--check` fails if someone hand-edits generated body.  
2. verify.sh 0; Phase 8 delete → non-zero; restore → 0.  
3. update-sync-markers no-op when current; changes SHA when core tip moves.  
4. Spot-read each delta for tool-specific-only content.

## Approval gate

**STOP.** Present this architecture for operator decision:

1. **Approve Hybrid (recommended)** → next session implements generator for text adapters.  
2. **Approve full Option B for all including experiments on Cursor** → higher risk, expand brief.  
3. **Reject generation; hand-thin only** → smaller PR, accept ongoing drift cost.  
4. **Defer P2-4** → leave ROADMAP deferred; no code change.

---

## Self-evaluation (this planning deliverable)

| Gate | Status |
|---|---|
| Completeness | Architecture options, migration order, marker/CI interactions, binary criteria for impl |
| Ambiguity | Operator must pick 1–4 above |
| Scope trap | Migration explicitly blocked pending approval |
| Verification | N/A for design-only; portability warm-up verified separately |
| Approval | **Waiting** |

## Handoff (planning session)

- **Changed:** (warm-up) Windows python portability in eval scripts + failure capture; this brief.  
- **Verified:** `eval-agent-code-quality-selftest.sh` exit 0; `eval-gxp-process-guarantees.sh v1.1.3 HEAD` exit 0; portability commit pushed.  
- **Not done:** P2-4 migration.  
- **Parked:** bare `python3` in `adapters/cowork/build.sh` (same stub class).  
