# Task brief

**Date:** 2026-07-30
**Task slug:** capability-scaffolding-v1
**Workflow:** full

## Goal

Add a first-class **scaffolding capability tier** (frontier | standard | constrained) to GXP so adapters can modulate prompt load and autonomy by model generation without forking the workflow or weakening verification.

## Context

- Related files:
  - `core/workflow.md` (Phase 0.5)
  - `core/templates/task-brief.md`
  - `core/routing.md`
  - `adapters/claude/ai-workflow/instructions/model-routing.md`
  - `adapters/claude/ai-workflow/custom-instructions.md`
  - `adapters/claude/ai-workflow/deltas/workflow.delta.md`
  - `adapters/cursor/ai-workflow/rule.mdc`
  - `AGENTS.md`
  - `scripts/generate-adapter-workflows.py` / `scripts/verify.sh`
- Operator request: implement model-tier-aware scaffolding per Cherny (ablate / high-level goals on capable models; keep scaffolding on weaker models), using current GXP workflow.
- Relevant rules: process changes go in `core/` first; adapters specialize; no silent host-file ablation.
- Relevant failures: verification-wrapper / adapter drift patterns — regenerate + verify after core edits.

**Strategy/Model:** Grok Build (agentic) — multi-file methodology edit with structural verify.
**Scaffolding tier:** standard — methodology change; keep full gates and verify.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** grok-build | local-agent
- **forbidden_engines:** —
- **exec_mode:** auto
- **output_contract:** core docs + workflow/brief updates + Claude adapter map + cursor/AGENTS pointers + canary note; `bash scripts/verify.sh` exit 0 after regenerate

## Ideal State Criteria

- [outcome] `core/docs/capability-scaffolding.md` exists and defines exactly three tiers (`frontier`, `standard`, `constrained`), detection order (explicit → model map → default standard), and invariants (binary criteria, verification ladder, anti-loop, ratings, privacy/stakes rails).
- [outcome] `core/workflow.md` Phase 0.5 requires selecting and recording a scaffolding tier (not only an engine/model).
- [outcome] `core/templates/task-brief.md` has a required **Scaffolding tier** field next to Strategy/Model.
- [outcome] Claude adapter documents a dated model-id → default tier map and a context-load policy per tier in `model-routing.md` (or adjacent instruction).
- [outcome] Claude custom instructions (and Phase 0.5 delta note) tell the agent to apply tier policy after Phase 0.5.
- [outcome] Cursor `rule.mdc` and root `AGENTS.md` mention scaffolding tier and point at the core doc (no second process definition).
- [outcome] A canary note under `core/evals/` records how to compare frontier vs constrained on the same brief.
- [guardrail] Verification-first, binary ISC, anti-loop, and privacy/stakes rails are not weakened for any tier.
- [guardrail] No auto-deletion of host `CLAUDE.md` / skills / hooks; ablation is operator-approved only.
- [guardrail] No three forked full workflows; one core workflow + tier policy only.
- [outcome] After `python scripts/generate-adapter-workflows.py`, `bash scripts/verify.sh` exits 0.
- [hypothesis] Touching only Claude + Cursor + AGENTS is enough for v1; other adapters can inherit via regenerated workflow Phase 0.5 text.

## Out of scope

- Auto-detect runtime in Claude Code / env tooling beyond documenting optional `GXP_SCAFFOLDING_TIER`
- Full model→tier maps for Grok, Codex, Perplexity, Cowork (beyond regenerated core text)
- Silent or automated ablation of host repo scaffolding files
- Changing privacy/stakes rails in routing.md beyond a one-line clarification
- Host-repo rollouts (pre-nicene-wiki, story-repo-steward, mooring-line)
- Version bump / GitHub release / push to origin (operator)

## Verification plan

1. File existence + content greps for tier names, detection order, invariants.
2. `python scripts/generate-adapter-workflows.py` then `python scripts/generate-adapter-workflows.py --check`
3. `bash scripts/verify.sh` exit 0
4. Walk each binding criterion with a named check (grep / test / read).

## Self-evaluation gate

- [x] Completeness — covers core + brief + Claude + cursor/AGENTS + canary + verify
- [x] Ambiguity — binding criteria are binary
- [x] Scope trap — other adapters full maps parked
- [x] Verification — verify.sh + greps
- [x] Approval gates — none required for methodology docs on feature branch; push/release parked
- [x] Criteria quality — outcomes/guardrails checkable
- [x] Anti-gaming — ships real tier axis, not rename-only of model routing
- [x] Ontology — N/A

## Approval gates

- None for implementing on feature branch.
- Operator approval before push/merge to main or host-repo ablation experiments.

## Dead ends

-

## Handoff notes

- What changed:
  - Added `core/docs/capability-scaffolding.md` (tiers, detection, invariants, ablation).
  - Extended Phase 0.5 + Phase 1 brief list in `core/workflow.md`.
  - Brief template field **Scaffolding tier**; routing note; PROGRAM.template default section.
  - Claude: model→tier map + context-load policy; custom-instructions + delta Phase 0.5 notes.
  - Cursor rule + AGENTS.md pointers; canary under `core/evals/canaries/capability-scaffolding/`.
  - Regenerated claude/chatgpt/grok/perplexity workflows + sync markers.
- What was verified: criterion greps; `python scripts/generate-adapter-workflows.py --check` OK; `bash scripts/verify.sh` exit 0.
- Explicitly not done / parked: installer `docs/` copy; full Grok/Codex/Perplexity/Cowork model maps; host-repo PROGRAM defaults; push/merge to origin; live frontier-vs-constrained trial runs.
- Approval gates: none hit (feature branch only).
- Rating: `core/ratings.jsonl` task `capability-scaffolding-v1`.
