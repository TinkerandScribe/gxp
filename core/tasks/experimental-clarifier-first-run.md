# Task brief

**Date:** 2026-08-05
**Task slug:** experimental-clarifier-first-run
**Workflow:** full
**clarification_protocol:** experimental-v0

## Goal

Complete the first controlled dogfood of Experimental Clarification Protocol v0 by adding a minimal, usable `gxp-criteria-checker` persona under the Grok Build adapter that implements the isolated maker-checker described in the experimental protocol.

## Context

- Related files: `core/docs/experimental/clarification-protocol-v0.md`, `adapters/grok-build/personas/`, `adapters/grok-build/README.md`, existing personas such as `gxp-verifier.toml`
- Related PRs: #15 (merged)
- Background: The experimental protocol defines an isolated criteria checker that receives only brief artifacts and never the proposer’s chain-of-thought. A concrete persona makes the protocol immediately runnable in Grok Build.

**Strategy/Model:** Grok Build / local agents — lowest friction for persona addition and matches the target adapter.

**Scaffolding tier:** standard

## Ideal State Criteria

- [outcome] A `gxp-criteria-checker.toml` (or equivalent) exists under `adapters/grok-build/personas/` and is discoverable.
- [outcome] The persona instructions explicitly require independent context (receives only Goal + ISCs + out-of-scope + verification plan) and forbid seeing proposer reasoning.
- [outcome] The persona evaluates for strict binarity, completeness, residual ambiguity, scope fidelity, and verifiability, and outputs PASS/FAIL + concrete rewrites.
- [guardrail] No changes are made to the stable (non-experimental) core workflow path or to Phase 1/2 hard rules.
- [guardrail] The experimental flag and the absolute “cannot write binary criteria → stop” rule remain intact and documented.
- [outcome] A short note or pointer exists (in the persona file, README, or experimental doc) explaining how to invoke the checker with experimental-v0.
- [hypothesis] Mirroring the style and structure of `gxp-verifier.toml` is the cleanest approach.

## Out of scope

- Changing any stable GXP core files beyond optional one-line discoverability pointers
- Implementing full nested clarification sub-loops or durable history schema (P1)
- Automatic promotion of the experimental path
- Heavy Topology runtime changes

## Verification plan

- File exists and is valid TOML / follows existing persona pattern
- Instructions contain the independent-context and evaluation requirements
- Diff is limited to the intended files (persona + optional short pointer)
- Manual review that the hard stop rule language is preserved

## Self-evaluation gate

(to be completed under experimental-v0 with isolated checker)

## Approval gates

None for this small addition (docs/persona only).

## Dead ends

-

## Handoff notes

To fill in at the end.
