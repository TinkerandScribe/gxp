# Task brief

**Date:** 2026-07-24
**Task slug:** release-notes-1.3.1-rewrite
**Workflow:** full
**Status:** parked — wait for operator release intent

## Goal

Rewrite CHANGELOG/README Latest for a truthful 1.3.1 narrative against then-HEAD, without claiming absent skill-zip builder sources, and without tagging until operator requests.

## Context

- From research `research-parked-stash-relevance.md` theme A (PARTIAL).
- Stash draft at W `3f03726` is stale vs HEAD and invents `skill-src` / `build-skill-zip.sh`.

**Strategy/Model:** local-agent — docs-only; hold until operator wants a release.

## Routing

- **privacy_class:** public
- **stakes:** low (docs) / high if tagging
- **engine_candidates:** [cursor, local-agent]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human for tag
- **output_contract:** CHANGELOG + README bump; tag only after explicit operator ask

## Ideal State Criteria

- [ ] 1. CHANGELOG has `## [1.3.1]` whose bullets are each true at the commit being released (spot-check ≥5 claims).
- [ ] 2. No 1.3.1 bullet claims tracked `skill-src` / `build-skill-zip.sh` unless those paths exist in-tree.
- [ ] 3. README Latest points at v1.3.1 with a one-line accurate summary.
- [ ] 4. `bash scripts/verify.sh` exits 0.
- [ ] 5. Git tag `v1.3.1` created **only** after explicit operator approval (or explicitly deferred in handoff).
- [ ] 6. Rating appended for the docs (and separately for release if tagged).

## Out of scope

- Implementing a skill-zip builder
- Restoring Cursor/runbook/schema (owned by `restore-parked-hygiene-cursor.md`)
- Marketing claims about GXP code-quality lift

## Verification plan

Spot-check each bullet vs tree; verify.sh; operator sign-off before tag.

## Approval gates

- **Tag/release** — stop for operator.

## Handoff notes

- Parked by operator-loop tick #1 after stash relevance research.
