# Task brief — Ratings chain tooling fix (experimental-v0 dogfood)

**Date:** 2026-08-06  
**Task slug:** ratings-chain-tooling-fix  
**Workflow:** full  
**clarification_protocol:** experimental-v0  
**Scaffolding tier:** standard  
**Status:** ready for implement (operator confirmed candidate 1)

## Goal

Make `scripts/validate-ratings-chain.py` succeed on `core/ratings.jsonl` by fixing the UTF-8 BOM read failure and any blocking `entry_hash` / chain issues that prevent a clean validation, without inventing false history.

## Context

- Validator crashes today: `JSONDecodeError: Unexpected UTF-8 BOM` on line 1 of `core/ratings.jsonl`.  
- Optional hash-chain fields are documented in the ledger schema line; some historical lines may have `entry_hash` mismatches.  
- Policy: live-for-fork-work re-anchors rather than rewriting missing parents; do not invent chains for unchained historical lines.  
- First **non-meta** experimental-v0 product dogfood after Clarifier protocol v0.

**Strategy/Model:** Grok Build — multi-file tooling fix + isolated criteria check.  

## Ideal State Criteria

- [outcome] `python scripts/validate-ratings-chain.py` exits **0** on repo-root `core/ratings.jsonl` and prints an OK summary.  
- [outcome] Validator tolerates a UTF-8 BOM on the ledger file (read via `utf-8-sig` or equivalent) so BOM does not crash parsing.  
- [outcome] Any `entry_hash` mismatch that still blocks validation is fixed by either correcting the hash to match the payload, re-anchoring per documented policy, or documenting a deliberate skip — without fabricating prior ledger content.  
- [guardrail] No force-rewrite of unrelated ratings history meaning; example/schema lines remain valid JSON.  
- [guardrail] `bash scripts/verify.sh` still exits 0 after the change.  
- [guardrail] Stable GXP core workflow path is not modified; experimental-v0 is not promoted to default.  
- [outcome] A ratings ledger entry for this task records `clarification_protocol: experimental-v0` and checker iteration count.  
- [hypothesis] Smallest fix is `encoding="utf-8-sig"` plus at most one re-anchor or hash repair on the known mismatched chained line.

## Out of scope

- Mandatory hash chains for every historical line.  
- Full ratings UI/product.  
- M6 campaign work.  
- ACP workflow implementation (separate brief).  
- Changing Phase 0–8 methodology.

## Verification plan

1. Isolated criteria-checker PASS on this brief (experimental-v0) before implement.  
2. `python scripts/validate-ratings-chain.py` → exit 0.  
3. `bash scripts/verify.sh` → exit 0.  
4. `git diff` limited to tooling/ledger/test notes as needed.  
5. Ratings entry present with experimental flag.

## Self-evaluation gate

(complete under experimental-v0 with `gxp-criteria-checker`)

## Approval gates

Operator confirmed candidate 1 (2026-08-06). Proceed after checker PASS.

## Handoff notes

Related decision set: M6 parked; ACP v1 design approved (implement separate).
