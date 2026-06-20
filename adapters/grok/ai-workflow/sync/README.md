# Sync with Core

This directory contains tooling to help keep the Grok AI Workflow skill aligned with the canonical methodology in `core/`.

## Recommended Command

**Before any significant work**, run:

```bash
bash sync/check-core.sh
```

By default, differences on **critical files** (especially the workflow definition) cause a non-zero exit. This enforces strong verification/anti-entropy.

## What the Script Checks

- Core workflow definition (against `instructions/workflow.md`)
- Key templates (task brief, failure capture, weekly refine)
- Important supporting files (PROGRAM template, ratings schema)
- Core philosophy files (`rules/README.md`, `failures/README.md`)
- Presence of sync instructions inside `SKILL.md`

It is intentionally **not exhaustive** — it focuses on high-signal files.

### Useful Flags

- `--quiet`     → Minimal output
- `--strict`    → Treat missing files and structural gaps as errors
- `--lenient`   → Do not fail on diffs (useful during active development of the Grok version)
- `--full-diff` → Show complete diffs
- `--help`      → Show all options

Examples:
```bash
bash sync/check-core.sh --strict
bash sync/check-core.sh --lenient
bash sync/check-core.sh --quiet --lenient
```

**Windows / PowerShell:** use `check-core.ps1`. If the full colored output appears
to hang in some terminals, run with `-Quiet` (exit code is still authoritative for CI).

## Current Status

The script is implemented and functional. It will continue to be refined as the Grok adapter and core methodology evolve.

## Philosophy

The goal is not strict 1:1 parity. The goal is **informed alignment** — the Grok version should know when the source of truth has changed so it can decide whether to adopt the change or consciously diverge for Grok-specific reasons.