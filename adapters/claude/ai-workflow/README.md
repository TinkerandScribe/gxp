# Claude AI Workflow Adapter

This is the **Claude-optimized** implementation of the AI Workflow methodology (GXP).

## How to Use with Claude

Claude has two main ways to use custom workflows:

### 1. Claude Projects (Recommended)
This is the best long-term way to use GXP with Claude.

1. Go to [claude.ai](https://claude.ai) and create a new **Project**.
2. In the Project settings, paste the contents of:
   - `instructions/workflow.md` (as the main custom instructions)
3. (Optional but recommended) Upload relevant files from `core/` as Project Knowledge:
   - `core/workflow.md`
   - `core/PROGRAM.template.md`
   - `core/templates/task-brief.md`
   - `core/templates/failure-capture.md`

### 2. Regular Chat Custom Instructions
If you want to use GXP outside of Projects:

1. Go to your Claude settings → **Custom Instructions**.
2. Paste the content from `instructions/workflow.md`.
3. Optionally add the content from `core/` files as well.

## Design Goals

- Leverage Claude’s strengths (careful reasoning, excellent instruction following, strong writing, and thoughtful analysis).
- Remain fundamentally aligned with the methodology defined in `../../../core/`.
- Provide clear, high-signal instructions that work well with Claude’s preferences.

## Staying in Sync with Core

**Recommended practice:**

Before starting any major task using the Full workflow, review the latest version of `core/workflow.md` (or run the local sync check if you also use the Grok version of this toolkit).

The Claude adapter is intentionally allowed to diverge from core where it produces meaningfully better results with Claude, but we still want to stay philosophically aligned.

## Directory Structure

- `README.md` — This file (usage instructions for Claude)
- `custom-instructions.md` — Ready-to-paste block for Claude Custom Instructions or Projects
- `instructions/` — Claude-optimized guidance:
  - `workflow.md` — Full Claude-adapted workflow
  - `context-loading.md` — Effective context strategies for Claude
  - `reasoning-patterns.md` — How to leverage Claude’s strengths in reasoning and self-critique
  - `model-routing.md` — Phase 0.5 guide for routing tasks to the right Claude tier or sibling tool
- `sync/` — Documentation for staying aligned with `core/` over time

## Recommended Project Setup (Best Experience)

When creating a Claude Project for ongoing GXP work:

1. Paste the contents of `custom-instructions.md` into the Project’s custom instructions.
2. Upload the following as Project Knowledge (highly recommended):
   - `../../../core/workflow.md`
   - `../../../core/PROGRAM.template.md`
   - `../../../core/templates/task-brief.md`
   - `../../../core/templates/failure-capture.md`
   - `instructions/reasoning-patterns.md`
   - `instructions/model-routing.md`
3. For each new significant task, start a new conversation inside the Project and explicitly invoke GXP mode.

## Relationship to Core

Like the other adapters, this one is allowed (and encouraged) to adapt the core methodology to play to Claude’s specific strengths, while keeping the fundamental principles intact (binary criteria, verification-first, anti-loop discipline, honest ratings, etc.).

See `../../../core/README.md` and `../../README.md` for more context on the overall model.