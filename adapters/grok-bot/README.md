# Grok Bot Adapter for GXP

**Dedicated adapter** that fits Guided eXecution Protocol to **Grok Bot** (thin chat orchestrator).

This adapter is independent of:

- `adapters/grok/` — grok.com / chat skill (`gxp` / `gxp-ai-workflow`)
- `adapters/grok-build/` — Grok Build personas, `/plan`, Heavy workflows (`gxp-build`)

Do not stretch those adapters to cover Bot constraints. `core/` remains the methodology source of truth.

## Why a dedicated Bot adapter?

Grok Bot is not Grok chat and not Grok Build:

| Surface | What it should do |
|---------|-------------------|
| Grok chat (`adapters/grok`) | In-chat skill, generated workflow, operator-run sync check |
| Grok Build (`adapters/grok-build`) | Personas, `/plan`, worktrees, Heavy front-half |
| **Grok Bot (this adapter)** | Brief + criteria + **status** only; widget gates; Cursor implements |

Forcing Bot to clone, edit, `/plan`, or spawn researcher/architect/verifier personas would fight the product.

## Operating model

```
Grok Bot chat          widgets           Cursor                     local CLI
─────────────          ───────           ──────                     ─────────
brief + criteria  -->  approve      -->  cloud agent or             git branch /
status only            (not /plan)       cursor-agent implements    commit / push
                                         and runs verify itself
```

### Bot chat stays thin

Allowed in the Grok Bot conversation: task brief, 4–8 binary Ideal State Criteria, status.

Forbidden in that conversation:

- Cloning repositories
- Editing, writing, or patching repo files
- Implementation, code dumps, or multi-file diffs
- Grok Build personas (`gxp-researcher`, `gxp-architect`, `gxp-verifier`)
- `/plan` as the approval gate
- Telling the operator to run `sync/check-core.sh`

### Implementation and git live elsewhere

- **Implement** via a **Cursor cloud agent** or local **`cursor-agent`**, using [`instructions/cursor-handoff.md`](instructions/cursor-handoff.md).
- **Verify** is owned by that agent (project `verify.sh` / PROGRAM commands, then criterion walk). Do not outsource Phase 5 to the human.
- **Mechanical git** (branch, commit, push) runs on the **local CLI** — never as a Grok Bot side effect.

## Files

| Path | Role |
|------|------|
| `SKILL.md` | Bot skill (`gxp-bot`) — constraints + precedence |
| `GETTING_STARTED.md` | Install / first run for operators |
| `instructions/cursor-handoff.md` | Copy-paste packet for Cursor |
| `sync/check-core.sh` / `.ps1` | Presence + integrity (CI / `verify.sh` glob) |
| `sync/drift-allowlist.txt` | Why this adapter has no generated `workflow.md` |

No personas, no installers that write `gxp-ai-workflow` or `gxp-build`, no generated `instructions/workflow.md`.

## Installation

See [`GETTING_STARTED.md`](GETTING_STARTED.md). Skill identity is **`gxp-bot`** only.

## Sync / verify

CI and maintainers (not Grok Bot chat):

```bash
# From repo root
bash adapters/grok-bot/sync/check-core.sh
bash scripts/verify.sh
```

```powershell
# From this adapter directory
.\sync\check-core.ps1
```

`check-core` is presence + integrity only. Intentional packaging divergences live in `sync/drift-allowlist.txt`.

## Relationship to core

Derives from `core/`. Does not change GXP phases, criteria tags, verification ladder, ratings, or failure capture. Bot-specific delivery (thin chat, widgets, Cursor handoff, local git) lives only here.

## Status

v0 — dedicated Bot surface: skill, getting started, Cursor handoff, lightweight `sync/check-core`.

---

GXP -- Guided eXecution Protocol  
Verification-first. Binary criteria. Bounded agents.
