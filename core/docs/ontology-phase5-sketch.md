# Phase 5 Ontology Validation Sketch

Insert after the deterministic checks paragraph in `core/workflow.md` Phase 5:

### Ontology validation (optional)

If the project declares an ontology (see `PROGRAM.md` or the task brief) or the brief contains ontology-referenced `[guardrail]` criteria:

1. Load the ontology and any instance data produced or modified by the change.
2. Run the project’s ontology validator / reasoner (SHACL, SPARQL constraints, or custom).
3. Treat any violation as a deterministic failure — the same way a failing test or lint error is treated.
4. Do not proceed to behavioral or subjective checks until ontology validation passes or the brief is amended.

This step is **opt-in**. Projects without an ontology skip it entirely.

The ontology is the external ledger; the LLM never gets to redefine what "Paid" or "hasRefund" means mid-task.
