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

Use personas (gxp-researcher, gxp-architect, composer-coder, grok-native-planner, **gxp-verifier**) with `spawn_subagent` for automatic switching inside the session. Prefer parallel researcher + architect for high-ambiguity / multi-constraint front-half work (see strategy-selection.md).

For Cursor: emit a self-contained GXP brief + ready-to-paste prompt that follows the Cursor adapter rules.

Always log the decision with binary justification and a capability note. This advances the coordination brief at `core/tasks/EXAMPLE-feature-brief.md`.

### Plan Mode = heavy GXP front half (Grok Build)

There is no separate “expert mode.” For serious work, prefer:

1. Suggest **`/plan <task>`** when the ask is multi-file, multi-constraint, high-stakes,
   or underspecified (operator did not supply ~4+ binary criteria).
2. Plan content must be GXP-shaped: goal, 4–8 Ideal State Criteria, out of scope,
   verification plan, Phase 0 files to read.
3. Do not treat plan approval as “tests already passed” — after execute, still run
   Phase 5 (two-layer verify). Optionally spawn **gxp-verifier** for criteria-only review.

See `GETTING_STARTED.md` §4 and `examples/AGENTS.gxp-snippet.md` for project defaults.

## Full Workflow (Phases 0–8)

Follow the detailed process in `instructions/workflow.md`.

Key reminders:
- Binary, checkable Ideal State Criteria are sacred.
- Deterministic verification **before** subjective judgment.
- Strong enforcement of the anti-loop rule (Phase 4).
- Honest rating (Phase 6) and meaningful failure capture (Phase 7).

### Scaffolding tier (Phase 0.5)

After choosing the engine/model, also set **Scaffolding tier:**
`frontier` | `standard` | `constrained` (default **standard** if unknown).

- **frontier** — minimal host scaffolding; high-level goal + binary criteria
- **standard** — default GXP intensity
- **constrained** — denser steps/gates (older, local, or unproven models)

Detection: explicit brief / operator / `GXP_SCAFFOLDING_TIER` → model map → **standard**.
Never auto-pick `frontier` without a known model id or explicit override.
Tier does **not** relax verification, binary criteria, anti-loop, or privacy/stakes rails.
Ablation of host system prompts/skills is operator-approved only.

Canonical: `core/docs/capability-scaffolding.md` (bundled under `docs/` in this skill when present).

## Evidence-backed non-negotiables (Grok Build)

These encode eval findings (weak public green, thin prompts). They do not replace core:

1. **Phase 0 before code** when the operator ask is underspecified (fewer than ~4 binary criteria, or multi-factor and vague). Open `PROGRAM.md` / `rules/` / `failures/` when present.
2. **Never treat weak public/smoke green as full done** on multi-file or multi-constraint work — walk each Ideal State Criterion with a tool check.
3. **4–8 binary criteria** before multi-file implementation.
4. **Two-layer verify** when smoke is thin: project suite first, then criterion-driven edges (fail-closed, isolation, state transitions, etc.).
5. **Handoff** states what was verified and which commands/tools produced the evidence.

## Lightweight Workflow

Use only for trivial, low-risk, single-file, easily reversible changes with a clear strong verify path.

If the task grows, smoke is thin, or criteria are mostly invented by you, immediately upgrade to the Full workflow and run the sync check.

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