# Experimental Clarifier Topology (Clarification Protocol v0)

Use this when `clarification_protocol: experimental-v0` is active and the task is
high-ambiguity, multi-constraint, or underspecified.

This extends the standard Heavy front-half by inserting an explicit **Clarifier**
step that runs the isolated `gxp-criteria-checker` before any downstream planning
or implementation nodes activate.

Prerequisites:

- Personas installed (`./install-grok-build.ps1 -Force` or project `.grok/personas/`)
- `gxp-criteria-checker.toml` present
- Discover personas: `/personas` in Grok Build

---

## Topology Overview

```
Operator goal
    │
    ▼
┌─────────────────────┐
│  Clarifier node     │  ← gxp-criteria-checker (isolated)
│  (PASS required)    │
└─────────────────────┘
    │ PASS
    ▼
┌─────────────────────┐     ┌─────────────────────┐
│  gxp-researcher     │     │  gxp-architect      │  (parallel, optional)
└─────────────────────┘     └─────────────────────┘
    │
    ▼
Parent synthesizes final brief
    │
    ▼
/plan (operator approval)
    │
    ▼
composer-coder → gxp-verifier → rating
```

Downstream nodes remain inactive until the Clarifier returns **PASS**.

---

## 1. Draft initial brief artifacts

Parent (or any proposer) produces a minimal draft:

- Goal (one sentence)
- 4–8 candidate Ideal State Criteria (tagged)
- Out-of-scope
- Verification plan

Do **not** expand into implementation yet.

---

## 2. Spawn the isolated Criteria Checker (Clarifier)

```text
spawn subagent persona=gxp-criteria-checker  isolation=none
  prompt: |
    Review only the following brief artifacts. Do not see any proposer reasoning.

    Goal:
    <goal>

    Ideal State Criteria:
    <list>

    Out of scope:
    <list>

    Verification plan:
    <plan>

    Evaluate for strict binarity, completeness, residual ambiguity,
    scope fidelity, and verifiability. Output PASS or FAIL + rewrites.
```

**Critical contract:** Pass **only** the four artifacts above. Never pass the proposer’s chain-of-thought.

---

## 3. Gate

- **PASS** → proceed to research / architect / synthesis (steps 4+).
- **FAIL** → apply the rewrite suggestions, re-spawn the checker (max 2 total attempts).
- After 2 failures → escalate to the operator with the full history.

---

## 4. Continue with standard Heavy front-half

Once the checker has returned PASS:

```text
spawn subagent persona=gxp-researcher   isolation=none
spawn subagent persona=gxp-architect    isolation=none
```

Parent synthesizes one coherent plan, then:

```text
/plan <synthesized GXP brief>
```

After operator approval → implementer (`composer-coder`, preferably worktree) → independent `gxp-verifier`.

---

## 5. Measurement

When experimental-v0 is used, record in ratings.jsonl:

- `clarification_protocol: "experimental-v0"`
- number of criteria-checker iterations
- whether residual ambiguity appeared later in Phase 5

Optionally append a lightweight clarification history note under `.ai/clarifications/`.

---

## Anti-patterns

- Giving the criteria-checker the proposer’s full reasoning or intermediate notes
- Skipping the PASS gate and letting research/architect run on unvalidated criteria
- Softening the hard “cannot write 4–8 binary criteria → stop” rule
- Treating the experimental path as default (it remains opt-in)

---

## Relation to standard Heavy

`examples/heavy-front-half.md` remains the default path.  
This file is the experimental extension that inserts the Clarifier node first.
