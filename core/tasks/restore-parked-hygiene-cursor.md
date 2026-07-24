# Task brief

**Date:** 2026-07-24
**Task slug:** restore-parked-hygiene-cursor
**Workflow:** full
**Status:** done — shipped PR #7 / `320a5a3`

## Goal

Restore still-relevant parked-stash themes E, C, and B onto main without blind `stash pop`, without weakening workflow/routing gates, and without dropping the Cursor Not gxp-refine disclaimer.

## Context

- Related files: stash W `3f03726` (`park-unrelated-before-gxp-refine`); research `core/tasks/research-parked-stash-relevance.md`
- Related PRs: #3–#5 gxp-refine surfaces; #6 research prompt
- Relevant rules: `core/rules/02-local-context-never-committed.md` (absolute path leak)
- Relevant failures: `core/failures/powershell-double-quote-backtick-eats-markdown.md` (write MD via Python)
- Background: research classified E/C/B as KEEP; D DROP; A deferred to separate release-notes brief

**Strategy/Model:** cursor/local-agent — multi-file adapter doc + one hygiene path fix; criteria are mechanical string/marker checks.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [cursor, claude-code, local-agent]
- **forbidden_engines:** []
- **exec_mode:** auto
- **output_contract:** PR with E+C+B fixes; verify.sh 0; rating appended

## Ideal State Criteria

- [x] 1. `OPERATOR_RUNBOOK.md` DEST example has no `C:\Users\Reepicheep` (or other absolute user path); uses a relative `<repo>\...` placeholder.
- [x] 2. Cowork `ratings-schema.md` documents optional `prev_hash` and `entry_hash` with pointer to `scripts/validate-ratings-chain.py`.
- [x] 3. Cursor `rule.mdc` contains the strings `Verification ladder` and `Where to append`, plus sharpened full/lightweight triggers matching stash intent (smoke thin / underspecified → full).
- [x] 4. Cursor `START_SESSION.md` paste block includes Verification ladder + where-to-append ratings guidance **and** still contains the `## Not gxp-refine` section linking `GXP_REFINE.md`.
- [x] 5. Cursor `TEST_PROMPT.md` quiz includes Verification-ladder and ratings-placement questions (12-question scoring thresholds).
- [x] 6. Cursor README mentions Verification ladder and where-to-append ratings; `sync/check-core.sh` and `.ps1` assert markers `Verification ladder` and `Where to append`.
- [x] 7. `bash scripts/verify.sh` exits 0; no edits to `core/workflow.md` or `core/routing.md`.
- [x] 8. Rating appended to `core/ratings.jsonl` via Python `json.dumps` (optional hash chain continued).

## Out of scope

- Blind `stash pop` / applying stash ratings.jsonl line (D)
- CHANGELOG/README 1.3.1 rewrite or git tag (see `release-notes-1.3.1-rewrite.md`)
- Adding skill-zip builder source tree
- Weakening Verification ladder / routing rails

## Verification plan

1. `rg "Reepicheep|C:\\Users" core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md` → no matches
2. `rg "prev_hash|entry_hash" adapters/cowork/.../ratings-schema.md` → both present
3–6. `rg` markers in Cursor adapter files + run `bash adapters/cursor/ai-workflow/sync/check-core.sh`
7. `bash scripts/verify.sh`
8. `python scripts/validate-ratings-chain.py` after append

## Self-evaluation gate

- [x] **Completeness**
- [x] **Ambiguity**
- [x] **Scope trap**
- [x] **Verification**
- [x] **Approval gates** — operator loop tick #1 auto-approve for this bounded restore; no tag/release.

## Approval gates

- None remaining for this brief (auto-approved by operator loop). Do not tag a release.

## Dead ends

-

## Handoff notes

- What changed: OPERATOR_RUNBOOK DEST relativized; cowork ratings-schema hash fields; Cursor Verification ladder + where-to-append across rule/START/TEST/README/sync (kept Not gxp-refine).
- Verified: `bash scripts/verify.sh` exit 0; cursor `check-core.sh` PASS including new markers; no Reepicheep path in runbook; no workflow.md/routing.md edits.
- Parked: stash `park-unrelated-before-gxp-refine` still local; release-notes-1.3.1-rewrite brief; D orphan rating DROP.
- Rating: core/ratings.jsonl task restore-parked-hygiene-cursor
