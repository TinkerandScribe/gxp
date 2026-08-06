# ACP GXP Session (thin packet) — v1 example

**Purpose (per design):** Single thin doc for ACP clients / external orchestrators.  
Inputs, personas, phase contract, handoff shape. No new GXP methodology phases.

**Location:** `adapters/grok-build/examples/acp-gxp-session.md` (docs-only).  
**Never** writes chat skill paths. Experimental paths remain opt-in.

---

## Inputs (brief artifacts only)

Provide exactly these to the ACP session:

- Goal (one sentence)
- 4–8 tagged Ideal State Criteria (`[outcome]`, `[guardrail]`, `[hypothesis]`)
- Out of scope (explicit list)
- Verification plan (commands / tool checks per criterion or group)
- Optional: `clarification_protocol: experimental-v0` (operator flag required)
- Optional: Phase 0 context pointers (PROGRAM.md / rules/ / failures/ when present)
- Scaffolding tier (default: standard)

Do not pass full chain-of-thought or implementation notes into the initial packet.

---

## Personas (shipped only; discover with /personas)

- gxp-researcher — aggressive tool-using exploration; uncertainty + candidate criteria. Never implements.
- gxp-architect — binary criteria, out-of-scope, verification plan. Never implements product code.
- composer-coder — smallest viable multi-file implementation. Prefer worktree isolation.
- gxp-verifier — Layer-2 critic: walks every Ideal State Criterion with tools. Never edits product.
- gxp-criteria-checker — **Experimental** isolated maker-checker (brief artifacts only). Outputs PASS/FAIL + rewrite suggestions. Requires `clarification_protocol: experimental-v0`.

All use `model = "grok-build"`.

---

## Phase contract (no new phases)

This packet maps to existing GXP phases only:

1. **Front-half (Heavy or Clarifier-then-Heavy)**  
   - Heavy: researcher ∥ architect → synthesize → `/plan` gate.  
   - Clarifier-then-Heavy (opt-in only): clarifier drafts → gxp-criteria-checker (isolated) → max 2 FAIL then escalate → on PASS, same heavy path.

2. **Approval** — `/plan` (operator sign-off required for multi-file / multi-constraint).

3. **Implement** — composer-coder (worktree preferred).

4. **Layer-2 verify** — gxp-verifier walks each criterion with tools.

5. **Rate + capture** — parent owns honest rating and optional failure capture.

6. **Handoff** — emit handoff per shape below.

Lightweight path is out of scope for this ACP packet shape (use only when a strong named verify already exists and change is trivial).

---

## Handoff shape (minimal)

Return a compact record consumable by ACP clients or downstream agents. Example structure (markdown or JSON-equivalent):

```text
## Handoff

**Task slug:** <slug>
**Date:** <ISO>
**clarification_protocol:** off | experimental-v0
**Scaffolding tier:** standard

### Brief artifacts (final)
- Goal: <one sentence>
- Ideal State Criteria:
  - [outcome] ...
  - [guardrail] ...
- Out of scope: ...
- Verification plan: ...

### Execution summary
- Front-half used: heavy-gxp | clarifier-then-heavy
- Criteria-checker iterations (if experimental): N (max 2)
- /plan approved: yes | (operator note)
- Implement isolation: worktree | parent
- Layer-2 verifier: PASS | FAIL (per-criterion table)
  - Criterion | Check command | Result | Evidence
- Project verify commands run:
  - bash adapters/grok-build/sync/check-core.sh
  - bash scripts/verify.sh
- Residual items / follow-ups: ...

### Artifacts touched
- <relative paths>

### Rating (parent)
criteria_met: <int>
criteria_total: <int>
rating: <1-10>
notes: <short>
```

---

## Invocation notes (Grok Build)

- Parent orchestrator owns the packet and spawns.
- Use conceptual spawn sequences from `heavy-gxp.md` and `clarifier-then-heavy.md`.
- After `/plan` approval, proceed only on explicit operator go-ahead.
- Always run the two verify commands listed in the handoff shape (adapter sync + repo verify).
- Never auto-enable experimental-v0.

---

## Anti-patterns

- Injecting proposer chain-of-thought into gxp-criteria-checker
- Skipping `/plan` gate
- Claiming “done” from smoke green alone
- Treating experimental as default
- Writing to chat skill paths (gxp-ai-workflow)

This is a thin example packet only. It does not alter core methodology or require Rhai/automation in v1.
