# Task brief

**Date:** 2026-07-25
**Task slug:** criteria-hardening-and-anti-fixation
**Workflow:** full

## Goal

Ship criteria-model hardening and anti-fixation/ceremony defaults into core methodology docs, then clean and rebaseline `adapters/artifacts` so planning notes match the live repo.

## Context

- Operator: `/gxp proceed as recommended` after review of `adapters/artifacts`.
- Recommended order: (1) criteria-hardening, (2) anti-fixation, (3) Perplexity artifact rebase + hygiene — no greenfield Perplexity adapter.
- Edit targets: `core/templates/task-brief.md`, `core/workflow.md` (Phase 1–2, full vs lightweight, Phase 4), `core/templates/gxp-refine-run.md`, regenerate adapters via `scripts/generate-adapter-workflows.py`, `ROADMAP.md` near-term rows, `adapters/artifacts/*`.
- Live Perplexity adapter already exists at `adapters/perplexity/` — do not create parallel Space-first layout.
- Sync: adapter structural floor PASS; core advanced 2 commits within threshold.
- Rules/failures: no secrets; prefer durable notes; PowerShell quoting failure if appending JSONL via shell.

**Strategy/Model:** grok-native full GXP — multi-file methodology docs + generator regen; no external handoff required.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [grok]
- **forbidden_engines:** []
- **exec_mode:** auto
- **output_contract:** core + generated adapter workflow diffs; cleaned artifacts; rating entry

## Ideal State Criteria

- [outcome] `core/templates/task-brief.md` requires every Ideal State Criteria line to be tagged `[outcome]`, `[guardrail]`, or `[hypothesis]`, and documents that only `[outcome]` / `[guardrail]` are binding for Phase 2 self-eval and Phase 6 verification.
- [outcome] Phase 2 self-eval in `core/workflow.md` includes a criteria-quality pass (binding ISC binary, outcome-focused, independently checkable, mechanism only if operator-required) and rejects style-only binding criteria (e.g. clean / idiomatic / elegant).
- [outcome] Every brief template includes the standing non-binding anti-gaming question: whether implementation satisfies the operator's stated objective, not merely the literal checklist.
- [outcome] Full-vs-lightweight prose defaults to lightweight for single-file (or equivalent small-scope) changes with no new external dependency, and requires a one-line justification when invoking full workflow for such a change; multi-file / multi-constraint / thin-smoke cases still require full.
- [outcome] Phase 4 anti-loop rule requires, after a second failed attempt on the same approach, a written reframe (restate problem + name ≥1 discarded assumption) before any further attempt; a third attempt that is only a minor variant without that reframe is disallowed.
- [outcome] `core/templates/gxp-refine-run.md` includes a standing audit question: whether the gate still solves a real bottleneck or has become ritual.
- [guardrail] No phase gate (self-eval, smallest viable change, deterministic-then-subjective verification, anti-loop, failure capture, operator refine gates) is removed or weakened; no verify-script behavior change beyond regenerating adapter workflows from core.
- [outcome] `adapters/artifacts` has a README, brief files use `.md` extensions and fixed review notes, and Perplexity planning materials acknowledge the live `adapters/perplexity/` tree (no greenfield Space file set as next action).

## Out of scope

- Divergent pre-Phase-1 spike workflow step (parked for a later brief).
- Requiring verify scripts to check behavior vs superficial markers (separate anti-gaming tooling brief).
- Greenfield Perplexity Space instructions package or new adapter file layout.
- Cursor `rule.mdc` generator migration (M8 deferred).
- Committing trial packs or changing public scientific claims.
- Git commit/push unless operator later requests it.

## Verification plan

1. Deterministic: `rg` / read for tags in `task-brief.md`, Phase 2 quality language, anti-gaming question, lightweight default + justification, reframe anti-loop, gxp-refine audit question.
2. Deterministic: `python scripts/generate-adapter-workflows.py --check` after regen.
3. Deterministic: `bash scripts/verify.sh` (or Git Bash equivalent) exit 0.
4. Deterministic: artifact paths use `.md`; README present; deep dive / brief-perplexity no longer claim adapter does not exist.
5. Subjective: sample mental walk — small single-file fix chooses lightweight by default; multi-file still full.

## Self-evaluation gate

- [x] **Completeness** — covers both methodology ship items + artifact cleanup from the review recommendation.
- [x] **Ambiguity** — tags and binding rules are binary; “minor variant” judged via presence of reframe note.
- [x] **Scope trap** — spike, verify-script gaming, greenfield Perplexity parked.
- [x] **Verification** — each criterion has a file/content check.
- [x] **Approval gates** — none destructive; operator already approved via “proceed as recommended.”
- [x] **Criteria quality** — binding lines are outcome/guardrail tagged; layout for Perplexity is not a locked mechanism criterion.
- [x] **Anti-gaming** — objective is ship methodology mitigations + clean artifacts, not merely rename files.

## Approval gates

None (docs + generated adapters only; operator pre-approved recommended sequence).

## Dead ends

None.

## Handoff notes

- **What changed:** Criteria taxonomy in `core/templates/task-brief.md`; Phase 1–2 + full/lightweight default + Phase 4 reframe in `core/workflow.md`; ritual audit in `gxp-refine-run.md`; regenerated claude/chatgpt/grok/perplexity `instructions/workflow.md`; Cursor `rule.mdc` aligned; `ROADMAP.md` Part C; `adapters/artifacts` cleaned and Perplexity notes rebased.
- **Verified:** `python scripts/generate-adapter-workflows.py --check` OK; `bash scripts/verify.sh` exit 0 (all adapter sync + gxp-refine selftest); content greps for tags / reframe / lightweight default / ritual audit.
- **Not done / parked:** divergent pre-Phase-1 spike; verify-script behavior-over-markers; Perplexity Space package (n/a live adapter — use rebased brief for a future trust-boundary pass).
- **Approval gates:** none hit (docs + generated).
- **Rating:** `core/ratings.jsonl` task `criteria-hardening-and-anti-fixation`.
