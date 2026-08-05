# Task Brief: First controlled dogfood of Experimental Clarification Protocol v0

**clarification_protocol: experimental-v0**

## Goal
Perform the first measured dogfood of Experimental Clarification Protocol v0 inside the GXP repository by adding a minimal, reversible `gxp-criteria-checker` persona (or equivalent documentation) under the Grok Build adapter so that the isolated maker-checker described in the experimental protocol can be used in practice.

## Ideal State Criteria (starting point — to be refined by the experimental maker-checker)
- [outcome] A `gxp-criteria-checker` persona (or clear equivalent) exists under `adapters/grok-build/` (or a clearly marked experimental location)
- [outcome] The persona instructions explicitly require independent context (no access to the proposer’s chain-of-thought) and output only PASS / FAIL + concrete rewrite suggestions
- [guardrail] No changes are made to the stable non-experimental GXP path (`core/workflow.md` Phase 1/2 behavior remains untouched)
- [guardrail] The hard rule “cannot write 4–8 strong binary Ideal State Criteria → stop and clarify with the operator” remains absolute
- [outcome] At least one entry is appended to the ratings ledger noting that experimental-v0 was used and the number of checker iterations (if any)
- [outcome] The change is small enough to be fully reversed by a single revert
- [outcome] Existing verification (scripts/verify.sh or equivalent) continues to pass or any new checks are documented

## Out of scope
- Full production-grade persona with extensive tooling or multi-adapter support
- Any automatic activation of the experimental protocol
- Changes to core GXP phases, anti-loop, or verification ladder
- Non-experimental adapter code

## Verification plan
- File(s) exist at the expected path(s)
- Content satisfies each Ideal State Criterion above
- `scripts/verify.sh` (or documented equivalent) exits cleanly
- Rating entry present with experimental flag

## Notes for the experimental protocol
This brief is intentionally open in places so the isolated criteria-checker has real work. Run Propose → Isolated Checker (max 2 iterations) before any implementation. Escalate unresolved ambiguity to the operator.
