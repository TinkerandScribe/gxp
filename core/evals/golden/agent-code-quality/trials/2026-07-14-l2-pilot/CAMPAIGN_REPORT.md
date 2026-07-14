# CAMPAIGN_REPORT — 2026-07-14 L2 tool-using pilot (09-rate-limit-service)

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Task:** `09-rate-limit-service` (multi-file + `.ai/` memory + weak public tests)  
**Scorer:** Python 3.14 `score_trial.py` (package mode)  
**Matrix:** 4 cells (2 models × 2 arms × 1 task)

## Models & arms

| Model | Engine | Control | GXP |
|-------|--------|---------|-----|
| `grok` | Session tool-using implementer | fix + public verify | Phase 0 + BRIEF + fix + verify + HANDOFF |
| `qwen` | Ollama `qwen3.6:27b` + minimal tool loop (`run-l2-qwen-tools.py`, think=false) | tools, no formal brief | tools + BRIEF (+ HANDOFF if written) |

## Correctness (matched pairs)

| Model | Task | Control | GXP | Δ | Winner |
|-------|------|--------:|----:|---:|--------|
| grok | 09-rate-limit-service | **1.00** (12/12) | **1.00** (12/12) | 0.00 | **tie** |
| qwen | 09-rate-limit-service | **0.92** (11/12) | **0.92** (11/12) | 0.00 | **tie** |

All cells: `no_test_tamper=true`, `scope_ok=true` (after allowing agent telemetry files).

### Imperfect cells (both Qwen arms)

Failed only: `test_invalid_config_fail_closed` (invalid file body still returned defaults / non-zero max).  
Missing-file fail-closed: **pass** on both Qwen arms.

Grok process (GXP): `process_score=1.0`.  
Qwen GXP: `process_score=1.0` (BRIEF present).

## Means

| Arm | Mean correctness |
|-----|-----------------:|
| control | **0.958** |
| gxp | **0.958** |

**Gap (GXP − control):** **0.000**

## Wins

| Metric | Value |
|--------|------:|
| GXP wins | **0** |
| Control wins | **0** |
| Ties | **2** |

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **FAIL** |
| Majority GXP wins | **FAIL** |
| No GXP tamper | **PASS** |

### Verdict: **FAIL**

No claim that GXP improved hidden correctness on this pilot.

## What this pilot *did* prove (design)

1. **L2 is not a pure ceiling for local Qwen** — 0.92 not 1.0; multi-factor config edge still bites.  
2. **Green-trap public tests are real** — starter public tests pass; agents that only “make public green” can still miss hidden factors (Qwen almost full).  
3. **Tool use works** — Qwen loop listed/read `.ai/`, rewrote `service/*`, ran unittest, wrote extra public tests.  
4. **Grok session still perfects** both arms when it uses tools + prompt carefully.  
5. **Scope scorer** must allow tool telemetry (`agent_tool_log.jsonl`, `ERROR.txt`, …) or L2 agents false-fail scope.

## Limits

- N=1 task, N=1 seed per cell.  
- Grok is not a blind separate product UI; same operator session class.  
- Qwen tool loop is minimal JSON-action (not full desktop agent).  
- GXP did not outperform control here (identical correctness).  
- Qwen GXP hit max steps without `done` once; still wrote code.

## Follow-ups

- Multi-seed L2; force incomplete first public-only checkpoint.  
- Stronger invalid-config trap in public self-check agents invent.  
- Transcript metric: `phase0_hit` / `tool_verify_ran`.  
- Second L2 task for majority-win statistics.
