# Ontology Integration for GXP (Coyle-style Agentic Guardrails)

**Status:** Experimental design (linked to issue #11)
**Goal:** Add an optional external formal ontology as the "ledger" for semantic validation of agent proposals and Ideal State Criteria.

## Why

LLMs are probabilistic. Binary criteria + deterministic tests catch many errors, but semantic domain constraints (allowed status values, functional properties, disjoint classes, transitive relations) are better enforced by a formal model outside the model.

This follows Frank Coyle’s neurosymbolic pattern: probabilistic reasoning inside the LLM, logical constraints outside it.

## Minimal Viable Design

### 1. Task Brief Extension

In `templates/task-brief.md`, add an optional section:

```markdown
## Ontology / Domain Model (optional)

- Ontology path: `.ai/ontology/domain.ttl` (or SHACL shapes)
- Relevant classes / constraints for this task:
- ISCs that reference ontology axioms: ...
```

Binding ISCs may cite ontology invariants, e.g.:

- [guardrail] Proposed status is one of the values allowed by the ontology Status class
- [outcome] No functional property is violated (e.g. an Order has at most one active Refund)

### 2. Phase 5 — Ontology Validation step

After deterministic checks (type/lint/test/build) and before behavioral/subjective:

```
If the brief or PROGRAM.md declares an ontology:
  1. Load the ontology (rdflib or equivalent).
  2. Materialize the current proposed state / tool arguments / changed entities as RDF (or validate against SHACL).
  3. Run consistency check + relevant SPARQL/SHACL constraints.
  4. Fail the verification ladder if violations are found (treat as deterministic failure).
  5. Record any semantic dead-ends in the brief or failures/.
```

This remains optional. Projects without an ontology continue exactly as today.

### 3. Example minimal ontology (Turtle)

```turtle
@prefix : <http://example.org/gxp-domain#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:Status a owl:Class .
:Pending a :Status .
:Shipped a :Status .
:Refunded a :Status .

:hasStatus a owl:FunctionalProperty ;
    rdfs:domain :Order ;
    rdfs:range :Status .

:hasRefund a owl:FunctionalProperty ;
    rdfs:domain :Order ;
    rdfs:range :Refund .
```

### 4. Implementation sketch (Python)

```python
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

def validate_against_ontology(state_rdf: str, ontology_path: str) -> list[str]:
    g = Graph()
    g.parse(ontology_path, format="turtle")
    g.parse(data=state_rdf, format="turtle")
    # simple consistency + custom constraints
    violations = []
    # e.g. check functional properties, disjointness, etc.
    return violations
```

### 5. Integration points

- PROGRAM.md can declare `ontology: path/to/ontology.ttl`
- Failure capture template gains a "semantic" category
- Anti-loop treats repeated ontology violations the same as repeated test failures

## Non-goals (v1)

- Full OWL reasoner performance optimization
- Automatic ontology learning from code
- Replacing existing binary criteria or tests
- Changing L3/L4 boundedness or human approval gates

## Next actions

1. Update task-brief.md and workflow.md on this branch.
2. Add a sample ontology under core/templates/ontology/.
3. Add a small helper script or document the validation pattern.
4. Dogfood on one real task.
5. Update ROADMAP / CHANGELOG once stable.

Keep the spirit of GXP: verification-first, binary, bounded, honest rating.
