# Getting Started — Grok Bot GXP adapter

Fit GXP onto Grok Bot in a few minutes. This surface is a **thin orchestrator**: brief, criteria, and status. Cursor does the repo work.

## What it gives you

- A Bot skill (`gxp-bot`) that will not clone or edit repositories in the Grok Bot chat.
- Widget approval gates (not Grok Build `/plan`).
- A copy-paste handoff for a **Cursor cloud agent** or local **`cursor-agent`**.
- Agent-owned verification — you are not asked to run `check-core.sh` in the Bot conversation.

## 1. Install the Bot skill

**Preferred:** paste `SKILL.md` into the Grok Bot instructions / system prompt for that bot.

**Optional** (only if your Grok host loads skills from disk): junction or symlink this directory to `~/.grok/skills/gxp-bot`.

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.grok\skills"
New-Item -ItemType Junction -Path "$HOME\.grok\skills\gxp-bot" -Target (Resolve-Path .)
```

```bash
mkdir -p ~/.grok/skills
ln -s "$(pwd)" ~/.grok/skills/gxp-bot
```

Protected paths — **never** use them for this adapter:

- `~/.grok/skills/gxp-ai-workflow` (chat)
- `~/.grok/skills/gxp-build` (Build)
- `~/.grok/skills/tinker-tools-ai-workflow` (legacy chat alias)

## 2. Use it day-to-day

1. In Grok Bot, state the goal. Say "use gxp-bot" if the host needs an invoke phrase.
2. The bot drafts a GXP brief and **4–8 binary Ideal State Criteria**.
3. Approve via a **widget**, not `/plan`.
4. Copy the packet from [`instructions/cursor-handoff.md`](instructions/cursor-handoff.md) into:
   - a **Cursor cloud agent**, or
   - local **`cursor-agent`** in an existing checkout (do not clone from Grok Bot).
5. Cursor implements and **runs verify itself**. Grok Bot only reports status.
6. Mechanical git stays on your **local CLI** (or the Cursor terminal): branch, commit, push.

Keep Bot messages thin. If the bot starts dumping patches or asking you to run `bash sync/check-core.sh`, it is on the wrong adapter.

## 3. What "done" looks like

The Cursor agent should return:

- Changed files
- Exact commands and exit codes (for this repo: `bash scripts/verify.sh`)
- Pass/fail per binding Ideal State Criterion
- Remaining risks / parked items

Grok Bot then records status. It does not re-implement.

## 4. Staying aligned with core

`core/` is the source of truth. This adapter does **not** ship a generated `instructions/workflow.md`.

- **Operators in Grok Bot:** do not run adapter sync scripts; wait for Cursor evidence.
- **Maintainers / CI:** `bash adapters/grok-bot/sync/check-core.sh` (also run by `scripts/verify.sh`).

When core advances, update Bot constraint docs here only if the *delivery* rules change. Process or principle changes go to `core/` first.

## Next steps

Open a Grok Bot chat, approve one small brief with a widget, hand it to Cursor, and keep git on the local CLI.
