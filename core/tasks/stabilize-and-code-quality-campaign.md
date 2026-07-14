# Task brief — stabilize (1) + stronger code-quality campaign (2)

**Date:** 2026-07-13  
**Workflow:** full  
**Slug:** stabilize-and-code-quality-campaign  

## Goal

1. Stabilize post-P2-4: CI already green; fix remaining bare `python3` in cowork build; ship changelog release.  
2. Run a stronger code-quality campaign: multi-seed control vs GXP on 3 tasks + multi-runner selftest attestation.

## Ideal State Criteria

- [x] 1. `adapters/cowork/build.sh` uses executable python probe (not Store stub).  
- [x] 2. CHANGELOG → v1.3.0; README latest; tag + GitHub release.  
- [x] 3. Multi-seed campaign (3 seeds × 3 tasks) via `run-code-quality-seeds.py`.  
- [x] 4. Report with winners, means, limits under `trials/2026-07-13-multiseed/`.  
- [x] 5. Multi-runner selftest attestation (Grok + Cursor + Claude).  
- [x] 6. `verify.sh` 0; generator `--check` 0; rate; push.

## Out of scope

- True multi-model blind agents (would need external operators mid-session).  
- Weakening structural floor.

## Verification

verify.sh; generate --check; selftest; campaign compare scripts; gh release view.
