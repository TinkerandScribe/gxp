# Installing the Grok Build GXP Adapter

This adapter is independent of the chat `gxp` skill (`adapters/grok/`).

## Personas (recommended first step)

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$HOME\.grok\personas"
Copy-Item -Path ".\personas\*.toml" -Destination "$HOME\.grok\personas\" -Force
```

```bash
# macOS / Linux / Git Bash
mkdir -p ~/.grok/personas
cp personas/*.toml ~/.grok/personas/
```

Or project-local (preferred for team repos):

```bash
mkdir -p .grok/personas
cp personas/*.toml .grok/personas/
```

In Grok Build use `/personas` to discover them, then spawn by name.

## Project defaults

Add GXP stop rules to your project root `AGENTS.md` (you can copy the snippet from the main Grok adapter examples).

## Heavy pattern quick start

For high-ambiguity or multi-constraint work:

1. Spawn `gxp-researcher` and `gxp-architect` in parallel.
2. Synthesize their outputs.
3. Run `/plan` with the synthesized GXP plan (must contain 4–8 binary Ideal State Criteria).
4. After approval, implement (composer-coder or native).
5. Spawn `gxp-verifier` for independent Layer-2 checks before rating.

## Verification that this install is safe for grok.com

This adapter never writes to `~/.grok/skills/`. The chat skill remains exactly as it was.
