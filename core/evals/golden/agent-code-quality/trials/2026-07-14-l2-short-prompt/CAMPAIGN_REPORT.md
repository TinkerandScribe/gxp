# CAMPAIGN_REPORT — 2026-07-14 short prompt + Phase 0

**Task:** `10-circuit-breaker`  
**Prompt:** underspecified `prompt.short.md` for **both** arms  
**Workspace:** full starter **with** `.ai/` for both  

## Design

| Arm | Behavior |
|-----|----------|
| control | Tools; no formal GXP; may discover `.ai/` or not |
| gxp | Forced Phase 0 + BRIEF + criteria |

## Correctness

| Model | control | GXP | Δ | Winner |
|-------|--------:|----:|---:|--------|
| grok | **0.73** (8/11) | **1.00** (11/11) | **+0.27** | **gxp** |
| qwen | **0.82** (9/11) | **0.82** (9/11) | 0.00 | **tie** |

## Means

| Arm | Mean |
|-----|-----:|
| control | **0.773** |
| gxp | **0.909** |

**Gap:** **+0.136** (≥ 0.10)

## Wins

GXP **1** · control **0** · ties **1**

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **PASS** |
| Majority GXP wins | **PASS** (1 > 0) |
| No GXP tamper | **PASS** |

### Verdict: **PASS**

## Interpretation

1. **New PASS outside pure public_green stop:** underspecified user prompt + GXP Phase 0 can lift Grok hidden score when control under-implements multi-factor edges.  
2. **Qwen:** both arms mined `.ai/` and matched at 0.82 — GXP process did not add correctness over opportunistic control discovery.  
3. **Grok control** used short-prompt incomplete fill (session); not a blind independent agent. Still a valid “skip Phase 0 / miss failure notes” scenario.

## Relation to other PASSes

| Design | Verdict |
|--------|---------|
| public_green stop | **PASS** (primary claim) |
| **short prompt + Phase 0** | **PASS** (this trial; Grok-driven) |
| unconstrained full prompt | **FAIL** |

## Limits

- N=1 task, N=1 seed.  
- Grok control incompleteness partly session-role.  
- Qwen tie weakens “always Phase 0 wins.”
