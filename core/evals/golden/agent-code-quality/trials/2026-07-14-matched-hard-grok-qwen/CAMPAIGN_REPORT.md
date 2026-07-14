# CAMPAIGN_REPORT — 2026-07-14-matched-hard-grok-qwen

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Pack:** hard tasks **06-lru-ttl**, **07-deep-merge**, **08-line-chunker**  
**Scorer:** Python 3.14 (`C:\Python314\python.exe`) `score_trial.py`  
**Matrix:** 12 cells (2 models × 2 arms × 3 tasks), **matched model within each row**

## Models

| ID | Engine | Notes |
|----|--------|--------|
| `qwen` | Ollama `qwen3.6:27b` | single-shot chat, **`think: false`** |
| `grok` | Session implementer | control: direct code; GXP: BRIEF + code (same session class) |

## Correctness (matched pairs)

| Model | Task | Control | GXP | Δ | Winner |
|-------|------|--------:|----:|---:|--------|
| grok | 06-lru-ttl | **1.00** (12/12) | **1.00** (12/12) | 0.00 | **tie** |
| grok | 07-deep-merge | **1.00** (16/16) | **1.00** (16/16) | 0.00 | **tie** |
| grok | 08-line-chunker | **1.00** (14/14) | **1.00** (14/14) | 0.00 | **tie** |
| qwen | 06-lru-ttl | **1.00** (12/12) | **1.00** (12/12) | 0.00 | **tie** |
| qwen | 07-deep-merge | **1.00** (16/16) | **1.00** (16/16) | 0.00 | **tie** |
| qwen | 08-line-chunker | **1.00** (14/14) | **0.93** (13/14) | **−0.07** | **control** |

All 12: `no_test_tamper=true`, `scope_ok=true`, `disqualified=false`.  
JSON: `scores/<model>-<arm>-<task>.json`.

### Sole imperfect cell

`qwen` / **gxp** / `08-line-chunker`: failed  
`test_max_line_on_buffer_without_delim` (no `ValueError` when buffer exceeds `max_line` without a delimiter).  
Process score still 1.0 (brief present). Correctness process does not override code score.

## Means

| Arm | Mean correctness |
|-----|-----------------:|
| control | **1.000** |
| gxp | **0.988** |

**Gap (GXP − control):** **−0.012** (does **not** meet ≥ 0.10).

## Task-level wins

| Metric | Value |
|--------|------:|
| GXP wins | **0** |
| Control wins | **1** |
| Ties | **5** |

## Process (GXP only)

| Cell | process_score |
|------|---------------|
| grok gxp 06/07/08 | 1.0 each (BRIEF + HANDOFF) |
| qwen gxp 06/07/08 | 1.0 each (BRIEF + raw_model_output) |

Process does **not** count toward the success rule.

## Pre-registered success rule

> PASS if (mean gap ≥ 0.10 **or** GXP majority wins) **and** no GXP tamper.

| Clause | Result |
|--------|--------|
| Mean gap ≥ 0.10 | **FAIL** (−0.012) |
| Majority GXP wins | **FAIL** (0 vs 1 control) |
| No GXP tamper | **PASS** |

### Verdict: **FAIL**

**No marketing claim** that GXP improved hidden-test correctness on this hard pack.

## What this run *did* show

1. **Hard pack broke pure all-1.0 ceiling for Qwen GXP on one cell** (0.93 vs 1.00) — headroom exists, but not in favor of GXP here.  
2. **Grok session implementer still perfects all three** under both arms — strong model + clear multi-rule prompt is enough.  
3. **Matched models** — control and GXP share model ID within each row (design OK).  
4. **Single-shot Ollama GXP** can hurt slightly (extra brief tokens / different extraction path) without tool-using verify loops.

## Honest limits

1. Grok fills are session-orchestrator implementations (prompt-constrained, not blind separate desktop apps).  
2. N=1 seed per cell.  
3. Hard pack still often 1.0 for capable models; need adversarial seeds, multi-turn tool budgets, or harder tasks for GXP verify-loop hypotheses.  
4. No release tag.

## Operator follow-ups

- Multi-seed incomplete/adversarial starters on 06–08.  
- Tool-using GXP arm (write tests, run self-checks) vs single-shot control.  
- Or harder tasks (parser + state machine + protocol) if single-shot still ceilings.
