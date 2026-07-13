# Protocol — fair A/B code-quality trial

## Goal

Estimate whether condition B produces **better code** than condition A on frozen
tasks, using **hidden automated tests** as the ground truth.

## Prerequisites

- Same model / tool version on both arms (or document the difference).  
- Clean worktrees; no copying solutions between arms.  
- Operator does not paste hidden tests into the agent context.

## Conditions (recommended default)

### Arm A — Control

System / user message includes:

1. Contents of `tasks/<id>/prompt.md`  
2. The `starter/` tree (or path to it)  
3. Explicit: “Do not modify files under `hidden_tests/` if present.”  
4. **No** GXP workflow file.

### Arm B — GXP

Same as A, plus:

1. “Follow GXP in `core/workflow.md` (or the installed adapter workflow).”  
2. “Before coding: write a brief with 4–8 binary Ideal State Criteria.”  
3. “Before claiming done: run the verification commands you defined; prefer
   deterministic checks.”  
4. Optionally attach `core/workflow.md` (full) — same attachment for every GXP run.

Do **not** attach this PROTOCOL, hidden tests, or the reference solution to either arm.

## Steps per task

1. `cp -R tasks/<id>/starter /tmp/trial-<arm>-<task>/`  
2. Point the agent at that directory as the only editable project root.  
3. Let the agent work until it claims done or hits a time/tool budget you set
   **in advance** (same budget both arms).  
4. Score:

```bash
python core/evals/golden/agent-code-quality/harness/score_trial.py \
  --task <id> \
  --result /tmp/trial-<arm>-<task> \
  --out /tmp/trial-<arm>-<task>/score.json
```

5. If GXP arm produced a brief, optionally score process with
   `--brief path/to/brief.md` (does not change correctness).

## Aggregation rules

For each task, record `correctness` ∈ [0,1], `no_test_tamper` ∈ {0,1}, `scope_ok` ∈ {0,1}.

**Disqualify** a trial if `no_test_tamper == 0` (agent edited hidden tests).

**Primary winner** on a task: higher `correctness` among non-disqualified trials
with `scope_ok == 1`. Ties if `|Δ| < 0.05`.

**Campaign winner** (when you have N tasks or N seeds):

- Count task-level wins for GXP vs control.  
- Report mean correctness ± range.  
- **Do not** claim proof from a single task/single seed.

Suggested minimum for a cautious claim: **≥3 tasks or ≥3 independent seeds**
on the same task with the same model.

## Contamination controls

| Risk | Mitigation |
|---|---|
| Agent saw reference | Never mount `reference/` into the trial workspace |
| Agent saw hidden tests | Don’t include in prompt; scorer injects tests at grade time |
| Operator steers after peeking at tests | Freeze prompts; no mid-trial rubric edits |
| Same-session bleed | New session (or new worktree) per arm when possible |
| Overfitting over time | Add new tasks; retire leaked ones |

## What this can prove

- Under these tasks and this model, GXP arm **passed more hidden tests**.  
- Agents under GXP **tampered less** or **scoped edits better** (if metrics differ).

## What this cannot prove

- Universal superiority of GXP for all models/tasks.  
- Better comments, API design, or untested requirements.
