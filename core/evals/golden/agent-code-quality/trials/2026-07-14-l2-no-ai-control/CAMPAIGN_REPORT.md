# CAMPAIGN_REPORT — 2026-07-14 control without `.ai/` vs GXP

**Task:** `10-circuit-breaker`  
**Design:** control workspace **strips `.ai/`**; GXP keeps PROGRAM/rules/failures. Both get full task `prompt.md` in the tool runner.

## Correctness

| Model | control_no_ai | GXP | Δ | Winner |
|-------|--------------:|----:|---:|--------|
| grok | **1.00** (11/11) | **1.00** (11/11) | 0 | **tie** |
| qwen | **0.91** (10/11) | **0.91** (10/11) | 0 | **tie** |

## Means

| Arm | Mean |
|-----|-----:|
| control_no_ai | **0.955** |
| gxp | **0.955** |

**Gap:** **0.000**

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **FAIL** |
| Majority GXP wins | **FAIL** |
| No GXP tamper | **PASS** |

### Verdict: **FAIL**

## Interpretation

Removing `.ai/` from control does **not** create a GXP hidden-correctness advantage when the **task prompt already encodes** multi-factor semantics (fail-closed, half-open, etc.). Control still listed missing `.ai/` then fixed from prompt + starter bugs.

Qwen control looked for `.ai/` (failed list) then proceeded from service files + prompt — same residual miss as GXP (`invalid_config_fail_closed`).

## Synthesis with prior campaigns

| Design | Gap | Verdict |
|--------|----:|---------|
| public_green stop vs GXP | large + | **PASS** |
| unconstrained control (with `.ai/`) vs GXP | 0 | **FAIL** |
| **control without `.ai/` vs GXP** | **0** | **FAIL** |

**Meaningful GXP wins remain conditioned on premature public-green stop**, not on Phase-0 file presence alone when the prompt is complete.
