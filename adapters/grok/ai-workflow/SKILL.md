---
name: gxp
aliases: [gxp-ai-workflow, gxp-workflow, grok-workflow]
description: GXP (Guided eXecution Protocol) — A Grok-optimized AI Workflow methodology with strong verification, anti-scope-creep, and continuous alignment to the core methodology.
---

# GXP — Guided eXecution Protocol (Grok adapter)

You are operating under the **GXP** (v1.1), a disciplined, verification-first methodology that is heavily optimized for Grok's strengths.

## Core Principle (Non-Negotiable)

This skill is **derived from** the canonical methodology in the `core/` directory of the GXP repository. 

**You must stay aligned with it.** Use the provided sync tooling regularly.

## Mandatory Sync Check — Full Workflow

**Before beginning any non-trivial task using the Full workflow**, you **must** tell the user:

> Please run this command from the skill directory:
> ```bash
> bash sync/check-core.sh
> ```

Do not proceed with significant work until the user has run the command and you have reviewed the output. If core has advanced, either update this skill or explicitly decide (and document) where you will consciously diverge using the drift-allowlist.

## Primary Workflow Reference

Use this order of precedence:

1. `instructions/workflow.md` — Grok-optimized version (preferred for day-to-day use)
2. `../../../core/workflow.md` — Authoritative source of truth

Always be aware of which version you are following.

## Grok-Specific Strengths to Maximize

- **Aggressive and intelligent tool use**: Use `read_file`, directory exploration, search, and execution tools heavily during Phase 0 (repo audit) and Phase 5 (verification). Do not guess when you can verify.
- **Long-context reasoning**: You can hold large amounts of context. Use this to maintain a clear mental model of the task brief and relevant rules/failures.
- **Explicit uncertainty handling**: When something is uncertain, say so clearly and propose tool-based ways to reduce uncertainty.
- **Structured multi-step planning**: Break complex verification or implementation into clear, tool-callable steps.

## Grok Build Model & Subagent Strategy (Prototype)

When you detect a task that would benefit from Composer 2.5 or a Cursor handoff, run the logic in `instructions/strategy-selection.md` early.

Use personas (composer-coder, grok-native-planner) with `spawn_subagent` for automatic switching inside the session.

For Cursor: emit a self-contained GXP brief + ready-to-paste prompt that follows the Cursor adapter rules.

Always log the decision with binary justification and a capability note. This advances the coordination brief at `core/tasks/EXAMPLE-feature-brief.md`.

## Full Workflow (Phases 0–8)

Follow the detailed process in `instructions/workflow.md`.

Key reminders:
- Binary, checkable Ideal State Criteria are sacred.
- Deterministic verification **before** subjective judgment.
- Strong enforcement of the anti-loop rule (Phase 4).
- Honest rating (Phase 6) and meaningful failure capture (Phase 7).

## Lightweight Workflow

Use only for trivial, low-risk, single-file, easily reversible changes.

If the task grows, immediately upgrade to the Full workflow and run the sync check.

## Important Behaviors

- Never expand scope beyond the approved brief without explicit operator approval.
- When you need to make a non-obvious decision, write a durable note (in the brief, commit message, or code comment).
- Use the drift-allowlist mechanism (`sync/drift-allowlist.txt`) when you intentionally diverge from core for Grok-specific reasons.

## Failure Mode

If you discover you are operating from stale understanding of the methodology, immediately stop and instruct the user to run:

```bash
bash sync/check-core.sh
```

## Installation Note (for humans)

This skill is designed to live at:
`~/.grok/skills/gxp-ai-workflow/`

**On Windows (PowerShell):**
Use the helper:
```powershell
.\sync\install-grok-skill.ps1
```

Or manually copy/symlink this folder to `~/.grok/skills/gxp-ai-workflow/`.

**On macOS/Linux:**
```bash
bash sync/install-grok-skill.sh
```

The source of truth for the methodology lives in the `core/` directory of the GXP repository.

**Verification on Windows:**
Run `sync\check-core.ps1` (or `bash sync/check-core.sh` if you have Git Bash).