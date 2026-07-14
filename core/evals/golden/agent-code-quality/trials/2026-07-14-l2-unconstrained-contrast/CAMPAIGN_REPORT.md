# CAMPAIGN_REPORT — 2026-07-14 unconstrained control vs GXP (contrast)

**Task:** `10-circuit-breaker`  
**Purpose:** When control is **best-effort tool use** (not public-green stop), does GXP still win?

## Arms

| Arm | Discipline |
|-----|------------|
| `control` | Tools + fix; no formal BRIEF; public verify before done |
| `gxp` | Phase 0 + BRIEF + criteria + HANDOFF |

## Correctness

| Model | control | GXP | Δ | Winner |
|-------|--------:|----:|---:|--------|
| grok | **1.00** (11/11) | **1.00** (11/11) | 0.00 | **tie** |
| qwen | **0.91** (10/11) | **0.91** (10/11) | 0.00 | **tie** |

Both Qwen arms miss only `test_invalid_config_fail_closed` (invalid body still returns default threshold 3).

## Means

| Arm | Mean |
|-----|-----:|
| control | **0.955** |
| gxp | **0.955** |

**Gap:** **0.000**

## Wins

GXP **0** · control **0** · ties **2**

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **FAIL** |
| Majority GXP wins | **FAIL** |
| No GXP tamper | **PASS** |

### Verdict: **FAIL**

## Interpretation (critical for honest GXP claims)

| Design | Result |
|--------|--------|
| public_green vs GXP (tasks 09, 10) | **PASS** large gaps |
| **unconstrained control vs GXP (this trial)** | **FAIL** gap 0 |

**Conclusion:** Meaningful GXP wins so far depend on a **premature public-green stop** control. Against best-effort tool agents that already read `.ai/` and fix multi-factor bugs, GXP process files do not improve hidden correctness on this fixture/model set.

## Limits

- N=1 task, N=1 seed.  
- Grok both arms used correct reference-quality fills (session).  
- Qwen control still read failures/rules (PROGRAM in workspace) — true “no memory” control would hide `.ai/` (future experiment).

## Follow-ups

1. Optional: control without mounting `.ai/` (harder).  
2. Transcript metrics on public_green PASSes.  
3. Stop over-claiming; keep dual reporting: public_green row + unconstrained row.
