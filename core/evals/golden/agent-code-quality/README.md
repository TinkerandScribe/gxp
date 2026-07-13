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

## Layout

```
agent-code-quality/
  README.md                 # this file
  PROTOCOL.md               # how to run a fair A/B trial
  harness/score_trial.py    # automatic scorer
  harness/compare_scores.py
  tasks/
    01-parse-kv/
    02-slugify/
    03-merge-intervals/
  trials/                   # recorded campaign runs (optional)
```

## Latest campaign

See [`trials/2026-07-13-campaign/CAMPAIGN_REPORT.md`](trials/2026-07-13-campaign/CAMPAIGN_REPORT.md)
(control vs GXP, 3 tasks, 1 model seed).

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
