# PROTOCOL_FROZEN — 2026-07-14 operator-blind (desktop Claude + Cursor)

**Entrypoint:** `core/evals/golden/agent-code-quality/DESKTOP_LAUNCH.md`  
**Workspaces:** `results/<tool>/<arm>/<task>/` under this directory (starters only).  
**Frozen at:** before implement sessions (operator desktop launch)

## Models / tools

| Label | Product (fill if you change) |
|-------|------------------------------|
| claude | Claude desktop / Claude Code (your default model) |
| cursor | Cursor desktop (your default agent model) |

## Matrix

- Tools: claude, cursor  
- Arms: control, gxp  
- Tasks: 01-parse-kv, 04-safe-join, 05-count-words  
- **12 sessions** (see `TRIALS.md`)

## Budget (per trial)

- ~15 minutes **or** ~40 tool turns  

## Pre-registered success rule

**PASS** if:

1. (GXP mean correctness − control mean ≥ **0.10**), **OR**  
2. GXP wins a majority of task-level comparisons among non-disqualified `scope_ok` trials  

**AND** no GXP trial fails tamper (`no_test_tamper=false`).  
For win eligibility, `scope_ok=false` makes that GXP cell ineligible (counts against majority).

Otherwise **FAIL**. No marketing claim on FAIL or all-1.0 ceiling.

## Contamination

Implement chats only open:

- `prompts/control.md` or `prompts/gxp.md` (via DESKTOP_LAUNCH)  
- `tasks/<TASK>/prompt.md`  
- files under that trial’s `DEST`  

Do **not** open before all 12 claim-done: `hidden_tests/`, `reference/`, `scores/`, other trials’ results, campaign reports.

## Scoring

After all 12:

```bash
bash core/evals/golden/agent-code-quality/scripts/score-operator-blind.sh \
  core/evals/golden/agent-code-quality/trials/2026-07-14-operator-blind
```

Then write `CAMPAIGN_REPORT.md` + `CONTAMINATION.md` here.
