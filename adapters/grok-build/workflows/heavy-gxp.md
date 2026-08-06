# Heavy GXP — Grok Build workflow (v1)

Use this named workflow for high-ambiguity, multi-constraint, or underspecified work
when the operator has not supplied ~4+ binary Ideal State Criteria up front.

This is the reusable form of the pattern documented in `examples/heavy-front-half.md`.

Prerequisites:

- Personas installed (`./install-grok-build.ps1 -Force` or project `.grok/personas/`)
- Optional skill: `./install-grok-build.ps1 -Force -InstallSkill` → skill name `gxp-build`
- Discover personas: `/personas` in Grok Build

Scaffolding tier: standard (default). See `core/docs/capability-scaffolding.md`.

---

## 1. Spawn research + architecture in parallel

In the parent (orchestrator) turn, launch both with scoped context only.
Do **not** let either implement product code.

```text
# Conceptual spawn (Grok Build subagents / Task tool)
spawn subagent persona=gxp-researcher  isolation=none
  prompt: <operator goal + repo path + “do not implement; structured research output only”>

spawn subagent persona=gxp-architect   isolation=none
  prompt: <same goal + any research already known + “plan only; no product code”>
```

Wait for both to finish. Researcher output should include uncertainty + candidate
criteria; architect output should include a GXP-shaped plan draft.

---

## 2. Parent synthesizes one plan

Merge into a single brief:

- Goal (one sentence)
- 4–8 binary Ideal State Criteria (`[outcome]` / `[guardrail]` / `[hypothesis]`)
- Out of scope
- Verification plan (commands / tool checks)
- Phase 0 files to open

Do not implement yet.

---

## 3. `/plan` for operator approval

```text
/plan <synthesized GXP brief>
```

Only after the operator approves the plan (or explicitly says proceed) move on.

---

## 4. Implement (smallest viable change)

```text
spawn subagent persona=composer-coder  isolation=worktree
  prompt: <approved plan + criteria + out-of-scope + “smallest viable change only”>
```

Or implement in the parent if the change is tiny and reversible.

---

## 5. Independent Layer-2 verify

```text
spawn subagent persona=gxp-verifier  isolation=none  capability=read-only
  prompt: <approved criteria list + “walk each criterion with tools; do not edit product code”>
```

Parent walks any residual failures, then rates honestly.

---

## 6. Quick commands (repo-level)

```bash
# From repo root
bash adapters/grok-build/sync/check-core.sh
bash scripts/verify.sh
```

```powershell
# From adapters/grok-build
.\sync\check-core.ps1
.\install-grok-build.ps1 -Force
```

---

## Anti-patterns

- Researcher or architect writing product code
- Verifier self-certifying the implementer’s smoke green without tool checks
- Skipping `/plan` on multi-file / multi-constraint work
- Touching `~/.grok/skills/gxp-ai-workflow` (chat skill — never)

---

## Personas referenced (shipped only)

- gxp-researcher
- gxp-architect
- composer-coder
- gxp-verifier

This workflow is docs-only under `adapters/grok-build/`. It does not alter `core/workflow.md`.
