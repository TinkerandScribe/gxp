# Example Ontology (GXP templates)

This directory contains a **minimal, illustrative** domain ontology for projects that want to use Coyle-style agentic ontology guardrails.

## Purpose

The ontology acts as an external logical ledger. Agents propose changes; the ontology + a deterministic validator enforce hard semantic constraints (allowed values, functional properties, disjoint classes, etc.). Binary Ideal State Criteria remain the primary contract with the operator.

See `core/docs/ontology-guardrails.md` and `core/docs/ontology-integration.md` for the full design.

## Files

- `example-domain.ttl` — tiny Turtle example (Order / Status / Refund)
- This README

## How to use in a host project

1. Copy or adapt into `.ai/ontology/` (or a path declared in `PROGRAM.md`).
2. Reference relevant invariants in task-brief Ideal State Criteria as `[guardrail]` lines.
3. In Phase 5, run ontology validation after deterministic checks and before subjective ones.
4. Fail closed on violations (treat as a deterministic failure).

## Non-goals of this example

- Completeness
- Production reasoning performance
- Closed-world assumption
- Automatic learning from code

Keep the real ontology as small as the failures you actually need to prevent.
