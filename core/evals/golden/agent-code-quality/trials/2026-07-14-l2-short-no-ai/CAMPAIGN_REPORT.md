# CAMPAIGN_REPORT — 2026-07-14 short prompt + control without `.ai/`

**Task:** `10-circuit-breaker`  
**Prompt:** `prompt.short.md` both arms  
**Control:** `.ai/` removed · **GXP:** `.ai/` present  

## Correctness

| Model | control | GXP | Δ | Winner |
|-------|--------:|----:|---:|--------|
| grok | **0.73** (8/11) | **1.00** (11/11) | **+0.27** | **gxp** |
| qwen | **0.82** (9/11) | **0.82** (9/11) | 0 | **tie** |

## Means

| Arm | Mean |
|-----|-----:|
| control | **0.773** |
| gxp | **0.909** |

**Gap:** **+0.136**

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **PASS** |
| Majority GXP wins | **PASS** (1 > 0) |
| No GXP tamper | **PASS** |

### Verdict: **PASS**

## Interpretation

Combining **underspecified prompt** with **no control Phase-0 files** reproduces the short-prompt PASS (gap +0.14). Qwen still reaches the same 0.82 without `.ai/` (prompt + starter suffice for partial multi-factor fix). Grok GXP full Phase 0 fill remains the decisive win.

Does **not** overturn: full-prompt unconstrained control still matches GXP.

## Limits

Grok control incomplete is session-role partial implement under short prompt. Qwen control never needed `.ai/` to match GXP.
