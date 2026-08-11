---
name: soft-structure-prompt
description: Redesign a user prompt using Soft Hierarchy Prompt Optimizer (SHPO) principles — hierarchical continuous concept distributions, Soft Thinking, adaptive depth, and high-leverage prioritization. Use when the user says "soft-structure this", "apply soft hierarchy", "rewrite with soft thinking", "SHPO this prompt", "make this hierarchical continuous", or when preparing a complex multi-axis reasoning task (especially before GXP Phase 0/1). Returns only the redesigned prompt; does not execute the task.
---

# Soft Hierarchy Prompt Optimizer (soft-structure-prompt)

Take the user's original prompt (or task description) and rewrite it so the model is guided to reason with:

1. **Soft high-level concept distributions** — hold multiple candidate framings as continuous mixtures instead of locking a single discrete interpretation early.
2. **Hierarchical structure** — establish the overall picture / binding constraints first; expand only the highest-leverage points.
3. **Adaptive depth** — allocate deeper refinement only where it most improves the outcome; keep secondary axes lighter.
4. **Continuous soft mixtures of options** — prefer ranked continuous evaluations over hard early choices when multiple valid paths exist.

## When to use

- Complex, multi-axis analysis or planning tasks.
- Preparing a prompt that will feed a GXP brief or Ideal State Criteria.
- Any time the user wants richer hierarchical continuous reasoning without changing the factual goal.

## Procedure

1. Read the original prompt carefully. Identify the core goal, the main performance/constraint axes, and any explicit success criteria.
2. Rewrite the prompt using this skeleton (adapt freely, keep it concise):

```
[Core goal statement]

First form soft high-level concept distributions over the main axes:
- [axis 1]
- [axis 2]
- [axis 3 ...]

Hierarchical structure: establish the overall picture and binding constraints under [context] before expanding critical failure or opportunity points.

Maintain continuous soft mixtures of alternative approaches; allocate deeper refinement only to the highest-leverage practical decisions that satisfy [constraints or Ideal State Criteria if present].

Then produce [the requested output form].
```

3. Preserve every concrete requirement, constraint, and success criterion from the original. Do not invent new scope.
4. Output **only** the redesigned prompt (plus a one-line note of what changed if useful). Do not solve the task itself.

## Design principles (do not violate)

- Soft / continuous first, discrete commitment later.
- Hierarchy: overall → binding constraints → ranked levers → details.
- Adaptive depth: more tokens only on highest-impact points.
- Stay compatible with binary Ideal State Criteria — this skill improves the *thinking* that produces criteria; it does not replace binary verification.
- Keep the rewritten prompt shorter or only modestly longer than the original.

## What this skill is NOT

- Not a full GXP workflow runner.
- Not a general answer generator — it only rewrites the prompt.
- Not for trivial single-axis questions (just answer those normally).

## Example transformation

**Original**  
Analyze the efficiency of the hybrid greenhouse design for Goshen, NB. Cover thermal performance, structural integrity, light utilization, and operational viability. Suggest improvements.

**Soft-structure version**  
Analyze the efficiency of the hybrid greenhouse design for Goshen, NB. First form soft high-level concept distributions over the main performance axes (thermal, structural, light, operational). Hierarchical structure: establish the overall efficiency picture under local climate constraints before expanding critical failure or opportunity points. Maintain continuous soft mixtures of improvement options; allocate deeper refinement only to the highest-leverage practical changes that stay passive-first. Then produce a structured assessment against the criteria.

## Integration notes

Optional front-end for GXP Phase 0 / Phase 1. Can be invoked before drafting Ideal State Criteria to improve hierarchical clarity while leaving binary verification rules unchanged.
