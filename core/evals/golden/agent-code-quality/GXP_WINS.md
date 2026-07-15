# Meaningful GXP wins — established (2026-07-14/15)

**Status:** Goal met. Pre-registered hidden-correctness wins exist under defined conditions.

Primary metric: hidden correctness via `score_trial.py`.  
Success rule: mean(GXP − control) ≥ 0.10 **or** majority pair wins; no GXP tamper.

## PASS campaigns (meaningful wins)

| Trial | Design | Gap | Commit / path |
|-------|--------|----:|---------------|
| `2026-07-14-l2-public-green-vs-gxp` | Stop when public tests green vs full GXP | **+0.42** | `a19703d` |
| `2026-07-14-l2-hardened-pg` | Zero-write public_green + multi-seed GXP (task 09) | **+0.77** | `ee167ae` |
| `2026-07-14-l2-task10-pg-vs-gxp` | Second L2 fixture (circuit breaker), public_green | **+0.68** | `0e1e6c6` |
| `2026-07-14-l2-short-prompt` | Underspec prompt both; Phase 0 available | **+0.14** | `71fbb0a` |
| `2026-07-14-l2-short-no-ai` | Underspec + control lacks `.ai/` | **+0.14** | `e4f4077` |

## FAIL / null results (boundaries)

| Trial | Design | Gap | Meaning |
|-------|--------|----:|---------|
| Easy/hard single-shot 01–08 | Matched models | ~0 | Ceiling / too easy |
| L2 unconstrained (full prompt) | Best-effort tools both | **0** | GXP ≠ automatic win |
| L2 no-`.ai/` full prompt | Strip control memory | **0** | Complete prompt suffices |

## What we can claim

1. **GXP beats premature “public tests green = done”** on multi-factor tool-using tasks (`09-rate-limit-service`, `10-circuit-breaker`), with hardened enforcement and multi-seed support on 09.  
2. **GXP Phase 0 can help under underspecified prompts** (short prompt trials; Grok-driven gap; Qwen often ties after discovering docs).  

## What we must not claim

- GXP always beats unconstrained best-effort agents given the **same complete prompt**.  
- Single-shot interview puzzles prove GXP process lift.  

## Operator index

- Scorecard: [`SCORECARD.md`](SCORECARD.md)  
- Transcript metrics: generate locally under `trials/` (gitignored) via `harness/score_transcript.py`  
- Tasks: `09-rate-limit-service`, `10-circuit-breaker`  

- Prompts: `prompts/control-public-green.md`, `prompts/gxp-tools.md`, `prompt.short.md`  

## Loop policy

The recurring “iterate until meaningful wins” criterion is **satisfied**. Further 60s loops should only run **new pre-registered protocols**, not re-prove public_green.
