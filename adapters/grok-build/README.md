# Grok Build Adapter for GXP

**Dedicated adapter** that optimizes the Guided eXecution Protocol for **Grok Build** (the terminal/CLI agentic harness).

This adapter is independent of the general Grok / grok.com skill (`adapters/grok/`). It does not modify or overwrite the chat skill.

## Why a dedicated Build adapter?

Grok Build provides native multi-agent primitives that map perfectly onto GXP:

- Subagents with independent context and Git worktree isolation
- Personas / custom agent types
- Plan Mode (ideal for the heavy GXP front-half)
- Workflows (scale to hundreds of parallel agents)
- Arena Mode, `/deep-research`, ACP

Specialized identities with locked roles enforce binary Ideal State Criteria, anti-scope-creep, and two-layer verification more reliably than a single agent role-playing every phase.

## Specialized Identities (Personas)

Shipped under `personas/` (install to `~/.grok/personas/` or project `.grok/personas/`):

| Persona | Role |
|---------|------|
| `gxp-researcher` | Aggressive tool-using exploration; surfaces uncertainty + candidate criteria. Never implements. |
| `gxp-architect` | Shapes GXP plans with 4-8 binary Ideal State Criteria, out-of-scope, verification plan. Never codes product. |
| `grok-native-planner` | Single-agent planning alternative for lighter ambiguity. |
| `composer-coder` | Coherent multi-file implementation (smallest viable change). Prefer worktree isolation. |
| `gxp-verifier` | Strict Layer-2 critic: walks every Ideal State Criterion with tools. Never edits product code. |
| `gxp-criteria-checker` | **Experimental** isolated maker-checker for Ideal State Criteria (Clarification Protocol v0). Receives only brief artifacts; outputs PASS/FAIL + rewrite suggestions. Never implements. |

Each persona contains strong role-locking instructions.

**Model convention:** all personas use `model = "grok-build"` (Grok Build harness default). That string is a surface/runtime label, not a pin to a chat product tier. Operators may override at spawn time; `sync/check-core.sh` enforces the shipped default.

## Heavy-style Orchestration Pattern

For high-ambiguity / multi-constraint / underspecified work:

1. Spawn **gxp-researcher** + **gxp-architect** in parallel (scoped context only).
2. Parent synthesizes into one coherent plan (binary criteria, out-of-scope, verification plan).
3. Present via `/plan` for operator approval.
4. After approval -> implementer (preferably in a worktree).
5. After implement -> independent **gxp-verifier** for Layer-2 criterion-by-criterion check.
6. Honest rating + failure capture by the parent.

Concrete command-level sequence: [`examples/heavy-front-half.md`](examples/heavy-front-half.md).

Named workflow recipes (v1):
- [`workflows/heavy-gxp.md`](workflows/heavy-gxp.md) — researcher ∥ architect → /plan → composer-coder (worktree) → gxp-verifier.
- [`workflows/clarifier-then-heavy.md`](workflows/clarifier-then-heavy.md) — opt-in `clarification_protocol: experimental-v0` gate (gxp-criteria-checker isolated, max 2 FAIL) then the heavy path.
- [`examples/acp-gxp-session.md`](examples/acp-gxp-session.md) — thin ACP session packet (inputs, personas, phase contract, handoff shape).

This recreates SuperGrok Heavy-style specialized collaboration while remaining strictly bounded by GXP.

## Mapping SuperGrok Heavy Custom Agents

1. Export your customized SuperGrok Heavy agent (system prompt + specialty).
2. Create a new `.toml` persona (or agent dir under `.grok/agents/`) that inherits the GXP base rules.
3. Lock the role boundaries (what it may / may not do).
4. Prefer high-reasoning models for research/architect/verifier; implementation models for coders.
5. Reference the persona by name when spawning subagents.

The adapter ships examples that can be copied and specialized further.

## Installation

From this adapter directory:

```powershell
# Windows -- personas only (default)
.\install-grok-build.ps1 -Force

# Optional Build skill at ~/.grok/skills/gxp-build (does not touch chat skill)
.\install-grok-build.ps1 -Force -InstallSkill
```

```bash
bash install-grok-build.sh --force
bash install-grok-build.sh --force --install-skill
```

Manual:

- Copy `personas/*.toml` -> `~/.grok/personas/` (or project `.grok/personas/`)
- Optional skill: junction/symlink this directory to `~/.grok/skills/gxp-build` (see `INSTALL.md`)

**Chat skill isolation:** installers never write `gxp-ai-workflow` or `tinker-tools-ai-workflow`.

See `INSTALL.md` for flags and verification.

## Sync / verify

```bash
# From repo root
bash adapters/grok-build/sync/check-core.sh
bash scripts/verify.sh
```

```powershell
# From this adapter directory
.\sync\check-core.ps1
```

`check-core` is presence + integrity only (no generated `workflow.md` to diff). Intentional packaging divergences live in `sync/drift-allowlist.txt`.

## Relationship to Core and Other Adapters

- Derives from `core/`.
- Does **not** touch `adapters/grok/` (chat skill remains intact for grok.com).
- Follows the same philosophy as other adapters: make the methodology excellent for this surface's strengths.

## Status

v0.3 -- Personas, Heavy orchestration docs, install scripts, `SKILL.md` (`gxp-build`), lightweight `sync/check-core`, `examples/heavy-front-half.md`, named workflow templates (`workflows/heavy-gxp.md`, `workflows/clarifier-then-heavy.md`), and ACP example (`examples/acp-gxp-session.md`) are shipped.

---

GXP -- Guided eXecution Protocol  
Verification-first. Binary criteria. Bounded agents.
