# Task brief — Grok Build ACP / workflow templates (design)

**Date:** 2026-08-06  
**Task slug:** grok-build-acp-workflow-templates  
**Workflow:** full  
**Phase:** design brief only (implementation is a follow-up brief)  
**ROADMAP:** Part D — “Workflow templates / ACP orchestration for Grok Build” (**next**)  
**Scaffolding tier:** standard  
**clarification_protocol:** off for this design ticket (optional experimental-v0 when implementing)

## Goal

Define a minimal, shippable design for **Grok Build workflow templates and/or ACP orchestration examples** that make the existing GXP Heavy + experimental Clarifier patterns **invocable as named workflows**, without changing stable GXP core methodology.

## Context

- Adapter: `adapters/grok-build/` (personas, install, `SKILL.md`, `examples/heavy-front-half.md`, `examples/experimental-clarifier-topology.md`)  
- README status (v0.2): personas + heavy docs usable; **“Workflow templates and ACP examples are next.”**  
- Host primitives (Grok Build): Workflows, Plan Mode, subagents/personas, worktree isolation, ACP  
- Out of product scope historically: multi-provider critic product; force-push; chat-skill overwrite  

**Strategy/Model:** Grok Build — native workflow/ACP surface is the delivery vehicle.  

## Ideal State Criteria (design deliverable)

- [outcome] A written design section in this brief (or linked `core/docs/` draft path) lists **≤3** concrete workflow artifacts to ship in v1 (names + one-sentence purpose each).  
- [outcome] Each proposed artifact maps to an existing persona topology already documented (heavy-front-half and/or experimental-clarifier-topology) — no new methodology phases.  
- [outcome] Install/discoverability plan states where files live (`adapters/grok-build/…`), how operators invoke them, and that chat skill `gxp-ai-workflow` remains untouched.  
- [outcome] Verification plan for a future implement brief names deterministic checks (path presence, `check-core` / `verify.sh`, optional dry-run command).  
- [guardrail] Design does **not** require stable-core changes to `core/workflow.md` Phases 0–8.  
- [guardrail] Design does **not** auto-promote `clarification_protocol: experimental-v0` (opt-in only).  
- [guardrail] No implementation, release tag, or ROADMAP status flip is required to complete **this** design brief — only the design content below.  
- [hypothesis] Starting with markdown workflow recipes + one optional ACP session template is enough for v1; Rhai/automation can wait.

## Out of scope (this brief)

- Implementing workflow files or ACP configs.  
- Changing `core/workflow.md` or chat adapters.  
- Full SHACL/reasoner tooling.  
- Arena Mode productization.  
- M6 campaign execution.

## Verification plan (design-only)

- All Ideal State Criteria above true by inspection of this file’s Design section.  
- `git diff` for a design-only landing touches only this brief (and optional ROADMAP one-liner later, separate).  
- Operator can approve/reject the v1 artifact list without running agents.

---

## Design (v1 proposal — for operator approval)

### Problem

Operators can read `examples/heavy-front-half.md` and copy-paste spawn sequences, but there is **no named, reusable workflow entrypoint** for:

1. Heavy front-half (research + architect → plan → implement → verify)  
2. Optional experimental Clarifier gate before heavy  
3. (Stretch) ACP-friendly session packet for external orchestrators  

### v1 artifacts (≤3)

| # | Artifact | Path (proposed) | Purpose |
|---|---|---|---|
| 1 | **Heavy GXP workflow recipe** | `adapters/grok-build/workflows/heavy-gxp.md` (or `.grok/workflows/` mirror if host requires) | Named steps matching `examples/heavy-front-half.md`, copy-paste / Workflow-ready |
| 2 | **Experimental Clarifier → Heavy recipe** | `adapters/grok-build/workflows/clarifier-then-heavy.md` | Opt-in `experimental-v0` gate then heavy; points at `gxp-criteria-checker` |
| 3 | **ACP session packet (thin)** | `adapters/grok-build/examples/acp-gxp-session.md` | Single doc: inputs, personas, phase contract, handoff JSON shape for ACP clients |

**Deferred (not v1):** Rhai/automation scripts, Arena configs, multi-repo mesh, automatic criteria invention.

### Mapping to existing topology

```text
Operator goal
    │
    ├─[workflow: heavy-gxp]─────────────────────────────┐
    │   researcher ∥ architect → /plan → composer → verifier
    │
    └─[workflow: clarifier-then-heavy] (opt-in flag)───┐
        clarifier → gxp-criteria-checker PASS
            → same heavy path
```

No new GXP phases. Experimental path remains flag-gated.

### Install / discoverability

1. Ship files under `adapters/grok-build/workflows/` + `examples/acp-gxp-session.md`.  
2. Link from `adapters/grok-build/README.md` (Workflow section; bump status note past “next”).  
3. Install scripts: **no** requirement to copy workflows into `~/.grok` for v1 (docs-first); optional later.  
4. **Never** write `~/.grok/skills/gxp-ai-workflow` or legacy chat aliases.

### Future implement brief — verification sketch

- Paths exist; README links resolve.  
- `bash adapters/grok-build/sync/check-core.sh` and `bash scripts/verify.sh` exit 0.  
- Recipes reference only shipped personas (`gxp-researcher`, `gxp-architect`, `composer-coder`, `gxp-verifier`, optional `gxp-criteria-checker`).  
- Grep: no instructions to modify stable core phases; experimental remains opt-in.

### Risks / non-goals

| Risk | Mitigation |
|---|---|
| Workflow host format churn | Keep v1 as markdown recipes; host-specific JSON/Rhai only if stable API documented |
| Scope creep into “orchestrator product” | Hard cap: 3 artifacts; no scheduler/critic product |
| Accidental experimental promotion | Clarifier workflow header: operator must set flag |

### Approval gate

Operator picks:

- **Approve v1 list as-is** → open implement brief `grok-build-acp-workflow-templates-implement`  
- **Edit list** (drop ACP packet / merge recipes) → amend this design, then implement  
- **Park** → leave ROADMAP Part D as next without files  

**Operator decision:** **Approve v1 list as-is** (2026-08-06)

## Handoff notes

- Design complete: operator approved v1 artifact list 2026-08-06.  
- Implementation is **out of scope** for this ticket → follow-up implement brief / Grok Build prompt.  
- Related examples already in tree: `examples/heavy-front-half.md`, `examples/experimental-clarifier-topology.md`.
