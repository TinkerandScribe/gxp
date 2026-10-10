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
| **Grok Bot (this adapter)** | Brief + criteria + **status**; small low-risk tweaks; widget gates; Cursor for bigger or risky work |

Forcing Bot to clone, take bigger or risky edits, `/plan`, or spawn researcher/architect/verifier personas would fight the product. Small, low-risk tweaks are allowed.

## Operating model

```
Grok Bot chat          widgets           Cursor or a small tweak       git
─────────────          ───────           ────────────────────────       ───
brief + criteria  -->  approve      -->  small low-risk tweak on       branch / commit /
status                 (not /plan)       the existing checkout, or      push / PR
                                         Cursor for bigger or risky     same review and
                                         work (no model pin)            merge rules
```

### Bot chat stays thin

Allowed in the Grok Bot conversation: task brief, 4–8 binary Ideal State Criteria, status, and a small low-risk tweak on an existing checkout.

Bots may make small, low-risk code tweaks (copy fixes, config values, a few lines in one or two files). Never edit payments, auth/sign-in, DB migrations, secrets, or legal text. Bigger or risky work goes to Cursor using the dashboard default model (no model pin). Same PR, review, and merge rules either way.

Forbidden in that conversation:

- Cloning repositories
- Payments, auth/sign-in, DB migrations, secrets, or legal text
- Bigger or risky implementation, code dumps, or multi-file diffs
- Grok Build personas (`gxp-researcher`, `gxp-architect`, `gxp-verifier`)
- `/plan` as the approval gate
- Telling the operator to run `sync/check-core.sh`

### Implementation and git

- **Small tweaks** are applied by Grok Bot on the existing checkout. Git for that tweak (branch, commit, push, PR) may run there.
- **Bigger or risky work** goes to a **Cursor cloud agent** or local **`cursor-agent`**, using [`instructions/cursor-handoff.md`](instructions/cursor-handoff.md). Dashboard default model (no model pin).
- **Verify** is owned by the agent that made the change (project `verify.sh` / PROGRAM commands, then criterion walk). Do not outsource Phase 5 to the human.
- **Mechanical git** for bigger work stays available on the **local CLI** or inside the Cursor session when the operator already authorized it.
- **Fleet rating** is one `bin/append.py` command after the run (see `SKILL.md`). Do not append with a shell heredoc.

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

Derives from `core/`. Does not change GXP phases, criteria tags, verification ladder, ratings, or failure capture. Bot-specific delivery (thin chat, widgets, small low-risk tweaks, Cursor handoff, local git, fleet append) lives only here.

## Status

v0 — dedicated Bot surface: skill, getting started, Cursor handoff, small low-risk tweaks, fleet rating append, lightweight `sync/check-core`.

---

GXP -- Guided eXecution Protocol  
Verification-first. Binary criteria. Bounded agents.
