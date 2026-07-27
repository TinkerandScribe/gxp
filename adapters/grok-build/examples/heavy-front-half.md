# Heavy front-half — concrete Grok Build sequence

Use this when the task is high-ambiguity, multi-constraint, or underspecified
(operator did not supply ~4+ binary Ideal State Criteria).

Prerequisites:

- Personas installed (`./install-grok-build.ps1 -Force` or project `.grok/personas/`)
- Optional skill: `./install-grok-build.ps1 -Force -InstallSkill` → skill name `gxp-build`
- Discover personas: `/personas` in Grok Build

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

## 2. Parent synthesizes one plan

Merge into a single brief:

- Goal (one sentence)
- 4–8 binary Ideal State Criteria (`[outcome]` / `[guardrail]` / `[hypothesis]`)
- Out of scope
- Verification plan (commands / tool checks)
- Phase 0 files to open

Do not implement yet.

## 3. `/plan` for operator approval

```text
/plan <synthesized GXP brief>
```

Only after the operator approves the plan (or explicitly says proceed) move on.

## 4. Implement (smallest viable change)

```text
spawn subagent persona=composer-coder  isolation=worktree
  prompt: <approved plan + criteria + out-of-scope + “smallest viable change only”>
```

Or implement in the parent if the change is tiny and reversible.

## 5. Independent Layer-2 verify

```text
spawn subagent persona=gxp-verifier  isolation=none  capability=read-only
  prompt: <approved criteria list + “walk each criterion with tools; do not edit product code”>
```

Parent walks any residual failures, then rates honestly.

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
