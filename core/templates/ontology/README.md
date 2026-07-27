# Example Ontology (GXP template)

This directory provides a **minimal, optional** domain ontology that projects can copy and adapt.

It demonstrates the Coyle-style external ledger pattern used by the optional Phase 5 Ontology Validation step in GXP.

## When to use

Copy this into a host project under `.ai/ontology/` (or `ontology/`) only when the domain has hard semantic invariants (allowed statuses, functional properties, disjoint classes, etc.) that binary Ideal State Criteria alone are brittle at expressing.

Projects without an ontology skip the Phase 5 ontology step entirely.

## Files

- `example-order-domain.ttl` — tiny Turtle example (Order, Status, Refund, functional properties)
- This README

## How GXP uses it

1. Declare the ontology path in `PROGRAM.md` or in the task brief.
2. Reference ontology invariants as `[guardrail]` Ideal State Criteria when relevant.
3. In Phase 5, after deterministic checks, run validation against the ontology (SHACL, SPARQL, or custom reasoner).
4. Treat violations as deterministic failures.

See `core/docs/ontology-guardrails.md` and `core/docs/ontology-integration.md` for the full design.

## Tooling

- Python: `rdflib`, `pyshacl`
- Keep the reasoner offline and deterministic.

Start tiny. Only model the constraints that protect against the failures you care about.
