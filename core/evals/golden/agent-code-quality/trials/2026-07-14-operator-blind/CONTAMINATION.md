# CONTAMINATION.md — 2026-07-14 operator-blind

## Who could see hidden tests / reference

| Actor | Access |
|-------|--------|
| Implement desktop sessions (12) | Instructed via `DESKTOP_LAUNCH.md` + `prompts/control.md` or `prompts/gxp.md` + task `prompt.md` + DEST only. Forbidden: `hidden_tests/`, `reference/`, scores, other trials. |
| Operator (human) | Launched sessions; provided model list after runs. |
| Scoring session (this Grok run) | Opened results and ran `score_trial.py` **after** all implement claims; read scores for report. |

## Protocol integrity

| Item | Status |
|------|--------|
| PROTOCOL_FROZEN before implement | Yes (desktop launch pack) |
| Separate chat per trial | Yes (operator desktop) |
| Models recorded | Yes (operator list mapped to TRIAL_ID 1–12) |
| Cross-arm solution paste | Not observed in trees |
| Hidden tests in implement prompts | Not in launch pack |
| Tag / release from this scoring pass | No |

## Model assignment (operator)

See CAMPAIGN_REPORT model table. Note: **arms are not model-matched** (different model per cell).

## Breaches / notes

1. **WSL Python 3.8 first score pass** produced false failures on `05-count-words` (`'type' object is not subscriptable` in setUpClass / annotations). Discarded; rescored with **Python 3.14**. Not implement-agent contamination.  
2. **Claude GXP 04-safe-join** has `BRIEF.md` but no `HANDOFF.md` (process incomplete vs prompt; still scope_ok and correctness 1.0).  
3. **`__pycache__`** may appear under results after scoring; not agent deliverables.  

## Compromised trials

None for test-leak.  
No `scope_ok=false` / tamper disqualifies on this run.
