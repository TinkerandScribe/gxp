# Task brief — before/after GXP output & process eval

**Date:** 2026-07-13  
**Task slug:** eval-gxp-before-after  
**Workflow:** full  

## Goal

Measure whether v1.2.0 GXP changes improve *enforceable process quality* and
*agent-facing output completeness* versus v1.1.3 — not only that scripts pass.

## Ideal State Criteria

- [x] 1. A deterministic process-guarantee scorecard compares `v1.1.3` vs `HEAD`
  (or `v1.2.0`) with ≥8 binary checks and records pass/fail for each version.
- [x] 2. At least **2 fixed canary tasks** are defined under `core/evals/canaries/`.
- [x] 3. For each canary, a scored agent artifact exists for **before** and **after**
  under `core/evals/canaries/gxp-version-comparison/`.
- [x] 4. Shared quality rubric (≥5 binary criteria) is applied to every artifact;
  version-specific criteria are scored separately.
- [x] 5. Final report states: guarantee wins, canary score deltas, limitations
  (same-model contamination), and a clear **improved / mixed / not improved** verdict.
- [x] 6. `bash scripts/verify.sh` exits 0 after adding eval artifacts; no secrets.
- [x] 7. Honest rating appended to `core/ratings.jsonl`.

## Out of scope

- Multi-model blind trials, statistical significance, human rater panels.
- Changing product methodology based on results (report only unless a bug is found).
- Releasing a new version.

## Verification plan

1. Run `scripts/eval-gxp-process-guarantees.sh` → scorecard JSON/md.  
2. Produce canary artifacts; fill score sheets.  
3. Write report; run verify.sh; rate.
