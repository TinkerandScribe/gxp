# Installing the Grok Build GXP Adapter

This adapter is independent of the chat `gxp` skill (`adapters/grok/`).

## Recommended: install scripts

From this directory (`adapters/grok-build/`):

```powershell
# Windows PowerShell ΓÇö personas only (default)
.\install-grok-build.ps1
.\install-grok-build.ps1 -Force

# Optional: also install Build skill as ~/.grok/skills/gxp-build
.\install-grok-build.ps1 -Force -InstallSkill
```

```bash
# macOS / Linux / Git Bash ΓÇö personas only (default)
bash install-grok-build.sh
bash install-grok-build.sh --force

# Optional: also install Build skill
bash install-grok-build.sh --force --install-skill
```

| Flag | Effect |
|------|--------|
| `-Force` / `--force` | Overwrite existing personas / `gxp-build` skill without prompts |
| `-SkipPersonas` / `--skip-personas` | Do not touch `~/.grok/personas` |
| `-InstallSkill` / `--install-skill` | Install **only** `~/.grok/skills/gxp-build` (opt-in; default off) |

## Manual personas

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.grok\personas"
Copy-Item -Path ".\personas\*.toml" -Destination "$HOME\.grok\personas\" -Force
```

```bash
mkdir -p ~/.grok/personas
cp personas/*.toml ~/.grok/personas/
```

Or project-local (preferred for team repos):

```bash
mkdir -p .grok/personas
cp personas/*.toml .grok/personas/
```

In Grok Build use `/personas` to discover them, then spawn by name.

## Optional skill (`gxp-build`)

Default install is **personas-only** and does not write under `~/.grok/skills/`.

With `-InstallSkill` / `--install-skill`, the installer creates a junction/symlink
(or copy fallback) at:

```text
~/.grok/skills/gxp-build  ΓåÆ  this adapter directory
```

Skill frontmatter name: `gxp-build` (aliases are Build-specific only).

## Chat skill isolation (hard rule)

Installers **never** create, remove, or rewrite:

- `~/.grok/skills/gxp-ai-workflow` (chat skill)
- `~/.grok/skills/tinker-tools-ai-workflow` (legacy chat alias)

Those paths belong exclusively to `adapters/grok/ai-workflow/sync/install-grok-skill.*`.

## Project defaults

Add GXP stop rules to your project root `AGENTS.md` (you can copy the snippet from the main Grok adapter examples).

## Sync check

```bash
# From repo root
bash adapters/grok-build/sync/check-core.sh
```

```powershell
# From this adapter directory
.\sync\check-core.ps1
```

Lightweight presence + integrity only (required files, SKILL name, persona model
convention, install isolation markers). Intentional packaging notes:
`sync/drift-allowlist.txt`.

## Heavy pattern quick start

For high-ambiguity or multi-constraint work:

1. Spawn `gxp-researcher` and `gxp-architect` in parallel.
2. Synthesize their outputs.
3. Run `/plan` with the synthesized GXP plan (must contain 4ΓÇô8 binary Ideal State Criteria).
4. After approval, implement (composer-coder or native).
5. Spawn `gxp-verifier` for independent Layer-2 checks before rating.

## Note on dual persona installers

Both the chat installer (`install-grok-skill`) and this Build installer may write the same
persona basenames under `~/.grok/personas/`. Last install wins; use `-Force` deliberately.
