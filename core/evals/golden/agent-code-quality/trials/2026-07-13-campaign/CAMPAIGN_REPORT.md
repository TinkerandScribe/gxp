# Campaign report — control vs GXP (2026-07-13)

## Setup

| Item | Value |
|---|---|
| Tasks | `01-parse-kv`, `02-slugify`, `03-merge-intervals` |
| Control | One-shot implementation, no brief, **no** mid-loop use of `score_trial` |
| GXP | Written brief (4–8 criteria) + implement + **score_trial as verify** before done |
| Model | Same agent (Grok) for both arms |
| Scorer | `harness/score_trial.py` hidden tests only |

## Results (code quality = correctness)

| Task | Control | GXP | Winner |
|---|---:|---:|---|
| 01-parse-kv | 1.00 (10/10) | 1.00 (10/10) | **tie** |
| 02-slugify | 1.00 (8/8) | 1.00 (8/8) | **tie** |
| 03-merge-intervals | **0.875** (7/8) | **1.00** (8/8) | **gxp** |

**Mean correctness:** control **0.958**, GXP **1.000**  
**Task wins:** GXP 1 · control 0 · ties 2  

### Process (informational only)

| Task | Control process | GXP process |
|---|---|---|
| all three | null (no brief) | 1.0 (brief present + checks) |

Process never overrides correctness in the scorer.

## Interpretation

1. **Harness works for multi-task A/B** — three independent tasks, automatic scoring.  
2. **On this single-agent campaign, GXP did not lose any task** and **won the only non-tie**
   (touching intervals: control used `<` instead of `<=`).  
3. **Cannot claim general proof** that “GXP makes agents write better code”:
   - Same model authored both arms **and** the hidden tests (severe contamination).  
   - Control still scored perfectly on 2/3 tasks — ceiling effect on easy tasks.  
   - N=3 tasks, N=1 seed, N=1 model.

## What would count as stronger proof next

| Upgrade | Why |
|---|---|
| Different model for agent arms than test author | Removes author leakage |
| ≥3 seeds per task (temperature / new sessions) | Variance |
| Harder tasks with lower control ceiling | Room for GXP verify-loop to matter |
| Blind operator (no peeking at hidden tests mid-control) | Fairness |

## Reproduce

```bash
# Rescore frozen trial trees
for t in 01-parse-kv 02-slugify 03-merge-intervals; do
  python core/evals/golden/agent-code-quality/harness/score_trial.py \
    --task $t \
    --result core/evals/golden/agent-code-quality/trials/2026-07-13-campaign/control/$t \
    --out /tmp/c-$t.json
  python core/evals/golden/agent-code-quality/harness/score_trial.py \
    --task $t \
    --result core/evals/golden/agent-code-quality/trials/2026-07-13-campaign/gxp/$t \
    --brief core/evals/golden/agent-code-quality/trials/2026-07-13-campaign/gxp/$t/BRIEF.md \
    --out /tmp/g-$t.json
  python core/evals/golden/agent-code-quality/harness/compare_scores.py \
    --a /tmp/c-$t.json --b /tmp/g-$t.json --label-a control --label-b gxp
done
```

## Bottom line

- **Test developed and run:** yes.  
- **Signal on this campaign:** mild GXP advantage (1 win, 0 losses, 2 ties).  
- **Scientific proof:** not yet — contamination + small N. The **value shipped** is a
  repeatable hidden-test harness so future multi-model runs can settle the question.
