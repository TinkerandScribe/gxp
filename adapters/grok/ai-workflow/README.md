# Grok AI Workflow Skill

This is the **Grok-optimized** implementation of the AI Workflow methodology.

## Installation

The canonical source lives in this repository.

To use it, install/symlink this directory into:

```
~/.grok/skills/gxp-ai-workflow/
```

## Design Goals

- Leverage Grok’s strengths (strong tool use, reasoning, context management, and long-context handling).
- Remain fundamentally aligned with the methodology defined in `../../../core/`.
- Provide a convenient way to stay in sync with core over time.

## Staying in Sync with Core

**Strong recommendation:**

Before starting any non-trivial task using the Full workflow, run:

```bash
bash sync/check-core.sh
```

This command will show you what has changed in `core/` since your local copy was last updated.

The `SKILL.md` file contains strong instructions telling Grok to require this check for important work.

## Directory Structure

- `SKILL.md` — The main skill definition loaded by Grok.
- `instructions/` — Grok-specific optimizations and rephrasings of the workflow.
- `sync/` — Tooling to help keep this adapter aligned with the core methodology.

## Relationship to Core

Duplication of content from `core/` is intentional and encouraged when it produces better results with Grok. However, the verification system will flag significant unexplained drift.

See `../../../core/README.md` and `../../README.md` for more context on the overall model.