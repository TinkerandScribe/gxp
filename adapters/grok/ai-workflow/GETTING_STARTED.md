# Getting Started — Grok GXP Skill

Get the GXP skill running in Grok in a few minutes.

## What it gives you

- A verification-first workflow tuned for Grok (tool use, long context, reasoning).
- Guardrails against scope creep and repeated mistakes.
- Ratings + failure capture so the process improves over time.

## 1. Install

**Windows:**

```powershell
cd path\to\gxp\adapters\grok\ai-workflow\sync
.\install-grok-skill.ps1
```

**macOS / Linux:** `bash sync/install-grok-skill.sh`

This installs (junction or copy) to `~/.grok/skills/gxp-ai-workflow/`. The skill is then
available in Grok chats as **gxp** (just say "use gxp") or the long name `gxp-ai-workflow`.
Manual alternative: copy or symlink `adapters/grok/ai-workflow/` to that path.

## 2. Verify it works

From the installed skill directory:

```powershell
.\sync\check-core.ps1        # or: bash sync/check-core.sh
```

This reports sync status against `core/`. Some differences are normal (Grok-specific
optimizations). Add `-Lenient` while you're customizing.

## 3. Use it day-to-day

1. Start a Grok chat and say "use gxp" (or reference the skill).
2. For non-trivial work it follows the full loop in `instructions/workflow.md`.
3. Run the sync check (step 2) before important tasks.

Extra Grok-specific guidance lives in `instructions/context-loading.md` and
`instructions/tool-use-patterns.md`.

## Staying in sync (anti-entropy)

The skill is designed not to drift from `core/`:

- `instructions/workflow.md` carries a "Last synced from core" marker.
- `sync/check-core.*` reports drift — run it before important work.
- `sync/drift-allowlist.txt` declares intentional divergences so the checker won't nag.

When core advances, either adopt the change or add an allowlist line explaining why you diverge.

## Going further (optional)

- **PowerShell shortcuts** — source `gxp.ps1` from your `$PROFILE` for `gxp check`,
  `gxp brief`, `gxp open`, etc. Ready-made snippet: `profile/gxp-profile-snippet.ps1`.
- **Customize** — this is your toolkit: edit `instructions/workflow.md`, add files under
  `instructions/`, or adjust `SKILL.md`. Keep the sync discipline so the methodology stays coherent.
- **Grok Build strategy selection (prototype)** — auto-pick a persona (Composer 2.5 vs
  native planner) or a Cursor handoff. See `instructions/strategy-selection.md` and
  `examples/grok-build-strategy/`.

## Next steps

Run the sync check, try a small task with the Full workflow, and rate it honestly.
