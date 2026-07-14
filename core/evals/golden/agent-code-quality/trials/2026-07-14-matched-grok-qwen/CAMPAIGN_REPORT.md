# CAMPAIGN_REPORT — 2026-07-14 matched Grok + local Qwen

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Scorer:** `score_trial.py` via **Python 3.14** (`C:\Python314\python.exe`)  
**Matrix:** 12 trials (2 models × 2 arms × 3 tasks), **matched model within each row**

## Models (matched)

| Model ID | Engine | Control | GXP |
|----------|--------|---------|-----|
| `qwen` | Ollama `qwen3.6:27b` (Q4_K_M), chat API | same | same |
| `grok` | Session implementer (same fill process both arms) | same | same |

**Tasks:** `01-parse-kv`, `04-safe-join`, `05-count-words`

## Correctness table (Python 3.14)

| Model | Task | Control | GXP | Δ | Winner |
|-------|------|--------:|----:|---:|--------|
| grok | 01-parse-kv | **1.00** (10/10) | **1.00** (10/10) | 0.00 | **tie** |
| grok | 04-safe-join | **1.00** (5/5) | **1.00** (5/5) | 0.00 | **tie** |
| grok | 05-count-words | **1.00** (7/7) | **1.00** (7/7) | 0.00 | **tie** |
| qwen | 01-parse-kv | **1.00** (10/10) | **1.00** (10/10) | 0.00 | **tie** |
| qwen | 04-safe-join | **1.00** (5/5) | **1.00** (5/5) | 0.00 | **tie** |
| qwen | 05-count-words | **1.00** (7/7) | **1.00** (7/7) | 0.00 | **tie** |

All 12: `no_test_tamper=true`, `scope_ok=true`, `disqualified=false`.  
Raw JSON: `scores/<model>-<arm>-<task>.json`.

## Means

| Arm | Mean correctness | Mean primary_code_score |
|-----|-----------------:|------------------------:|
| control | **1.00** | 1.00 |
| gxp | **1.00** | 1.00 |

**Gap (GXP − control correctness):** **0.00** (does **not** meet ≥ 0.10).

## Task-level wins

All six matched pairs: **tie** (correctness equal within 0.05; all scope_ok).

| Metric | Value |
|--------|------:|
| GXP wins | **0** |
| Control wins | **0** |
| Ties | **6** |

## Process (GXP only)

| Cell | process_score | Artifacts |
|------|---------------|-----------|
| grok gxp 01 | 1.0 | BRIEF + HANDOFF |
| grok gxp 04 | 1.0 | BRIEF + HANDOFF |
| grok gxp 05 | 1.0 | BRIEF + HANDOFF |
| qwen gxp 01 | 1.0 | BRIEF + HANDOFF + raw_model_output |
| qwen gxp 04 | 1.0 | BRIEF + HANDOFF + raw_model_output |
| qwen gxp 05 | 1.0 | BRIEF + HANDOFF + raw_model_output |

Control arms: no brief (as designed). Process does **not** count toward the success rule.

## Pre-registered success rule

From PROTOCOL_FROZEN:

> PASS if (mean GXP − mean control correctness ≥ 0.10) OR (GXP wins majority of matched task comparisons), AND no GXP `no_test_tamper=false`.

| Clause | Result |
|--------|--------|
| Mean gap ≥ 0.10 | **FAIL** (0.00) |
| Majority GXP wins | **FAIL** (0 wins, 6 ties) |
| No GXP tamper | **PASS** (all `no_test_tamper=true`) |

### Verdict: **FAIL**

**No marketing claim** that GXP improved hidden-test correctness in this matched Grok+Qwen campaign.

## Implementation notes

1. **Qwen thinking bug:** default Ollama chat for `qwen3.6:27b` puts tokens in `message.thinking` and can leave `message.content` empty when `num_predict` is exhausted by thinking. Remaining/failed cells re-ran with **`think: false`**. Campaign script updated accordingly.
2. **Qwen arms:** single-shot codegen via Ollama (prompt + starter → full module). Control cells 04/05 ran earlier without `think:false` but still produced content; 01 + all GXP cells used `think:false`.
3. **Grok arms:** session-filled from `_grok_fill/` (same correct implement both arms) + GXP BRIEF/HANDOFF. Matched code ⇒ Δ=0 by construction on correctness; process artifacts only differ.
4. **Ceiling:** both models solved all three tasks at 1.0 under both arms — no headroom for GXP lift on this fixture set.

## Honest limits

1. **Ceiling effect** — same as 2026-07-14 operator-blind: fixtures too easy for strong models.
2. **Matched models (good):** unlike operator-blind, control and GXP share model ID within each row.
3. **Grok fill is not a blind independent dual-prompt race** — identical implement bytes for control vs GXP; only process files differ. Qwen is the cleaner independent dual-arm codegen comparison.
4. **N=1 seed per cell** — no variance estimate.
5. **In-repo interview-style tasks** — models may know similar problems from pretraining.
6. **No tag/release** from this campaign unless operator asks.

## Operator follow-ups

- Harder tasks / adversarial starters before next matched claim attempt.
- Prefer independent dual-prompt Grok cells (separate control vs GXP sessions) if claiming process lift on Grok.
- Keep `think: false` (or larger budgets + content extraction from thinking) for Qwen3.x Ollama codegen.
- Document Python ≥3.10 (or 3.14) for `score_trial.py`.
