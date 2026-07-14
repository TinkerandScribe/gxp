# Operator notes — 09-rate-limit-service (L2)

## Seed

```bash
# from repo root
TASK=09-rate-limit-service
DEST=core/evals/golden/agent-code-quality/trials/<date>-l2-pilot/results/<model>/<arm>/$TASK
mkdir -p "$DEST"
cp -R core/evals/golden/agent-code-quality/tasks/$TASK/starter/. "$DEST/"
```

## Prompts

| Arm | File |
|-----|------|
| Control (tools, no GXP) | [`prompts/control-tools.md`](../../prompts/control-tools.md) + task `prompt.md` |
| GXP (tools + full workflow) | [`prompts/gxp-tools.md`](../../prompts/gxp-tools.md) + task `prompt.md` |

**Both arms must have the same tool budget** (e.g. shell + edit + read).

## Public verify (agent-visible)

```bash
cd "$DEST"
python -m unittest discover -s tests_public -v
```

Starter is designed so this **already passes** (green trap).

## Score (hidden)

```bash
python core/evals/golden/agent-code-quality/harness/score_trial.py \
  --task 09-rate-limit-service \
  --result "$DEST" \
  --brief "$DEST/BRIEF.md" \
  --out scores/...json
```

## Pre-register (suggested)

Same as other campaigns: mean gap ≥ 0.10 or majority wins; no GXP tamper.
Optional secondary: GXP more often re-reads `.ai/failures` / runs verify (transcript).
