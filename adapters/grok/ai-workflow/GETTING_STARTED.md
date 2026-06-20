# Getting Started with the Grok AI Workflow Skill

This guide helps individual power users get the GXP skill running quickly and effectively.

## What This Skill Gives You

- A structured, verification-first workflow optimized for Grok's strengths (tool use, long context, reasoning).
- Strong guardrails against scope creep and repeated mistakes.
- Built-in mechanisms to stay aligned with the evolving core methodology.
- Ratings + failure capture so the process improves over time.

## 1. Installation (Windows)

The easiest way:

```powershell
cd path\to\gxp\adapters\grok\ai-workflow\sync
.\install-grok-skill.ps1
```

This will create a directory junction (preferred) or copy the skill into:

```
$HOME\.grok\skills\gxp-ai-workflow\
```

After installation, the skill is available in your Grok chats under the short name **gxp** (recommended — just say "use gxp") as well as the longer name `gxp-ai-workflow`.

**Alternative (manual):**
Copy or symlink the entire `adapters/grok/ai-workflow/` folder to `~/.grok/skills/gxp-ai-workflow/`.

## 2. First Run – Verify Everything Works

From inside the installed skill directory, run:

```powershell
.\sync\check-core.ps1
```

You should see output showing the current sync status with `core/`.

On first use it will likely show differences — this is normal while the Grok version is still maturing.

Use `-Lenient` while actively developing your personal version of the workflow:

```powershell
.\sync\check-core.ps1 -Lenient
```

## 3. How to Use the Skill Day-to-Day

1. Start a new Grok chat and invoke the skill (or reference it in your prompt).
2. For any non-trivial task, the skill will remind you to run the sync check.
3. Follow the workflow in `instructions/workflow.md` (Grok-optimized version).
4. Use the extra guidance files:
   - `instructions/context-loading.md`
   - `instructions/tool-use-patterns.md`

## 4. Staying in Sync (Anti-Entropy)

The skill includes strong mechanisms so it doesn't drift from the source of truth:

- **Marker system**: The workflow file contains a "Last synced from core" line.
- **check-core.ps1** (or `.sh`): Run this regularly.
- **drift-allowlist.txt**: Explicitly declare intentional divergences so the checker doesn't nag you.

**Recommended habit:**
- Run the check before any important or complex task.
- When core advances, decide whether to adopt the changes or update the allowlist with a comment explaining why you're diverging.

## 5. Customization

This is *your* toolkit. Feel free to:

- Heavily customize `instructions/workflow.md` for how you like working with Grok.
- Add new files in `instructions/`.
- Extend the allowlist.
- Modify `SKILL.md` to change how the skill presents itself.

Just keep the sync discipline so the methodology stays coherent over time.

## 6. Making GXP Easy to Use (Discoverability)

For maximum convenience, add the helper functions to your PowerShell profile.

### One-time setup (recommended)

1. Open your profile:
   ```powershell
   notepad $PROFILE
   ```

2. Add this line (update the path if your repo is elsewhere):
   ```powershell
   . "C:\path\to\gxp\adapters\grok\ai-workflow\gxp.ps1"
   ```

3. Save and reload:
   ```powershell
   . $PROFILE
   ```

After that you can use these tools from anywhere (recommended subcommand style):

- `gxp check` → Run the sync check against core methodology
- `gxp open` → Open the skill folder in Explorer
- `gxp test` → Print a good test prompt
- `gxp install` → Re-install or repair the skill
- `gxp root` (or `gxp cd`) → cd into the skill folder
- `gxp edit` → Open key workflow files for editing
- `gxp new-brief` (or `gxp brief`) → Start a new task brief from the template
- `gxp help` → Show all available tools

The old flat names (`gxp-check`, `gxp-open`, etc.) still work for backward compatibility.

There's also a ready-made snippet at:
`profile/gxp-profile-snippet.ps1`

## 7. Tips for Power Users

- Use `-FullDiff` when you want to deeply review changes.
- Keep the allowlist honest — only add things you have a real reason to diverge on.
- Periodically review the core methodology even if you're mostly using the Grok-optimized version.
- The ratings + failure capture system is extremely valuable — be honest when rating runs.

## 8. Grok Build Strategy Selection (Prototype)

When running inside Grok Build, the GXP skill now includes early strategy classification (see `instructions/strategy-selection.md` and the new section in `instructions/workflow.md`).

This lets you automatically choose:
- `composer-coder` persona (Composer 2.5) for strong multi-file coding
- `grok-native-planner` for ambiguity and planning
- Cursor Composer handoff when the IDE/visual context wins

Sample personas live in `examples/grok-build-strategy/personas/`.

Copy them to `~/.grok/personas/` (or project `.grok/personas/`) and the agent will discover them for `spawn_subagent`.

Example classification decision will appear in your transcript for qualifying tasks. It uses GXP brief/criteria language and notes capability (external_apis).

This prototype advances the coordination brief without touching the upstream orchestrator.

## Next Steps

- Run the check script now.
- Try a small task using the Full workflow.
- Customize the workflow file to better match your personal style.
- Come back and contribute improvements to the broader `gxp` project when you discover better patterns.

Welcome to the workflow. Use it deliberately, measure it, and keep making it better.