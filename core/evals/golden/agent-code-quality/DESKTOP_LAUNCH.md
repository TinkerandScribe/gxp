# Desktop launch — single prompt for Claude / Cursor apps

Workspaces for **2026-07-14** are already seeded.  
Protocol is frozen at  
`trials/2026-07-14-operator-blind/PROTOCOL_FROZEN.md`.

---

## Single launch prompt (paste into a **new** chat)

Change only **`TRIAL_ID`** (1–12). Everything else is read from disk.

```text
You are running ONE implement trial for the GXP blind code-quality campaign.

Open and follow the arm prompt file for this trial (do not improvise a different methodology):

1. Read:
   C:\Users\Reepicheep\Claude\gxp-public\core\evals\golden\agent-code-quality\trials\2026-07-14-operator-blind\TRIALS.md
2. Find the row where ID = TRIAL_ID (set below).
3. From that row take TOOL, ARM, TASK, and DEST (absolute path).
4. If ARM is control, follow:
   C:\Users\Reepicheep\Claude\gxp-public\core\evals\golden\agent-code-quality\prompts\control.md
   If ARM is gxp, follow:
   C:\Users\Reepicheep\Claude\gxp-public\core\evals\golden\agent-code-quality\prompts\gxp.md
5. Use these variables:
   TOOL / ARM / TASK / DEST from the TRIALS.md row
   REPO = C:\Users\Reepicheep\Claude\gxp-public
6. Read the task prompt only from:
   REPO\core\evals\golden\agent-code-quality\tasks\TASK\prompt.md
7. Edit files only under DEST (already contains starter code).
8. When finished, say DONE and list files you changed.

TRIAL_ID = 1

Hard rules:
- Do NOT open hidden_tests, reference, scores, other trial DEST folders, or CAMPAIGN_REPORT files.
- Do NOT run score_trial.py.
- GXP arm only: BRIEF.md + HANDOFF.md + implementation files in DEST (no ratings.jsonl, no verify_adhoc.py).
- New chat per trial. Budget ~15 minutes or ~40 tool turns.
```

**Examples:** set `TRIAL_ID = 1` in Claude for first control parse-kv; `TRIAL_ID = 8` in Cursor for cursor gxp parse-kv.

Checklist of IDs: `trials/2026-07-14-operator-blind/TRIALS.md`

---

## After all 12 trials (one scoring chat — any agent with shell)

```text
Scoring pass for the operator-blind campaign. Do not implement tasks.

1. Run from REPO C:\Users\Reepicheep\Claude\gxp-public:
   bash core/evals/golden/agent-code-quality/scripts/score-operator-blind.sh \
     core/evals/golden/agent-code-quality/trials/2026-07-14-operator-blind

2. Read all JSON under that BASE/scores/.

3. Write under the same BASE:
   - CAMPAIGN_REPORT.md (correctness table, means, pre-registered PASS/FAIL from PROTOCOL_FROZEN.md)
   - CONTAMINATION.md (what implement chats could see; any extras in DEST)

4. Do not create a git tag or GitHub release unless I explicitly ask.
5. Commit to main only if I ask.
```

---

## Operator quick order

1. Claude desktop: chats with `TRIAL_ID` **1 → 6**  
2. Cursor desktop: chats with `TRIAL_ID` **7 → 12**  
3. One scoring chat (prompt above)  
