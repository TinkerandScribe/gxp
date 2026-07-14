# CAMPAIGN_REPORT — 2026-07-14 operator-blind (desktop Claude + Cursor)

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Checklist:** [`TRIALS.md`](TRIALS.md)  
**Scorer:** `score_trial.py` via **Python 3.14** (`C:\Python314\python.exe`)  
**Matrix:** 12 trials (2 tools × 2 arms × 3 tasks), one model per trial cell  

## Models used (operator-supplied)

| ID | App | Arm | Task | Model |
|----|-----|-----|------|--------|
| 1 | Claude | control | 01-parse-kv | fable |
| 2 | Claude | gxp | 01-parse-kv | opus high |
| 3 | Claude | control | 04-safe-join | sonnet med |
| 4 | Claude | gxp | 04-safe-join | haiku |
| 5 | Claude | control | 05-count-words | sonnet extra |
| 6 | Claude | gxp | 05-count-words | opus extra |
| 7 | Cursor | control | 01-parse-kv | auto |
| 8 | Cursor | gxp | 01-parse-kv | grok 4.5 high fast |
| 9 | Cursor | control | 04-safe-join | gpt 5.6 terra med |
| 10 | Cursor | gxp | 04-safe-join | composer 2.5 |
| 11 | Cursor | control | 05-count-words | composer 2.5 |
| 12 | Cursor | gxp | 05-count-words | gpt 5.6 terra med |

## Correctness table (Python 3.14)

| App | Task | Control model | Control | GXP model | GXP | Δ | Notes |
|-----|------|---------------|--------:|-----------|----:|--:|-------|
| Claude | 01-parse-kv | fable | **1.00** (10/10) | opus high | **1.00** (10/10) | 0.00 | tie; both scope_ok |
| Claude | 04-safe-join | sonnet med | **1.00** (5/5) | haiku | **1.00** (5/5) | 0.00 | tie; GXP has BRIEF only (no HANDOFF) |
| Claude | 05-count-words | sonnet extra | **1.00** (7/7) | opus extra | **1.00** (7/7) | 0.00 | tie |
| Cursor | 01-parse-kv | auto | **1.00** (10/10) | grok 4.5 high fast | **1.00** (10/10) | 0.00 | tie |
| Cursor | 04-safe-join | gpt 5.6 terra med | **1.00** (5/5) | composer 2.5 | **1.00** (5/5) | 0.00 | tie |
| Cursor | 05-count-words | composer 2.5 | **1.00** (7/7) | gpt 5.6 terra med | **1.00** (7/7) | 0.00 | tie |

All 12: `no_test_tamper=true`, `scope_ok=true`, `disqualified=false`.  
Raw JSON: `scores/<tool>-<arm>-<task>.json`.

## Means

| Arm | Mean correctness | Mean primary_code_score |
|-----|-----------------:|------------------------:|
| control | **1.00** | 1.00 |
| gxp | **1.00** | 1.00 |

**Gap (GXP − control correctness):** **0.00** (does **not** meet ≥ 0.10).

## Task-level wins

All six paired comparisons: **tie** (correctness equal within 0.05; all scope_ok).

| Metric | Value |
|--------|------:|
| GXP wins | **0** |
| Control wins | **0** |
| Ties | **6** |

## Process (GXP only)

| Cell | process_score | Brief / handoff |
|------|---------------|-----------------|
| claude gxp 01 | 1.0 | BRIEF + HANDOFF |
| claude gxp 04 | 1.0 | BRIEF only |
| claude gxp 05 | 1.0 | BRIEF + HANDOFF |
| cursor gxp 01 | 1.0 | BRIEF + HANDOFF |
| cursor gxp 04 | 1.0 | BRIEF + HANDOFF |
| cursor gxp 05 | 1.0 | BRIEF + HANDOFF |

Control arms: no brief (as designed). Process does **not** count toward the success rule.

## Pre-registered success rule

From PROTOCOL_FROZEN:

> PASS if (mean gap ≥ 0.10 **or** GXP majority wins) **and** no GXP tamper/scope fail for win eligibility.

| Clause | Result |
|--------|--------|
| Mean gap ≥ 0.10 | **FAIL** (0.00) |
| Majority GXP wins | **FAIL** (0 wins, 6 ties) |
| No GXP tamper/scope fail | **PASS** (all scope_ok / no tamper) |

### Verdict: **FAIL**

**No marketing claim** that GXP improved hidden-test correctness in this operator-blind desktop run.

## Honest limits

1. **Ceiling effect:** every model×arm scored 1.0 on all three tasks — no room for GXP lift.  
2. **Not matched models across arms:** control and GXP used *different* models (e.g. fable vs opus high). Cross-arm Δ confounds process with model strength.  
3. **N=1 seed per cell** — no variance estimate.  
4. **Scorer environment:** first pass via WSL Python 3.8 falsely zeroed count-words (`dict[str,…]` / setUpClass). Canonical scores use Windows **Python 3.14**.  
5. Implement agents may still share web knowledge of common interview-style tasks.

## Operator follow-ups

- Harder tasks or adversarial starters before the next blind.  
- **Matched models:** same model ID for control and GXP on a given task.  
- Document Python ≥3.10 (or 3.14) for `score_trial.py` in eval README.  
- Prefer scoring with the same interpreter the campaign freezes in PROTOCOL.
