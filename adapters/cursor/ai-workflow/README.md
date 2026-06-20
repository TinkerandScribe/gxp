# Cursor AI Workflow Adapter

The Cursor-specific implementation of the GXP (two-pass) AI workflow methodology.
This adapter makes Cursor follow the full L3/L4 bounded-agent loop defined in
`core/workflow.md`.

## What This Adapter Does

- Installs a Cursor `.mdc` rule that enforces the GXP workflow phases
- Adds Cursor-native operating guidance (Composer, terminal, @-references)
- Encodes a verification output contract so Phase 5 always produces real evidence
- Scopes Cursor to the task brief, preventing scope expansion during Composer edits
- Enforces PowerShell-compatible command generation on Windows hosts

## Relationship to Core

This adapter is a **compressed summary** of `core/workflow.md` — intentionally shorter
because Cursor rules should be concise and directly actionable. The authoritative
methodology lives in `core/workflow.md`. When the two appear to conflict, `core/` wins.

The path-mapping block in `rule.mdc` handles the two operating modes:
- **In a target repo**: reads `.ai/` scaffold (install via `scripts/install-ai-from-core.ps1`)
- **In gxp itself**: reads `core/` directly

## Installation

### Recommended (from gxp repo)

```powershell
# Workflow rule only
powershell -ExecutionPolicy Bypass -File adapters\cursor\ai-workflow\sync\install-cursor-rule.ps1 `
  -TargetRepo C:\path\to\project -Force

# Optional: generic security.mdc (only if missing)
powershell -ExecutionPolicy Bypass -File adapters\cursor\ai-workflow\sync\install-cursor-rule.ps1 `
  -TargetRepo C:\path\to\project -Force -IncludeSecurityTemplate
```

`-Force` overwrites **only** `ai-workflow.mdc`. Other `.cursor/rules/*.mdc` files are preserved.

### Full scaffold + Cursor rule

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-ai-from-core.ps1 `
  -TargetRepo C:\path\to\project -Force -IncludeCursorRule
```

### Manual

Copy `rule.mdc` to `.cursor/rules/ai-workflow.mdc`. Optionally copy
`security.mdc.template` to `security.mdc` and customize.

## Drift Detection

A structural drift check is encoded in the rule itself via the **version contract**:
the rule states which version of `core/workflow.md` it implements. If you update
`core/workflow.md` to a new version, grep `rule.mdc` for the version string and
update it (and any changed phase descriptions) to match.

Quick check:
```powershell
Select-String "v1\." adapters\cursor\ai-workflow\rule.mdc
Select-String "^## Version" core\workflow.md
```

## Testing the Adapter

Open a new Cursor chat and paste the contents of `TEST_PROMPT.md`.
Score: 9-10 correct = working well. Less than 7 = check the rule is installed.

## Maintenance

- When `core/workflow.md` bumps its version, update the version string in `rule.mdc`
  and adjust any phase descriptions that changed.
- Keep `rule.mdc` concise. Deeper guidance lives in `instructions/` sub-files (future).
- Do not mirror the full `core/workflow.md` text into `rule.mdc` — compression is
  intentional. The rule is a behaviour contract, not a documentation copy.
- Run `sync\check-core.ps1` after any edits to verify structural alignment.
