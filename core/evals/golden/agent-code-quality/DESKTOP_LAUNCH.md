# Desktop launch — single prompt for Claude / Cursor apps

**Local only:** seed workspaces under `trials/` on your machine (gitignored).  
Do not commit trial trees, scores, or CAMPAIGN_REPORT packs.

1. Seed a pack (example date tag):

```bash
# from repo root — see scripts/seed-operator-blind.sh for flags
bash core/evals/golden/agent-code-quality/scripts/seed-operator-blind.sh
```

2. Freeze protocol at `trials/<DATE>-operator-blind/PROTOCOL_FROZEN.md` before implement chats.
3. Use the launch prompt below with your repo path as `REPO`.

---

## Single launch prompt (paste into a **new** chat)

Change **`TRIAL_ID`** (1–12) and set **`REPO`** to your clone path. Everything else is read from disk.

```text
You are running ONE implement trial for the GXP blind code-quality campaign.

Open and follow the arm prompt file for this trial (do not improvise a different methodology):

1. Read:
   REPO/core/evals/golden/agent-code-quality/trials/<DATE>-operator-blind/TRIALS.md
2. Find the row where ID = TRIAL_ID (set below).
3. From that row take TOOL, ARM, TASK, and DEST (absolute path).
4. If ARM is control, follow:
   REPO/core/evals/golden/agent-code-quality/prompts/control.md
   If ARM is gxp, follow:
   REPO/core/evals/golden/agent-code-quality/prompts/gxp.md
5. Use these variables:
   TOOL / ARM / TASK / DEST from the TRIALS.md row
   REPO = <absolute path to your gxp clone>
6. Read the task prompt only from:
   REPO/core/evals/golden/agent-code-quality/tasks/TASK/prompt.md
7. Edit files only under DEST (already contains starter code).
8. When finished, say DONE and list files you changed.

TRIAL_ID = 1

Hard rules:
- Do NOT open hidden_tests, reference, scores, other trial DEST folders, or CAMPAIGN_REPORT files.
- Do NOT run score_trial.py.
- GXP arm only: BRIEF.md + HANDOFF.md + implementation files in DEST (no ratings.jsonl, no verify_adhoc.py).
- New chat per trial. Budget ~15 minutes or ~40 tool turns.
```

**Examples:** set `TRIAL_ID = 1` for first control parse-kv; higher IDs per your `TRIALS.md`.

Checklist of IDs: `trials/<DATE>-operator-blind/TRIALS.md` (local).

---

## After all 12 trials (one scoring chat — any agent with shell)

```text
Scoring pass for the operator-blind campaign. Do not implement tasks.

1. Run from REPO:
   bash core/evals/golden/agent-code-quality/scripts/score-operator-blind.sh \
     core/evals/golden/agent-code-quality/trials/<DATE>-operator-blind

2. Read all JSON under that BASE/scores/.

3. Write under the same BASE (local only — do not commit):
   - CAMPAIGN_REPORT.md (correctness table, means, pre-registered PASS/FAIL from PROTOCOL_FROZEN.md)
   - CONTAMINATION.md (what implement chats could see; any extras in DEST)

4. Do not create a git tag, GitHub release, or commit of trials/ unless I explicitly ask.
```

---

## Operator quick order

1. Implement chats with `TRIAL_ID` **1 → N** (one new chat each)  
2. One scoring chat (prompt above)  
3. Keep all outputs under local `trials/` (gitignored)
