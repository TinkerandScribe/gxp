# Golden eval: do agents write better code?

This harness measures **code quality via automated tests**, not process
completeness and not self-rating. Use it to compare conditions such as:

| Condition | Agent receives |
|---|---|
| **Control** | Task prompt + starter only |
| **GXP** | Task prompt + starter + instruction to follow GXP (`core/workflow.md` or adapter workflow) with a written brief before coding |
| **GXP+verify** | Same as GXP, plus must run the task’s `verify.sh` / tests before claiming done |

## What “better code” means here

For each trial, the scorer produces objective metrics:

| Metric | How measured |
|---|---|
| **correctness** | Fraction of *hidden* tests passed |
| **no_test_tamper** | Hidden test files unchanged (hash match) |
| **scope** | Only allowed paths modified under the task package |
| **process** *(optional)* | Separate checklist if a brief/handoff was produced — **not** mixed into correctness |

A condition “wins” on code quality only if **correctness** is higher with equal or
better `no_test_tamper` and `scope`. Process scores never override test failures.

## Operator entrypoint (Claude / Cursor)

**Tell the agent:**

> Follow `core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md` end to end.

| File | Role |
|------|------|
| [`OPERATOR_RUNBOOK.md`](OPERATOR_RUNBOOK.md) | Seed → 12 implement chats → score → report |
| [`prompts/control.md`](prompts/control.md) | One implement session (no GXP) |
| [`prompts/gxp.md`](prompts/gxp.md) | One implement session (GXP) |
| [`scripts/seed-operator-blind.sh`](scripts/seed-operator-blind.sh) | Create workspaces |
| [`scripts/score-operator-blind.sh`](scripts/score-operator-blind.sh) | Score all results |

## Layout

```
agent-code-quality/
  README.md
  OPERATOR_RUNBOOK.md       # operator entrypoint
  PROTOCOL.md
  prompts/control.md
  prompts/gxp.md
  scripts/seed-operator-blind.sh
  scripts/score-operator-blind.sh
  harness/score_trial.py
  harness/compare_scores.py
  tasks/
    01-parse-kv/ … 05-count-words/
  trials/
```

## Latest campaigns

| Campaign | Path |
|---|---|
| Single-seed control vs GXP | [`trials/2026-07-13-campaign/CAMPAIGN_REPORT.md`](trials/2026-07-13-campaign/CAMPAIGN_REPORT.md) |
| Multi-seed (3 incomplete controls × 3 tasks) + multi-runner selftest attestation | [`trials/2026-07-13-multiseed/CAMPAIGN_REPORT.md`](trials/2026-07-13-multiseed/CAMPAIGN_REPORT.md) |

Regenerate multi-seed: `python scripts/run-code-quality-seeds.py`

## Quick self-test (proves the scorer works)

From the **repo root**:

```bash
# Starter should score poorly on correctness
python core/evals/golden/agent-code-quality/harness/score_trial.py \
  --task 01-parse-kv \
  --result core/evals/golden/agent-code-quality/tasks/01-parse-kv/starter

# Reference solution should score full correctness
python core/evals/golden/agent-code-quality/harness/score_trial.py \
  --task 01-parse-kv \
  --result core/evals/golden/agent-code-quality/tasks/01-parse-kv/reference
```

## Fair comparison (operator / outer agent)

See [`PROTOCOL.md`](PROTOCOL.md). Summary:

1. Copy `tasks/<id>/starter` to two clean work dirs (`control/`, `gxp/`).  
2. Run the **same** model/tooling twice with only the condition prompt differing.  
3. Score both result trees with `score_trial.py`.  
4. Record JSON rows in `trials/` (gitignored or committed as results).  
5. Verdict from **correctness** delta across ≥3 tasks or ≥3 seeds when possible.

## Limitations (read before claiming proof)

- One task is a **canary**, not a universe of software engineering.  
- Same model on both arms still shares priors; use multiple tasks/seeds.  
- Agents that see hidden tests can overfit — keep `hidden_tests/` out of the
  prompt and out of the agent’s context when your tool allows.  
- This does **not** measure taste, architecture elegance, or security beyond tests.
