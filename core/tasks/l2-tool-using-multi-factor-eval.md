# Task brief — L2 tool-using multi-factor code-quality eval

**Date:** 2026-07-14  
**Task slug:** l2-tool-using-multi-factor-eval  
**Workflow:** full  
**Status:** done  

## Goal

Ship one golden **L2** coding task where success requires **multi-file repair**,
**repo memory** (rules/failures), and **tool use** (run public verify), so
control vs GXP can measure process—not single-shot interview puzzles.

## Context

- L0–L1 packs (01–08) ceiling under strong single-shot models.  
- GXP targets: binary criteria, Phase 0, verify, verification plan, anti-loop.  
- Harness today is single-file oriented; needs package mode.

**Strategy/Model:** session implement + unittest scorer — deterministic, stdlib.

## Ideal State Criteria

- [x] 1. Task pack **`09-rate-limit-service`**: multi-file starter + reference +
  weak `tests_public/` + hidden tests + `.ai/` PROGRAM/rules/failures.  
- [x] 2. `score_trial.py` supports `meta.mode = "package"` (grade whole tree).  
- [x] 3. Reference correctness **1.0**; starter **≈0.17** (≤ 0.35) on hidden tests.  
- [x] 4. Public verify (`tests_public`) **passes on starter** (weak green trap).  
- [x] 5. Prompt + control/GXP **tool-using** operator prompts documented.  
- [x] 6. Selftest includes 09; full selftest exit 0.  
- [x] 7. Stdlib only; no network deps; no campaign run in this brief.  
- [x] 8. Scope allows BRIEF/HANDOFF/`tests_public` extras; forbids new packages.

## Out of scope

- Full matched multi-model campaign on 09.  
- Transcript mining for `tool_verify_ran` (document metric; implement later).  
- Non-Python packages.

## Verification plan

1. Score starter/reference with Python 3.14.  
2. Run public tests on starter → exit 0.  
3. `bash scripts/eval-agent-code-quality-selftest.sh` includes 09.  
4. Spot-check: every hidden assertion is stated or implied in prompt/README/failures.

## Multi-factor traps (must appear)

| Factor | Planted in starter |
|--------|-------------------|
| Sliding vs fixed window | Wrong window math |
| Fail-closed config | Invalid config allows all |
| Multi-client isolation | Shared counter across keys |
| Clock inject | Wall clock only / ignore clock |
| Scope | Tempting full rewrite |
| Weak public tests | Pass while hidden fail |

## Self-evaluation gate

- Completeness: L2 tool-using, not another pure function — yes.  
- Scope trap: one task pack + harness only — yes.  
- Verification: automated scores — yes.
