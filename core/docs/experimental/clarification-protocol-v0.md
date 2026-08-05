# Experimental Clarification Protocol v0

**Status:** Experimental · Operator-gated · Opt-in only  
**Does not modify the stable GXP core path in `core/workflow.md`.**

## Purpose
Strengthen the front-loaded clarification gate (Phase 1 → Phase 2) by applying maker-checker discipline and optional graph structure to the production of Ideal State Criteria themselves.  
Goal: higher-quality binary criteria on first pass, fewer late-emerging ambiguities, while preserving the hard stop rule.

## Non-negotiable Guardrail
If the agent cannot produce 4–8 strong, binary Ideal State Criteria that fully capture the goal, the task is not understood.  
**Stop. Escalate to the operator.**  
No experimental feature may invent, assume, or soften criteria to bypass this gate.

## Activation
In the task brief or scaffolding config:
```
clarification_protocol: experimental-v0
```
Or via flag in Heavy Topology plans. Default remains the stable sequential path.

## Enhanced Clarification Flow (P0)

### 1. Propose
An agent drafts:
- One-sentence Goal
- 4–8 binary Ideal State Criteria (tagged `[outcome]` / `[guardrail]` / `[hypothesis]`)
- Explicit Out-of-Scope list
- Verification plan (deterministic checks preferred)

### 2. Isolated Check (Maker-Checker)
A separate `gxp-criteria-checker` (or equivalent persona) runs in **independent context**.  
It receives only the drafted brief artifacts — never the proposer’s chain-of-thought or intermediate reasoning.

Checker evaluates:
- Strict binarity (each criterion is pass/fail with no interpretation required)
- Completeness relative to the Goal
- Absence of residual ambiguity
- Scope fidelity (no expansion beyond the original ask)
- Verifiability (named deterministic or behavioral checks exist)

Output: `PASS` or `FAIL` + concrete rewrite list.

### 3. Iterate or Escalate
- Max 2 checker cycles (consistent with anti-loop).
- On persistent FAIL → escalate to operator with the failed brief and checker notes.
- Only on PASS does the brief become eligible for Phase 2 Self-Eval Gate / implementation.

## Optional: Clarifier Node (Heavy Topology)
For high-ambiguity or multi-constraint work, the graph may begin with a Clarifier node whose sole Ideal State Criteria are:
1. Binary brief is complete.
2. Isolated checker has returned PASS.

Downstream nodes remain inactive until the Clarifier succeeds. This keeps parallelism structured and bounded.

## Measurement Hooks
Append to ratings.jsonl (when experimental):
- `clarification_protocol`: "experimental-v0"
- `criteria_checker_iterations`: N
- `criteria_quality` (1–10)
- `late_ambiguity_detected`: true/false (from Phase 5)

Log recurring checker failures or clarification patterns in `.ai/failures/`.

## Future (P1, after measurement)
- Durable clarification history schema (questions, answers, discarded assumptions).
- Bounded nested clarification sub-loops for individual criteria that fail late.

## Integration
- Grok Build: add / update `gxp-criteria-checker` persona with isolated context contract.
- Claude / other adapters: support via skill instructions or system prompt fragments when the experimental flag is set.
- Lightweight path: remains available and unchanged; experimental clarifier is opt-in.
- Compatible with existing scaffolding tiers and ontology guardrails.
- Does **not** relax anti-scope-creep, deterministic-first verification, or L3/L4 bounded autonomy.

## Success Criteria for this Experimental Protocol
- [ ] Does not increase scope-creep incidents
- [ ] Reduces late Phase 5 ambiguity failures
- [ ] Improves first-pass criteria quality (measurable via ratings)
- [ ] Operator retains final authority on unresolved ambiguity

This document is itself subject to GXP: any changes require a brief + verification.
