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

This installs (junction or symlink) to `~/.grok/skills/gxp-ai-workflow/` and re-points the
legacy alias `~/.grok/skills/tinker-tools-ai-workflow/` to the same adapter so old skill
paths stay current. It also installs example personas into `~/.grok/personas/*.toml`
(use `-Force` / `--force` to refresh without prompts; `-SkipPersonas` / `--skip-personas`
to skip). The skill is available as **gxp** (say "use gxp") or `gxp-ai-workflow`.

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

## 4. Heavy / “expert” work in Grok Build = Plan Mode + GXP

Grok Build has no separate “expert mode” flag. For serious multi-file or high-stakes
work, use **Plan Mode**, then execute under GXP:

1. In the TUI: `/plan <what you want done>` (or `/plan` then describe the task).
2. Require the plan to include: **goal**, **4–8 binary Ideal State Criteria**,
   **out of scope**, **verification plan**, and **Phase 0 files to open**
   (`.ai/PROGRAM.md`, `rules/`, `failures/` when present).
3. Review and approve only when criteria are checkable (not vague).
4. After approval, implement under full GXP; do **not** treat thin public/smoke
   green as done — walk each criterion (two-layer verify).
5. Optional: spawn the **gxp-verifier** persona for Layer 2 (criteria-only critic).

**When to force this path (auto-suggest `/plan`):** multi-file work, multi-constraint
behavior, thin smoke tests, or an underspecified operator ask.

**When lightweight is fine:** single-file reversible fix with a strong named verify.

### Project defaults without full `.ai/` install

Copy `examples/AGENTS.gxp-snippet.md` into your project root `AGENTS.md` so Grok Build
always sees stop-rule defaults for that repo.

### Personas (optional)

Example personas under `examples/grok-build-strategy/personas/`:

| Persona | Use |
|---------|-----|
| `grok-native-planner` | Ambiguity / architecture; pair with `/plan` |
| `composer-coder` | Coherent multi-file implement |
| `gxp-verifier` | Criteria-only verify after implement |

`install-grok-skill` copies these into `~/.grok/personas/*.toml` (Grok discovers
file-based personas there — a single file named `personas` is wrong and is repaired).
Or copy into project `.grok/personas/` for repo-local personas. Manage via `/personas`.

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
