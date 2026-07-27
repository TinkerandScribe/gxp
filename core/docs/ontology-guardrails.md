# Agentic Ontology Guardrails (Coyle Pattern)

**Status:** Experimental design (feature/agentic-ontology-guardrails)
**Inspired by:** Frank Coyle — "Why Agentic Systems Need Ontologies" (AI Engineer, Jul 2026)

## Core idea

LLMs are probabilistic. GXP already forces binary Ideal State Criteria and deterministic verification first. An **ontology** (typed entities + relationships + constraints) supplies the durable *semantic ledger* that sits outside the model.

> "Pydantic at the door, ontology at the ledger."

This document defines how GXP can optionally use that ledger without becoming autonomous or closed-world.

## When to use

Declare an ontology for a project (or task) when:

- The domain has hard invariants that English criteria alone are brittle at expressing (statuses, roles, uniqueness, disjointness, allowed transitions).
- Agents will make multi-step tool calls or state changes that must remain consistent.
- You want semantic violations to fail the same way tests/linters do.

Do **not** require an ontology for pure code/style/docs tasks. Keep it opt-in.

## Integration points in the GXP loop

### Phase 1 — Task brief
Ideal State Criteria may reference ontology invariants as binding `[guardrail]` lines, e.g.:

- `[guardrail] Order.status is one of {Paid, Shipped, Refunded} (ontology:OrderStatus)`
- `[guardrail] hasRefund is functional — at most one refund per order`

### Phase 5 — Verification ladder (proposed extension)

After deterministic checks (type/lint/test/build) and before subjective checks:

1. If the project or brief declares an ontology, run **Ontology Validation**.
2. Load the ontology (RDFS/OWL Turtle, SHACL shapes, or project-specific JSON Schema + SHACL).
3. Validate the proposed change / resulting state against it.
4. Fail closed on violations (treat as deterministic failure).
5. Record the ontology check result in the rating notes.

Pseudocode sketch:

```python
def phase5_verify(brief, change):
    run_deterministic_checks()          # existing
    if ontology_declared(brief or PROGRAM):
        result = ontology_reasoner.validate(change, ontology)
        if not result.ok:
            fail("Ontology violation: " + result.explanations)
    run_behavioral_checks()
    run_subjective_checks()
```

### Phase 0 / PROGRAM.md
Projects that use this pattern add:

```markdown
## Ontology
- Path: ontology/ or .ai/ontology/
- Format: turtle | shacl | json-schema+shacl
- Required for: tasks that touch [list of domains]
```

## Minimal directory layout (suggested)

```
.ai/ontology/          # or ontology/ at repo root
  README.md            # human description of the domain model
  core.ttl             # or core.owl / shapes.shacl
  constraints.md       # prose explanation of key invariants
```

Start tiny. Only model the entities and constraints that actually protect against the failures you care about.

## Tooling recommendations

- Python: `rdflib` + simple SPARQL or `owlready2` for light reasoning; `pyshacl` for SHACL.
- Prefer SHACL shapes over full OWL when the existing data is JSON/YAML (easier migration).
- Keep the reasoner offline and deterministic so it fits GXP's verification philosophy.

## Relation to existing GXP strengths

- Binary ISC remain the primary contract with the operator.
- Ontology adds a second, durable layer of truth that does not depend on conversation history.
- Anti-loop, failure capture, and honest rating continue to apply to semantic failures.
- Human approval gates for irreversible actions are unchanged.

## Non-goals (v0)

- Automatic ontology learning from code.
- Full closed-world assumption.
- Replacing the binary criteria system.
- Forcing every GXP user to maintain an ontology.

## Next concrete steps for this branch

1. Update `core/templates/task-brief.md` with ontology reference guidance.
2. Add a short section to `core/workflow.md` Phase 5.
3. Provide a toy example ontology for a simple domain (orders/status/refunds or similar).
4. Optional: tiny validation helper script under `scripts/` or `core/`.

Keep everything reversible and discussion-first.
