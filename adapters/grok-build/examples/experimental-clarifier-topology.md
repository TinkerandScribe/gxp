# Experimental Clarifier Topology (v0)

Use this when `clarification_protocol: experimental-v0` is active and the task is
high-ambiguity, multi-constraint, or underspecified.

This inserts a **Clarifier** front node that must pass the isolated criteria-checker
before any research/architect/implement work begins.

Prerequisites:

- Personas installed (`./install-grok-build.ps1 -Force` or project `.grok/personas/`)
- `gxp-criteria-checker.toml` present (Experimental Clarification Protocol v0)
- Discover personas: `/personas` in Grok Build

See also: `core/docs/experimental/clarification-protocol-v0.md`

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
│ gxp-architect         │  (parallel, as in heavy-front-half)
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

Do **not** implement or expand scope yet.

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

Spawn the checker with **only** the brief artifacts. Never pass the proposer’s
chain-of-thought or intermediate reasoning.

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

- **PASS** → proceed to research / architect synthesis.
- **FAIL** → return rewrites to the Clarifier (max 2 total attempts).
- After 2 FAILs → escalate to the operator with the full clarification history.

---

## 3. Continue with standard Heavy front-half

Once the criteria-checker returns PASS:

1. Optionally spawn `gxp-researcher` + `gxp-architect` in parallel for deeper work.
2. Parent synthesizes final plan.
3. `/plan` for operator approval.
4. `composer-coder` (worktree) → `gxp-verifier` → rate.

See `heavy-front-half.md` for the remaining steps.

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
