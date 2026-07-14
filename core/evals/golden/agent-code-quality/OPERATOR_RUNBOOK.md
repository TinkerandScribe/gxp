# Operator runbook — blind control vs GXP (Claude + Cursor)

**Tell the agent:**  
> Follow `core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md` end to end. Do not create a git tag or GitHub release unless I explicitly ask.

This file is the single entrypoint for an **operator-led** M6-style blind campaign.  
Implement chats only open `prompts/control.md` or `prompts/gxp.md` plus one task `prompt.md`.

Related: [`PROTOCOL.md`](PROTOCOL.md) · brief [`../../tasks/blind-multi-model-code-quality-campaign.md`](../../tasks/blind-multi-model-code-quality-campaign.md)

---

## Roles

| Role | Who | What they open |
|------|-----|----------------|
| **Operator** | You + one agent with shell (Claude Code / Cursor / Grok on the gxp repo) | **This runbook** |
| **Implementer** | Fresh chat per trial (Claude or Cursor) | `prompts/control.md` or `prompts/gxp.md` only |

Implementers must **never** open `hidden_tests/`, `reference/`, `scores/`, or prior trial reports.

---

## Default matrix

| Tool | Arms | Tasks |
|------|------|--------|
| `claude` | control, gxp | `01-parse-kv`, `04-safe-join`, `05-count-words` |
| `cursor` | control, gxp | same three |

= **12 implement sessions**, then one score + report pass.

Optional: all five tasks (`02-slugify`, `03-merge-intervals` too) → 20 sessions.

---

## Pre-registered success rule (freeze before implement)

Write this into `trials/<DATE>-operator-blind/PROTOCOL_FROZEN.md` **before** the first implement chat:

> **PASS** if  
> (GXP mean correctness − control mean ≥ **0.10**)  
> **OR** (GXP wins a majority of task-level comparisons among non-disqualified `scope_ok` trials)  
> **AND** no GXP trial has `no_test_tamper=false` or (for win eligibility) `scope_ok=false`.  
> Otherwise **FAIL**. No marketing claim on FAIL or on ceiling (all 1.0).

Also record: models/tools, budget (default 15 min or ~40 turns), task list, date.

---

## Phase A — Operator setup

From **gxp repo root**:

```bash
# Git Bash / WSL
bash core/evals/golden/agent-code-quality/scripts/seed-operator-blind.sh
# prints BASE=... path; export or copy DATE from output
```

PowerShell:

```powershell
bash core/evals/golden/agent-code-quality/scripts/seed-operator-blind.sh
```

This creates:

```text
core/evals/golden/agent-code-quality/trials/<DATE>-operator-blind/
  PROTOCOL_FROZEN.md   # template — fill models/budget before implement
  results/<tool>/<arm>/<task>/   # starter copies only
  scores/
```

Fill `PROTOCOL_FROZEN.md` (models, budget). Do **not** start implement chats until that file exists and is filled.

---

## Phase B — Implement sessions (you open 12 chats)

For each row in the checklist below:

1. Open a **new** Claude or Cursor chat (match the Tool column).  
2. Say only:

```text
Follow core/evals/golden/agent-code-quality/prompts/<ARM>.md

Set:
  TOOL=<claude|cursor>
  ARM=<control|gxp>
  TASK=<task-id>
  DEST=<absolute path to results/TOOL/ARM/TASK>
  REPO=<absolute path to gxp repo root>

Read the task prompt from:
  REPO/core/evals/golden/agent-code-quality/tasks/TASK/prompt.md

Then implement only under DEST.
```

3. When the implementer stops, **do not coach**. Tick the row and move on.

### Checklist

| # | TOOL | ARM | TASK | Done |
|---|------|-----|------|------|
| 1 | claude | control | 01-parse-kv | ☐ |
| 2 | claude | gxp | 01-parse-kv | ☐ |
| 3 | claude | control | 04-safe-join | ☐ |
| 4 | claude | gxp | 04-safe-join | ☐ |
| 5 | claude | control | 05-count-words | ☐ |
| 6 | claude | gxp | 05-count-words | ☐ |
| 7 | cursor | control | 01-parse-kv | ☐ |
| 8 | cursor | gxp | 01-parse-kv | ☐ |
| 9 | cursor | control | 04-safe-join | ☐ |
| 10 | cursor | gxp | 04-safe-join | ☐ |
| 11 | cursor | control | 05-count-words | ☐ |
| 12 | cursor | gxp | 05-count-words | ☐ |

**DEST example (Windows):**  
`C:\Users\Reepicheep\Claude\gxp-public\core\evals\golden\agent-code-quality\trials\2026-07-14-operator-blind\results\claude\control\01-parse-kv`

---

## Phase C — Score (operator agent with shell)

After all 12 claim done, in a **scoring** session (not an implement session):

```text
Follow core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md Phase C only.
BASE is core/evals/golden/agent-code-quality/trials/<DATE>-operator-blind
Run scripts/score-operator-blind.sh with that BASE (or the bash block in the script header).
Do not open implement chats. Write CAMPAIGN_REPORT.md and CONTAMINATION.md under BASE.
Do not create a git tag or GitHub release unless I explicitly ask.
```

Or run:

```bash
bash core/evals/golden/agent-code-quality/scripts/score-operator-blind.sh \
  core/evals/golden/agent-code-quality/trials/<DATE>-operator-blind
```

Then have an agent write `CAMPAIGN_REPORT.md` + `CONTAMINATION.md` from the score JSONs (same structure as `trials/2026-07-13-blind/`).

---

## Phase D — Commit (optional)

Only if you want artifacts on `main`:

```text
Commit the operator-blind trial tree (exclude **/__pycache__ and *.pyc).
Update ROADMAP M6 status if the pre-registered rule is evaluated.
Do not tag or create a GitHub release unless I explicitly ask.
```

---

## Contamination rules (hard)

| Do | Don't |
|----|--------|
| New chat per trial | Reuse a control chat for GXP |
| Only `prompts/*.md` + task `prompt.md` + `DEST` | Open `hidden_tests/` or `reference/` before all 12 done |
| GXP: only impl + `BRIEF.md` + `HANDOFF.md` | GXP: `ratings.jsonl`, `verify_adhoc.py`, random scripts in DEST |
| Score only after all claim-done | Coach after peeking at scores |

---

## Quick “what do I say?”

| You want… | Say to the agent |
|-----------|------------------|
| Seed workspaces | `Run core/evals/golden/agent-code-quality/scripts/seed-operator-blind.sh and fill PROTOCOL_FROZEN.md` |
| One implement trial | `Follow core/evals/golden/agent-code-quality/prompts/control.md` (or `gxp.md`) with TOOL=… ARM=… TASK=… DEST=… REPO=… |
| Score + report | `Follow OPERATOR_RUNBOOK.md Phase C for BASE=…` |
| Full campaign as operator | `Follow core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md end to end` |
