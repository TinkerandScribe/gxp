# Experimental Clarification Protocol v0

**Status:** Experimental / Operator-gated only  
**Does not alter the stable GXP core path.**  
**Activation:** Add `clarification_protocol: experimental-v0` to the task brief (or set via scaffolding / env / adapter flag). Default is off.

## Purpose
Strengthen the front-loaded clarification gate with maker-checker quality controls and optional graph structure, while preserving the hard rule that prevents agents from proceeding on underspecified work.

## Non-negotiable Core Rule (unchanged)
If you cannot write **4–8 strong binary Ideal State Criteria**, the task is not understood yet.  
**Stop and clarify with the operator.**  
No agent may invent vague, non-binary, or incomplete criteria and proceed to implementation. This rule remains absolute and cannot be bypassed by the experimental protocol.

## Enhanced Clarification Flow (when experimental-v0 is active)

### 1. Propose
Any capable agent/persona drafts:
- Goal
- 4–8 tagged Ideal State Criteria (`[outcome]`, `[guardrail]`, `[hypothesis]`)
- Out-of-scope
- Verification plan

### 2. Isolated Criteria Checker (Maker-Checker)
A dedicated checker (persona `gxp-criteria-checker` or equivalent) runs in **independent context**.  
It receives **only** the brief artifacts (no proposer’s chain-of-thought or intermediate reasoning).

> **Persona location:** `adapters/grok-build/personas/gxp-criteria-checker.toml` (Grok Build). Other adapters may provide an equivalent isolated checker.

The checker evaluates against:
- Strict binarity (each binding criterion is pass/fail without interpretation)
- Completeness relative to the stated Goal
- Absence of residual ambiguity or weasel words
- Scope fidelity (no creep)
- Concrete verifiability (deterministic check exists or can be named)

Output: `PASS` or `FAIL` + specific, actionable rewrite suggestions.

### 3. Gate
- **PASS** → brief advances to Phase 2 / rest of workflow (or to downstream graph nodes).
- **FAIL** → iterate (max 2 attempts total, consistent with anti-loop). After 2 failures → escalate to operator with the full history.

### 4. Optional Clarifier Node (Heavy Topology only)
For complex or high-ambiguity tasks, the graph may begin with a **Clarifier** node whose sole Ideal State Criteria are:
- “Binary brief is complete”
- “Isolated criteria-checker has returned PASS”

Downstream nodes (architect, implementer, verifier, etc.) activate only after Clarifier succeeds.

## Durable Clarification History (recommended)
When experimental-v0 is used, append a lightweight record to `.ai/clarifications/<slug>.md` or the ratings ledger:
- Questions posed (if any)
- Operator answers
- Discarded assumptions
- Checker iterations and outcomes

This becomes shared state for future runs or nested sub-graphs.

## Measurement
In `ratings.jsonl` include (when experimental):
- `clarification_protocol: "experimental-v0"`
- Number of criteria-checker iterations
- Final criteria quality (self-rated or operator)
- Whether residual ambiguity appeared later in Phase 5

Capture systemic patterns in `.ai/failures/`.

## Integration Notes
- Lightweight path: remains optional / off by default.
- Full / Heavy path: recommended for multi-file, multi-constraint, or underspecified operator asks.
- Adapters (Grok Build, Claude, Cursor, etc.): support isolated checker context and the activation flag.
- Compatible with existing scaffolding tiers and ontology guardrails.
- Does **not** relax anti-scope-creep, deterministic-first verification, or L3/L4 bounded autonomy.

## Success Criteria for this Experimental Protocol
- [ ] Does not increase scope-creep incidents
- [ ] Reduces late Phase 5 ambiguity failures
- [ ] Improves first-pass criteria quality (measurable via ratings)
- [ ] Operator retains final authority on unresolved ambiguity

This document is itself subject to GXP: any changes require a brief + verification.
