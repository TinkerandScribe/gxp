# Canary: GXP v1.1.3 vs current (v1.2.0+) process & output eval

## Question

Did the verification-hardening release improve **enforceable process quality**
and **agent handoff completeness** versus v1.1.3?

## Design

| Layer | Method | Bias notes |
|---|---|---|
| **A. Process guarantees** | `scripts/eval-gxp-process-guarantees.sh` | Fully deterministic; measures detection/enforcement, not prose talent |
| **B. Fixed canary tasks** | Same prompt + shared rubric, scored for before/after | Same model runs both → contamination risk; still useful for completeness checklist |
| **C. Verdict** | Guarantee delta primary; canary scores secondary | Do not claim statistical significance |

## Canary tasks (fixed)

1. **`canary-brief-only`** — Produce a GXP task brief for:  
   *“Add one sentence to CONTRIBUTING.md under ‘Before you open a PR’ reminding
   contributors that adapter workflow drift is now structurally checked.”*  
   No code change required for the canary itself.

2. **`canary-handoff`** — Produce a Phase-8-style handoff claiming the brief-only
   task is done (simulated completion), including verification evidence.

## Shared quality rubric (both versions)

| ID | Criterion |
|---|---|
| S1 | ≥4 binary Ideal State Criteria |
| S2 | Explicit out-of-scope |
| S3 | ≥1 deterministic verification step named |
| S4 | Smallest-change framing (no scope expansion) |
| S5 | Done claim cites a concrete command or evidence |

## Version-specific rubric

| ID | Criterion | Expected before (v1.1.3 claude) | Expected after (v1.2.0+) |
|---|---|---|---|
| V1 | Handoff section present (Phase 8 content) | optional | required |
| V2 | Ratings fields named (`ts`, `criteria_met`, …) | optional | required |
| V3 | Mentions structural/sync check as verification | optional | expected |

## Artifacts

- `process-guarantees.md` / `.json` — layer A  
- `before/` / `after/` — layer B artifacts + `scores.md`  
- `REPORT.md` — final verdict  
