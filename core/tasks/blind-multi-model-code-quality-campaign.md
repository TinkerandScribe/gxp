# Task brief — blind multi-model code-quality campaign (Roadmap M6.1)

**Status:** draft — ready for pickup (operator-heavy)  
**Depends on:** recommended
[`grow-code-quality-eval-tasks.md`](grow-code-quality-eval-tasks.md); harness multi-runner
selftest already green  
**Workflow:** full  

## Goal

Produce evidence on whether **GXP** improves **hidden-test correctness** when the
implementing agents **did not author the fixtures**, using frozen prompts and
score-only operators.

## Context

- Prior evidence: multi-seed incomplete one-shots lose to verify-to-green (9/9) —
  process signal, not multi-model field study.  
- Protocol base: `core/evals/golden/agent-code-quality/PROTOCOL.md`.  
- Operator rule: no release/tag spam; results land as trial reports.

## Ideal State Criteria

- [ ] 1. Written run protocol frozen before first agent run (arms, models, budgets,
  no peeking at `hidden_tests/` or `reference/`).  
- [ ] 2. At least **2 models/tools** × **2 arms** (control vs GXP) × **≥3 tasks**
  (or 1 task × ≥3 seeds if tasks not yet grown — document choice).  
- [ ] 3. Each trial scored only with `score_trial.py` (and optional brief score
  separately); JSON under `trials/<date>-blind/`.  
- [ ] 4. CAMPAIGN_REPORT.md with mean correctness per arm, win counts, and
  **pre-registered** success rule result (pass/fail).  
- [ ] 5. Pre-registered success rule (example — lock before runs):  
  GXP mean correctness − control mean ≥ **0.10** across tasks **or** GXP wins
  majority of task-level comparisons with no scope/tamper disqualifies on GXP.  
- [ ] 6. Contamination log: who could see tests; any protocol breaches.  
- [ ] 7. No marketing claim without report; rating honest about limits.

## Out of scope

- Changing the methodology to “win” the campaign.  
- Editing hidden tests mid-campaign.  
- Requiring a second-model critic product.

## Verification plan

- Protocol file committed before first score JSON.  
- Re-run `score_trial.py` on all result dirs reproduces report numbers.  
- `verify.sh` still 0 on main (campaign artifacts only under evals/).

## Operator checklist

1. Freeze protocol + success rule in this brief or a dated PROTOCOL addendum.  
2. Dispatch control and GXP sessions (separate contexts).  
3. Collect trees → score → report.  
4. Decide claim language from pre-registered rule only.
