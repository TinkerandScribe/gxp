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
| `gxp-architect` | Shapes GXP plans with 4–8 binary Ideal State Criteria, out-of-scope, verification plan. Never codes product. |
| `grok-native-planner` | Single-agent planning alternative for lighter ambiguity. |
| `composer-coder` | Coherent multi-file implementation (smallest viable change). Prefer worktree isolation. |
| `gxp-verifier` | Strict Layer-2 critic: walks every Ideal State Criterion with tools. Never edits product code. |

Each persona contains strong role-locking instructions.

## Heavy-style Orchestration Pattern

For high-ambiguity / multi-constraint / underspecified work:

1. Spawn **gxp-researcher** + **gxp-architect** in parallel (scoped context only).
2. Parent synthesizes into one coherent plan (binary criteria, out-of-scope, verification plan).
3. Present via `/plan` for operator approval.
4. After approval → implementer (preferably in a worktree).
5. After implement → independent **gxp-verifier** for Layer-2 criterion-by-criterion check.
6. Honest rating + failure capture by the parent.

This recreates SuperGrok Heavy-style specialized collaboration while remaining strictly bounded by GXP.

## Mapping SuperGrok Heavy Custom Agents

1. Export your customized SuperGrok Heavy agent (system prompt + specialty).
2. Create a new `.toml` persona (or agent dir under `.grok/agents/`) that inherits the GXP base rules.
3. Lock the role boundaries (what it may / may not do).
4. Prefer high-reasoning models for research/architect/verifier; implementation models for coders.
5. Reference the persona by name when spawning subagents.

The adapter ships examples that can be copied and specialized further.

## Installation

```powershell
# From this adapter directory (Windows)
.\install-grok-build.ps1   # (to be added)
```

Or manually:

- Copy `personas/*.toml` → `~/.grok/personas/` (or project `.grok/personas/`)
- Optionally place agent definitions under `~/.grok/agents/` or project `.grok/agents/`
- For the skill itself: install or symlink this directory if a Build-specific skill entry is desired (name it distinctly, e.g. `gxp-build`)

See also the general Grok adapter install scripts for patterns.

## Relationship to Core and Other Adapters

- Derives from `core/`.
- Does **not** touch `adapters/grok/` (chat skill remains intact for grok.com).
- Follows the same philosophy as other adapters: make the methodology excellent for this surface’s strengths.

## Status

Initial structure (v0). Personas and orchestration docs are production-usable. Full install scripts, Workflow templates, and ACP examples are next.

---

GXP — Guided eXecution Protocol  
Verification-first. Binary criteria. Bounded agents.
