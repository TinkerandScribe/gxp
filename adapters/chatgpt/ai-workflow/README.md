# ChatGPT AI Workflow Adapter

This is the **ChatGPT-optimized** implementation of the GXP methodology.

## How to Use with ChatGPT

Choose the surface that matches the work. **Use Codex for repository edits, commands,
tests, and review.** This adapter covers the ChatGPT side of the workflow: planning,
research, decision-making, and portable handoffs.

### 1. ChatGPT Project (Recommended for ongoing GXP work)

Projects keep chats, reference files, and project instructions together. They are the
best ChatGPT home for a stream of related briefs, research, and handoffs.

1. Create a ChatGPT Project and add the principles in `custom-instructions.md` as
   Project instructions.
2. Add the following as Project sources:
   - `../../../core/workflow.md`
   - `../../../core/PROGRAM.template.md`
   - `../../../core/templates/task-brief.md`
   - `../../../core/templates/failure-capture.md`
   - `instructions/model-routing.md`
   - `instructions/context-loading.md`
   - `../../codex/instructions/codex-handoff.md` (required shape for execution handoffs)
3. Start one chat per significant task, keep the brief and source links in the Project,
   and hand repository implementation to Codex with the required context and criteria.

### 2. Custom GPT (Optional reusable persona)

Create a Custom GPT when you want a reusable GXP planning and research persona across
unrelated work. Paste `custom-instructions.md` into its Instructions field and upload
the same core documents as Knowledge. Do not treat a Custom GPT as a substitute for a
repo-aware coding agent.

### 3. Account Custom Instructions (Personal defaults only)

If you want GXP principles outside a Project or Custom GPT:

1. Open ChatGPT Settings and add `custom-instructions.md` to Custom Instructions.
2. Keep these instructions generic; put repository-specific commands and constraints in
   the Project or in Codex `AGENTS.md` guidance.

## Design Goals

- Leverage ChatGPT's strengths: structured output, source synthesis, planning, and research.
- Make the boundary explicit: ChatGPT produces plans, research, and handoffs; Codex owns
  repository execution and deterministic verification.
- Remain fundamentally aligned with the methodology defined in `../../../core/`.

## Staying in Sync with Core

Before starting any major task using the Full workflow, review the latest
`core/workflow.md` or run the local sync check:

```powershell
.\sync\check-core.ps1 -Lenient
```

```bash
bash sync/check-core.sh --lenient
```

The ChatGPT adapter may diverge from core where it produces meaningfully better results
with ChatGPT, but it must remain philosophically aligned.

## Directory Structure

- `README.md` — usage instructions for ChatGPT
- `custom-instructions.md` — ready-to-paste principles for Project, Custom GPT, or account settings
- `instructions/`:
  - `workflow.md` — generated ChatGPT-adapted workflow
  - `context-loading.md` — Project, Knowledge, and handoff context strategies
  - `model-routing.md` — Phase 0.5 routing between ChatGPT and Codex
- `TEST_PROMPT.md` — separate ChatGPT planning and Codex execution tests
- `sync/` — tooling to stay aligned with core

## Relationship to Core

Like the other adapters, this one adapts the core methodology to play to ChatGPT's
strengths while keeping binary criteria, verification-first work, the anti-loop rule,
honest ratings, and failure capture intact.

For repository execution, see the dedicated [`../../codex/README.md`](../../codex/README.md).
See `../../../core/README.md` and `../../README.md` for the overall model.
