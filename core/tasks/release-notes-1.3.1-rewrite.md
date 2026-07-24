# Task brief

**Date:** 2026-07-24
**Task slug:** release-notes-1.3.1-rewrite
**Workflow:** full
**Status:** done — shipped 2026-07-24 (operator triage auto-approve + tag authorized if honest)

## Goal

Rewrite CHANGELOG/README Latest for a truthful 1.3.1 narrative against HEAD, without claiming absent skill-zip builder sources; tag 1.3.1 when verify is green and claims match HEAD.

## Context

- From research 
esearch-parked-stash-relevance.md theme A (PARTIAL).
- Stash draft at W 3f03726 was stale vs HEAD and invented skill-src / uild-skill-zip.sh — **not** used.
- Operator 2026-07-24 triage: approve rewrite; tag OK if contents honest.

**Strategy/Model:** local-agent — docs + brief triage; tag after verify green.

## Routing

- **privacy_class:** public
- **stakes:** low (docs) / high if tagging
- **engine_candidates:** [cursor, local-agent]
- **forbidden_engines:** []
- **exec_mode:** auto (operator authorized tag when honest)
- **output_contract:** CHANGELOG + README bump; 1.3.1 tag/release when verify green

## Ideal State Criteria

- [x] 1. CHANGELOG has ## [1.3.1] whose bullets are each true at the commit being released (spot-check ≥5 claims).
- [x] 2. No 1.3.1 bullet claims tracked skill-src / uild-skill-zip.sh unless those paths exist in-tree.
- [x] 3. README Latest points at v1.3.1 with a one-line accurate summary.
- [x] 4. ash scripts/verify.sh exits 0.
- [x] 5. Git tag 1.3.1 created after verify green with honest changelog (operator triage authorized).
- [x] 6. Rating appended for the docs (and separately for release if tagged).

## Out of scope

- Implementing a skill-zip builder
- Restoring Cursor/runbook/schema (owned by 
estore-parked-hygiene-cursor.md, shipped #7)
- Marketing claims about GXP code-quality lift

## Verification plan

Spot-check each bullet vs tree; verify.sh; tag/release when claims match HEAD.

## Approval gates

- None remaining — operator triage authorized docs + honest tag.

## Handoff notes

- Honest 1.3.1: gxp-refine v0, Verification ladder, M4/M5, Grok productization, eval local-only, path hygiene, PS backtick failure, Cursor ladder sync — **no** skill-zip builder claims.
- Stash park-unrelated-before-gxp-refine dropped after residual absorbed/confirmed obsolete (B/C/E via #7; A rewritten; D DROP stays dropped).
