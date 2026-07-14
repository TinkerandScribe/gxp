# Implement arm — CONTROL (no GXP)

**Operator starts the chat with:**

```text
Follow core/evals/golden/agent-code-quality/prompts/control.md

TOOL=<claude|cursor>
ARM=control
TASK=<01-parse-kv|04-safe-join|05-count-words|…>
DEST=<absolute path to trial result dir, already seeded from starter>
REPO=<absolute path to gxp repo root>
```

---

## Instructions for the implementer (you)

You are implementing a small coding task. **Do not** use GXP, task briefs, or any workflow methodology docs.

### Inputs you must load

1. Read the task prompt file (and nothing else under `tasks/` except this path):

   `{REPO}/core/evals/golden/agent-code-quality/tasks/{TASK}/prompt.md`

2. Your **only** editable project root is:

   `{DEST}`

   It was pre-seeded from the task `starter/`. Implement the deliverable **there**.

### Rules

- Edit only under `{DEST}`.
- Do **not** create or modify any `hidden_tests` directory.
- Do **not** open or request: `reference/`, `hidden_tests/`, `score_trial.py`, other trial results, or campaign reports.
- Do **not** explore the rest of the gxp repo for solutions.
- Stop when you believe the task is done. Briefly list what you changed.

### Budget

About **15 minutes** or **~40 tool turns**, whichever comes first (unless the operator stated another limit in `PROTOCOL_FROZEN.md`).

### Done

Say “DONE” and summarize files touched. Do not run the official scorer.
