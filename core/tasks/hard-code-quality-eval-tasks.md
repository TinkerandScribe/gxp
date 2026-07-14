# Task brief — hard code-quality eval tasks (break the ceiling)

**Date:** 2026-07-14  
**Status:** done  
**Workflow:** full  
**Depends on:** harness + tasks 01–05 (done); matched campaigns hit ceiling  
**Blocks:** next matched/blind claim attempt that needs headroom  

## Goal

Add **≥3 frozen coding tasks** hard enough that strong models (Grok-class,
Qwen 27B-class) do **not** routinely score 1.0 on control *and* GXP under
single-shot implement. Enable measurable control vs GXP correctness gaps.

## Context (why easy tasks failed science)

Campaigns through 2026-07-14 (`*-campaign`, `*-multiseed`, `*-operator-blind`,
`*-matched-grok-qwen`) repeatedly hit **correctness = 1.0** on tasks 01/04/05
for capable models. Pre-registered gap rules **FAIL** under ceiling — not
because GXP was disproven, but because fixtures lacked headroom.

Easy-task failure modes (too weak for frontier/local-strong):

| Weak pattern | Why ceiling |
|--------------|-------------|
| Single pure function + short rule list | Pretraining + one-shot fix |
| “Interview classic” (merge intervals, slugify) | Memorized |
| Starter bugs obvious in prompt | Model rewrites whole file correctly |

## Design principles (non-negotiable)

1. **Multi-rule interaction** — missing any one rule fails ≥2 tests.  
2. **Adversarial starter** — looks mostly right; fails edge/interaction tests.  
3. **Not a famous leetcode slug** — prefer systems/library micro-specs.  
4. **Injectable time / pure-ish APIs** where needed (deterministic hidden tests).  
5. **Stdlib only**; same pack layout as 01–05 (`prompt`, `starter`, `reference`,
   `hidden_tests`, `meta.json`).  
6. **Reference scores 1.0**; **starter scores ≤ 0.45** on each hard task, and
   **mean starter ≤ 0.35** across the hard pack (room without free perfects).  
7. **≥8 hidden tests** per task covering happy path + ≥4 traps.

## Ideal State Criteria

- [x] 1. Task pack **`06-lru-ttl`**: capacity + TTL + clock inject + peek vs get.  
- [x] 2. Task pack **`07-deep-merge`**: recursive merge, list modes, `None` delete, no mutate.  
- [x] 3. Task pack **`08-line-chunker`**: stateful byte feeder, max line, multi-byte newline.  
- [x] 4. Each: `reference` **1.0**; starters **06≈0.17 / 07≈0.44 / 08≈0.29** (mean ≈0.30 ≤ 0.35).  
  Measured Python 3.14 `score_trial.py` after ship.  
- [x] 5. `scripts/eval-agent-code-quality-selftest.sh` includes 06–08 and exits 0.  
- [x] 6. README task list updated; this brief criteria checked off when done.  
- [x] 7. Stdlib only; no network; no changes to scorer contract beyond new task ids.  
- [x] 8. No full multi-model campaign in this task (design + fixtures only).

## Out of scope

- Running matched/blind campaigns on the new tasks (separate brief).  
- Non-Python tasks.  
- Changing success thresholds in old campaign reports.  
- Making tasks “unfair” (hidden requirements not in prompt.md).

## Verification plan

1. Score each starter and reference with Python 3.14 `score_trial.py`.  
2. Assert reference == 1.0 and starter ≤ 0.40 and starter < reference.  
3. Run `bash scripts/eval-agent-code-quality-selftest.sh` (all tasks 01–08).  
4. Spot-check: prompt lists every behavior that a test asserts.

## Difficulty calibration (target, not a gate)

| Arm expectation (strong model, single-shot) | Target mean correctness |
|---------------------------------------------|-------------------------|
| Control | 0.35 – 0.85 (not all 1.0) |
| GXP | may match or beat control; **must have room** either way |

If a pilot still ceilings all three, add adversarial seeds or a fourth task
in a follow-up brief — do not loosen hidden tests to create fake fails.

## Suggested trap catalog (map into tests)

- **06:** expire-on-get removes; `__contains__` does not refresh; capacity after
  reaping expired; set-updates MRU+TTL; capacity &lt; 1 raises.  
- **07:** do not mutate inputs; nested dict+scalar override; list
  `replace`/`extend`/`unique`; `None` deletes key; list under dict key.  
- **08:** partial newline sequence; `max_line` before append; `close()` flush
  without requiring delimiter; empty feeds; binary (not text) safe.

## Rating note (after ship)

Expect process/GXP lift only if agents use criteria + self-checks on traps;
single-shot may still fail. Honest: fixtures prove **headroom**, not GXP win.
