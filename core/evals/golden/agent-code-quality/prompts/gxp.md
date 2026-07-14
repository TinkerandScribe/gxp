# Implement arm — GXP

**Operator starts the chat with:**

```text
Follow core/evals/golden/agent-code-quality/prompts/gxp.md

TOOL=<claude|cursor>
ARM=gxp
TASK=<01-parse-kv|04-safe-join|05-count-words|…>
DEST=<absolute path to trial result dir, already seeded from starter>
REPO=<absolute path to gxp repo root>
```

---

## Instructions for the implementer (you)

Follow **GXP** for this coding task (full workflow unless the task is truly trivial).

### Inputs you must load

1. Methodology:

   `{REPO}/core/workflow.md`

2. Task prompt (only this path under `tasks/`):

   `{REPO}/core/evals/golden/agent-code-quality/tasks/{TASK}/prompt.md`

3. Your **only** editable project root is:

   `{DEST}`

   Pre-seeded from the task `starter/`. Implement **there**.

### Required process

1. **Before coding:** write `{DEST}/BRIEF.md` with:
   - Goal  
   - **4–8 binary** Ideal State Criteria  
   - Out of scope  
   - Verification plan  

2. Implement the deliverable (smallest change that meets the brief).

3. **Anti-loop:** if the same approach fails twice, stop, note the dead end, change strategy.

4. **Before claiming done:** run your own deterministic checks (e.g. small Python snippets).  
   You will **not** receive the official hidden tests.

5. Write `{DEST}/HANDOFF.md`: what changed / what you verified / what is not done.

### Hard rules (scope)

Allowed in `{DEST}`:

- Implementation file(s) required by the task prompt  
- `BRIEF.md`  
- `HANDOFF.md`  

**Do not** write into `{DEST}`:

- `ratings.jsonl`  
- `verify_adhoc.py` or other helper scripts  
- `hidden_tests/`  
- copies of `core/` or the rest of the monorepo  

(Extra non-`.md` files can fail the scorer’s `scope_ok` check even if tests pass.)

### Forbidden

- Opening `hidden_tests/`, `reference/`, `score_trial.py`, other trial trees, or campaign reports  
- Requesting the official test suite or a reference solution  

### Budget

Same as control: about **15 minutes** or **~40 tool turns**, unless operator says otherwise.

### Done

Say “DONE”, point at `BRIEF.md` + `HANDOFF.md` + impl files. Do not run the official scorer.
