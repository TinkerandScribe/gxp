# Task brief — grow code-quality eval task set (Roadmap M5.1)

**Status:** done  
**Depends on:** harness + selftest (done)  
**Blocks:** recommended before
[`blind-multi-model-code-quality-campaign.md`](blind-multi-model-code-quality-campaign.md)  
**Workflow:** full

## Goal

Add frozen coding tasks so control arms no longer hit a correctness ceiling as
often, and multi-model campaigns cover more failure modes.

## Context

- Today: `01-parse-kv`, `02-slugify`, `03-merge-intervals`.  
- Multi-seed incomplete controls still average ~0.7; some seeds ≥0.9.  
- Need tasks where partial implementations systematically fail more tests.

## Ideal State Criteria

- [x] 1. +2 tasks: `04-safe-join`, `05-count-words`.  
- [x] 2. Reference 1.0; starters well below reference (safe-join / count-words).  
- [x] 3. Selftest lists all five tasks.  
- [x] 4. Seeds extended for 04/05 in `run-code-quality-seeds.py`.  
- [x] 5. Stdlib only.  
- [x] 6. verify.sh 0.  
- [x] 7. README updated.  

## Out of scope

- Running the blind multi-model campaign (separate brief).  
- Non-Python tasks (unless explicitly chosen and scored automatically).

## Verification plan

Selftest; score starter/reference per task; run multi-seed if extended; verify.sh.

## Suggested task themes (non-binding)

- Path normalization / traversal rejection  
- Idempotent config merge with conflict rules  
- Small stateful CLI with exit codes  
