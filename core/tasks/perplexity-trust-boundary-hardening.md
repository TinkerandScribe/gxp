# Task brief

**Date:** 2026-07-25
**Task slug:** perplexity-trust-boundary-hardening
**Workflow:** full

## Goal

Harden the live Perplexity adapter as research-stage only with explicit
provenance, epistemic handoff sections, and no false local-verify claims.

## Context

- Source brief: `adapters/artifacts/brief-perplexity-adapter.md`
- Live tree: `adapters/perplexity/ai-workflow/` (Collections + instructions; no greenfield Space package)
- Related: methodology ship in `core/tasks/criteria-hardening-and-anti-fixation.md` already done

**Strategy/Model:** grok-native — docs-only adapter hardening

## Ideal State Criteria

- [outcome] Handoff template separates verified findings, inferences, and open questions.
- [outcome] Handoff requires repo vs external provenance on load-bearing facts.
- [guardrail] Adapter docs never instruct claiming local tests/lint/build or file edits unless a host performed them.
- [outcome] SKILL / README / research-workflow state research-stage scope and trust boundaries.
- [outcome] Sync checks fail if required handoff trust-boundary markers are removed.
- [guardrail] No parallel Space-first file tree created; live Collections layout preserved.

## Out of scope

- SPACE_INSTRUCTIONS / START_SESSION / REWRITE_PROMPT greenfield package
- API automation wrapper
- Criteria/anti-fixation methodology (already shipped)

## Verification plan

1. Content greps for Verified findings / Inferences / Open questions / Explicit non-claims / false local-verify
2. `bash adapters/perplexity/ai-workflow/sync/check-core.sh`
3. `bash scripts/verify.sh`
4. Confirm no new Space-first top-level files under adapters/perplexity/

## Handoff notes

- **What changed:** Live Perplexity adapter trust boundaries in `research-handoff.md`,
  `SKILL.md`, `README.md`, `research-workflow.md`, `research-to-brief.md`, delta,
  `TEST_PROMPT.md`; sync checks enforce handoff markers; workflow regenerated.
- **Verified:** `check-core.sh` PASS; `verify.sh` exit 0; greps for Verified findings /
  Inferences / Open questions / Explicit non-claims / false local-verify; no
  SPACE_INSTRUCTIONS greenfield files.
- **Not done:** Space-mode optional files (still hypothesis only).
