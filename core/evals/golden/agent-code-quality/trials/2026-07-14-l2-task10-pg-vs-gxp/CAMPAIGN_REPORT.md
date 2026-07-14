# CAMPAIGN_REPORT — 2026-07-14 L2 task 10 public_green vs GXP

**Task:** `10-circuit-breaker` (second L2 multi-factor tool-using fixture)  
**Protocol:** hardened public_green (zero writes if public green) vs full GXP  

## Correctness

| Model | public_green | GXP | Δ | Winner |
|-------|-------------:|----:|---:|--------|
| grok | **0.27** (3/11) | **1.00** (11/11) | **+0.73** | **gxp** |
| qwen | **0.27** (3/11) | **0.91** (10/11) | **+0.64** | **gxp** |

## Means

| Arm | Mean |
|-----|-----:|
| public_green | **0.273** |
| gxp | **0.955** |

**Gap:** **+0.682**

## Wins

GXP **2** · public_green **0** · ties **0**

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **PASS** |
| Majority GXP wins | **PASS** |
| No GXP tamper | **PASS** |

### Verdict: **PASS**

## Combined with task 09 hardened multi-seed

Across L2 fixtures **09** and **10** under public_green vs GXP, GXP wins all matched pairs — multi-task majority holds.

## Limits

Same claim scope: beats premature public-green stop, not unconstrained best-effort.
