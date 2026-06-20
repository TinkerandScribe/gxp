# Perplexity AI Workflow Adapter

This is the **Perplexity-optimized** adapter for the GXP (Guided eXecution Protocol) methodology.

## When to use Perplexity

Perplexity is not a coding agent — it's the **research layer**. Reach for it when a GXP task
needs grounded, cited information *before* you write code or commit to an approach.

Use it for:

- **Phase 0 context** — technologies, libraries, recent developments, prior art.
- **Pre-decision research** — best practices and trade-offs before an architecture choice.
- **Competitive / domain background** — a cited briefing on an unfamiliar area.

Then bring the synthesized, cited findings back into your coding agent (Grok, Claude, Cursor).

## Recommended Ways to Use

### 1. Perplexity Collections (Best for Ongoing Work)
Create dedicated Collections for different research areas:
- Technology Research
- Competitive Analysis
- Best Practices & Patterns
- Domain-Specific Knowledge

Use the GXP-optimized prompts from `instructions/` as starting points for threads inside these Collections.

### 2. Focused Research Sessions
When you hit a knowledge gap during a GXP task, spin up a dedicated Perplexity thread using the patterns in this adapter. Bring the synthesized findings back into your main coding/research agent (Grok, Claude, Cursor, etc.).

### 3. Pre-Task Research
Before starting a significant Full Workflow task, use Perplexity to build rich context that you can then feed into your primary agent.

## Design Goals

- Leverage Perplexity’s strengths in fast, high-quality research with citations.
- Provide structured prompts and workflows that produce research outputs that are easy to consume inside the GXP process.
- Keep research tightly scoped to the task brief (avoiding the common Perplexity trap of endless rabbit holes).

## Directory Structure

- `README.md` — This file
- `collections-strategy.md` — Recommended long-term Collection architecture for power users
- `instructions/` — Perplexity-optimized guidance:
  - `research-workflow.md` — How to use Perplexity effectively inside the GXP process
  - `prompt-templates.md` — Large library of ready-to-use research prompts
  - `research-to-brief.md` — How to convert Perplexity output into high-quality GXP task briefs
  - `research-handoff.md` — Template for handing research off to coding agents (Grok, Claude, Cursor, etc.)
  - `focus-modes.md` — Strategic use of Perplexity’s different Focus modes
- `sync/` — Guidance for staying aligned with `core/` over time

## Relationship to Core

This adapter focuses on the **research layer** of the GXP methodology. It helps produce higher-quality Phase 0 context, which leads to better briefs and ultimately better outcomes.

See `../../../core/README.md` and `../../README.md` for more context on the overall model.