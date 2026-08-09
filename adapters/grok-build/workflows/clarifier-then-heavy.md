# Clarifier-then-Heavy — Grok Build workflow (v1)

**Operator flag required.** This workflow is **opt-in only**.

Activate by setting `clarification_protocol: experimental-v0` in the task brief (or equivalent operator/env/adapter flag). Default is off.

**Runnable orchestration:** [`gxp-heavy-front-half.rhai`](gxp-heavy-front-half.rhai)
with `args.clarification_protocol = "experimental-v0"` runs the isolated clarifier
gate (max 2 FAIL → `await_user`) then the Heavy front-half. Never auto-enable.

When active for high-ambiguity, multi-constraint, or underspecified work, this inserts an isolated criteria-check gate **before** the standard Heavy path.

This is the reusable form of the pattern documented in `examples/experimental-clarifier-topology.md`.

Prerequisites:

- Personas installed (`./install-grok-build.ps1 -Force` or project `.grok/personas/`)
- `gxp-criteria-checker.toml` present
- Discover personas: `/personas` in Grok Build
- Operator must explicitly enable experimental-v0

**No changes to stable `core/workflow.md`.** Experimental path remains strictly opt-in.

Scaffolding tier: standard (default).

---

## Topology overview

```
Operator goal (underspecified)
        │
        ▼
┌───────────────────────┐
│  Clarifier node       │  (parent or dedicated subagent)
│  - draft Goal         │
│  - draft 4–8 ISCs     │
│  - Out-of-scope       │
│  - Verification plan  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ gxp-criteria-checker  │  ← independent context only
│ (isolated maker-check)│
└───────────┬───────────┘
            │
     PASS ──┤── FAIL → rewrite (max 2) → escalate to operator
            │
            ▼
┌───────────────────────┐
│ gxp-researcher +      │
│ gxp-architect         │  (parallel, as in heavy-gxp)
└───────────┬───────────┘
            │
            ▼
       /plan → implement → gxp-verifier → rate
```

---

## 1. Clarifier drafts the brief

Parent (or a light planner) produces only:

- Goal (one sentence)
- 4–8 tagged Ideal State Criteria
- Out of scope
- Verification plan

Do **not** implement or expand scope yet. Mark the brief with `clarification_protocol: experimental-v0`.

```text
# Conceptual
spawn subagent persona=gxp-architect isolation=none
  prompt: |
    Draft a GXP brief only (Goal + 4–8 binary Ideal State Criteria +
    Out-of-scope + Verification plan). Do not research deeply or implement.
    Mark the brief with clarification_protocol: experimental-v0.
```

---

## 2. Isolated Criteria Checker (hard gate)

Spawn the checker with **only** the brief artifacts. Never pass the proposer’s chain-of-thought or intermediate reasoning.

```text
spawn subagent persona=gxp-criteria-checker isolation=none
  prompt: |
    Evaluate the following brief artifacts only:
    <Goal>
    <Ideal State Criteria>
    <Out-of-scope>
    <Verification plan>

    Return PASS or FAIL + concrete rewrite suggestions.
    Do not invent new criteria. Do not implement.
```

- **PASS** → proceed to research / architect synthesis (Heavy path).
- **FAIL** → return rewrites to the Clarifier (max 2 total attempts).
- After 2 FAILs → escalate to the operator with the full clarification history.

---

## 3. Continue with standard Heavy path

Once the criteria-checker returns PASS:

1. Optionally spawn `gxp-researcher` + `gxp-architect` in parallel (as in `heavy-gxp.md`).
2. Parent synthesizes final plan.
3. `/plan` for operator approval.
4. `composer-coder` (worktree) → `gxp-verifier` → rate.

See `heavy-gxp.md` (or `examples/heavy-front-half.md`) for the remaining steps.

---

## Clarifier Ideal State Criteria (for the Clarifier node itself)

When treating Clarifier as a first-class graph node, its only binding criteria are:

- [outcome] Binary brief (Goal + 4–8 Ideal State Criteria + Out-of-scope + Verification plan) is complete
- [outcome] Isolated criteria-checker has returned PASS

Downstream nodes activate only after both are true.

---

## Durable clarification history (recommended)

After the gate, append a short record (e.g. under `.ai/clarifications/<slug>.md` or the ratings notes):

- Questions posed (if any)
- Operator answers
- Discarded assumptions
- Checker iterations and final PASS/FAIL

This becomes shared state for nested sub-graphs or later sessions.

---

## Anti-patterns

- Feeding the proposer’s chain-of-thought into the criteria-checker
- Skipping the isolated checker and going straight to research/architect
- Letting the checker invent new criteria or expand scope
- Treating a thin smoke green as sufficient after implementation
- Auto-activating experimental-v0 without the operator flag

---

## Personas referenced (shipped only)

- gxp-criteria-checker (isolated, brief-artifacts only)
- gxp-researcher
- gxp-architect
- composer-coder
- gxp-verifier

This workflow is docs-only under `adapters/grok-build/`. It does not alter `core/workflow.md`. Experimental remains opt-in; operator flag is required.
