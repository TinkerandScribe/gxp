# Canary score sheets

**Scorer:** single agent (Grok) — same model for before/after → contamination risk.  
**Primary signal:** process-guarantees totals, not canary prose elegance.

## Shared rubric scores

| Criterion | Before brief | Before handoff | After brief | After handoff |
|---|---|---|---|---|
| S1 ≥4 binary criteria | 1 | 1 | 1 | 1 |
| S2 out-of-scope | 1 | 1 | 1 | 1 |
| S3 deterministic verify step | 1 | 1 | 1 | 1 |
| S4 smallest-change framing | 1 | 1 | 1 | 1 |
| S5 done cites evidence | 0.5* | 0.5* | 1 | 1 |
| **Shared subtotal /5** | **4.5** | **4.5** | **5** | **5** |

\*Before handoff cites verify.sh in prose only; no transcript/path to scorecard.

## Version-specific scores

| Criterion | Before | After |
|---|---|---|
| V1 Phase 8 / structured handoff | 0 (not in v1.1.3 Claude workflow) | 1 |
| V2 Ratings fields named | 0 | 1 |
| V3 Structural/sync verification mentioned | 0 | 1 |
| **Version subtotal /3** | **0** | **3** |

## Combined canary totals (shared mean + version)

| Side | Shared (mean of brief+handoff) | Version | Combined /8 |
|---|---|---|---|
| Before | 4.5 | 0 | **4.5** |
| After | 5.0 | 3 | **8.0** |

## Notes

- After artifacts are **more complete** because the after workflow **requires** handoff +
  ratings fields; before workflow does not. That is an improvement in **default
  completeness**, not proof of smarter coding.
- Same-model contamination: the scorer knew the after rubric when writing before
  artifacts and tried to stay faithful to v1.1.3 constraints; residual bias remains.
