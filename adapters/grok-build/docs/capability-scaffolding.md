# Capability scaffolding tiers

**Status:** v1 (methodology)
**Related:** `core/workflow.md` Phase 0.5 · `core/templates/task-brief.md` · adapter model-routing

## Why this exists

Model **selection** (which engine runs the task) is not the same as **scaffolding intensity** (how much structure you inject into prompts, skills, and step lists).

Newer frontier models often need *less* corrective scaffolding; older or weaker models need *more*. Treating every run as if the model were mid-tier either hobbles capable models or under-controls weak ones.

GXP keeps **one** workflow. Tiers only modulate load policy and brief style. They never fork process principles.

## Tiers

Exactly three tiers:

| Tier | Default use | Context load | Brief style | Autonomy |
|------|-------------|--------------|-------------|----------|
| **`frontier`** | Proven flagship / current frontier model IDs | Minimal: `PROGRAM.md`, rules, failures, verification commands. Skip long host system prompts / skills **for this run** unless a criterion repeatedly fails without them | High-level goal + 4–8 binary Ideal State Criteria + verification plan | Longer unattended loops OK when verify is strong |
| **`standard`** | Default mid-tier and unknown models | Current GXP defaults (full portable `.ai` / adapter instructions) | Full brief + self-eval gates | Normal GXP loops |
| **`constrained`** | Older, local, or unproven models | Keep host scaffolding, denser guardrails, explicit step hints when criteria alone under-specify | More explicit steps + earlier human gates | Short loops; escalate model/tier faster at Phase 4 |

## Invariants (all tiers)

These do **not** vary by tier:

1. Binary Ideal State Criteria (binding `[outcome]` / `[guardrail]`)
2. Phase 5 verification ladder (deterministic first; optional ontology; then behavioral; then subjective)
3. Phase 4 anti-loop (two failures → reframe; no silent grind)
4. Honest ratings and failure capture
5. Privacy / stakes rails in `core/routing.md`
6. Bounded L3/L4 autonomy — no self-directed scope expansion

**Anti-pattern:** dropping verification or binary criteria on `frontier` “because the model is smart.” Frontier still needs strong exit criteria; it needs *less prompt debt*, not less truth-checking.

## Detection order (fail closed to standard)

1. **Explicit override** — task brief field, operator instruction, or env `GXP_SCAFFOLDING_TIER=frontier|standard|constrained`
2. **Adapter model map** — known model id/name → default tier (dated tables in adapters; revisable after model jumps)
3. **Default `standard`** — if unknown

Never auto-select `frontier` without a known model id **or** an explicit operator/env override.

## Ablation rule

Ablation (deleting or ignoring host `CLAUDE.md`, skills, hooks, long custom instructions for a run or experiment):

- Allowed as an **operator-approved** experiment on `frontier` only (or via `gxp-refine`)
- **Not** silent auto-deletion of host files
- Re-add only what repeatedly fails without it (empirical, not preventive)

## What adapters may specialize

Adapters may:

- Map concrete model IDs to default tiers
- State which files/skills load or skip per tier
- Re-evaluate tier at Phase 4 when escalating/de-escalating models

Adapters must **not**:

- Define a second process that conflicts with `core/workflow.md`
- Ship three full copies of the workflow
- Weaken invariants for any tier

## Relationship to Phase 0.5 model selection

| Axis | Question | Recorded as |
|------|----------|-------------|
| Engine / model | Which tool/model runs the work? | **Strategy/Model** |
| Scaffolding tier | How much structure do we inject? | **Scaffolding tier** |

You may pair a frontier model with `standard` scaffolding (conservative) or a mid model with `constrained` (safer). Pairing a weak model with `frontier` scaffolding is an anti-pattern unless the operator explicitly accepts the risk.

## Optional env

```bash
export GXP_SCAFFOLDING_TIER=standard   # frontier | standard | constrained
```

Projects may document a default in `PROGRAM.md` (e.g. “default scaffolding tier: standard”). Project default still loses to an explicit brief field for a single task.

## Canary

See `core/evals/canaries/capability-scaffolding/README.md` for a same-brief frontier vs constrained comparison recipe.
