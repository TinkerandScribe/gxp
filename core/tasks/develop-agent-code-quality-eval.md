# Task brief — agent code-quality eval harness

**Date:** 2026-07-13  
**Task slug:** develop-agent-code-quality-eval  
**Workflow:** full  

## Goal

Ship a frozen, mostly automatic test that can score whether agents produce
*better code* under different conditions (e.g. no-GXP vs GXP), without relying
on self-grading prose.

## Ideal State Criteria

- [x] 1. At least one golden coding task with starter code + hidden automated tests.
- [x] 2. A scorer script grades a result directory purely from test outcomes (+ scope).
- [x] 3. Reference solution scores full marks; unmodified starter scores lower.
- [x] 4. Protocol documents A/B conditions, contamination controls, and verdict rules.
- [x] 5. Process adherence is scored separately from code quality (not conflated).
- [x] 6. `bash scripts/verify.sh` exits 0; no secrets; eval is self-contained (stdlib).
- [x] 7. Rating appended to `core/ratings.jsonl`.

## Out of scope

- Running multi-model statistical campaigns in this task (harness only + self-test).
- Changing GXP core workflow text.

## Verification plan

1. Score starter → low correctness.  
2. Score reference → high correctness.  
3. Run verify.sh.  
