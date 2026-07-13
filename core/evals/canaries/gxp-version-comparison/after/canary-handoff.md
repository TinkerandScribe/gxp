# Canary artifact — AFTER handoff (v1.2.0+)

## Phase 8 — Handoff

- **Changed:** Simulated one-sentence CONTRIBUTING reminder that adapter workflow
  drift is **structurally** checked via sync checks / CI.  
- **Verified:**  
  - Deterministic: `bash scripts/verify.sh` → exit 0 (live tree).  
  - Deterministic: process-guarantee scorecard
    `scripts/eval-gxp-process-guarantees.sh v1.1.3 HEAD` → after 10/11, before 2/11.  
  - Behavioral: Phase 8 deletion fails verify (see process-guarantees
    `neg_drift_behavioral` after=1).  
- **Not done:** Actual CONTRIBUTING.md product edit deliberately **not** applied
  in this eval (docs-only canary artifacts under `core/evals/`).  
- **Approval gates:** none.  
- **Dead ends:** none.  
- **Rating fields:** `ts`, `criteria_met`, `criteria_total`, `rating` (see ledger).  
- **Failure refs:** none.

## Self-check against shared rubric

| ID | Pass? | Notes |
|---|---|---|
| S1 ≥4 binary criteria | yes | 6 criteria |
| S2 out-of-scope | yes | |
| S3 deterministic verify | yes | verify.sh + scorecard + mutation |
| S4 smallest change | yes | eval artifacts only |
| S5 evidence on done | yes | exit codes + scorecard paths |
