# Model Routing (Phase 0.5 — Model Selection)

> **Canonical definition:** core/workflow.md Phase 0.5 (tool-agnostic Strategy
> & Model Selection).
>
> This document is the **Claude specialization** of the core process. It sits
> between Phase 0 (repo audit / context) and Phase 1 (Task Brief): once you
> understand the task, deliberately choose the *right model* (or engine) before
> committing to a brief.
>
> Routing decisions are an **adapter-level optimization**. The core principles
> (binary Ideal State Criteria, verification-first, anti-loop, honest ratings)
> are unchanged no matter which engine is chosen.

## Why route at all

Using one model for everything is wasteful in both directions: a frontier model
on trivial mechanical work burns cost and latency for no quality gain, and a
small/cheap model on ambiguous, high-stakes reasoning produces confident-but-wrong
output that the workflow then has to catch. The goal of Phase 0.5 is to spend the
*least* capability that can clear the task's Ideal State Criteria with margin.

**Claude Note**: You are good at honestly assessing task difficulty. Use that in
Phase 0.5 — don't reflexively reach for the biggest model, and don't under-spec a
task you can already tell is genuinely hard.

## Step 1 — Classify the task

From your Phase 0 findings, place the task in one (or more) of these buckets:

- **Research-first** — needs current information, citations, or broad comparison
  before any code/decision is sound.
- **Reasoning-heavy** — ambiguous, multi-file, architectural, security- or
  correctness-critical, or genuinely novel. Getting it *right* dominates.
- **Well-scoped implementation** — the brief is clear, criteria are binary, the
  path is known. Execution dominates over invention.
- **Mechanical / high-volume** — formatting, renames, bulk edits, simple
  classification, first-pass triage. Low ambiguity, high repetition.
- **Autonomous long-run** — a build → verify → reflect loop you want to run many
  steps unattended in a sandbox.
- **In-editor loop** — tight edit/run/verify cycles against a local repo.

## Step 2 — Pick the engine and tier

### Within Claude (default engine for reasoning and writing)

| Task profile | Model | Why |
| --- | --- | --- |
| Reasoning-heavy; Full Workflow default; Phase 2 self-critique; high-stakes review | **Opus 4.8** (`claude-opus-4-8`) | Most capable; best for ambiguity, architecture, correctness. |
| Same as above but latency matters (interactive pairing, quick high-stakes edits) | **Opus 4.8 + Fast mode** (`/fast`) | Opus-level quality with faster output — it does **not** drop to a smaller model. |
| Well-scoped implementation, routine refactors, test writing, clear features | **Sonnet 4.6** (`claude-sonnet-4-6`) | Strong cost/quality balance for the bulk of Phase 3. |
| Mechanical, high-volume, low-ambiguity work | **Haiku 4.5** (`claude-haiku-4-5`) | Cheapest and fastest; ideal for bulk and triage. |

> `Fable 5` (`claude-fable-5`) is also a current top-tier model; prefer it where
> your org's guidance or your own evals say it does better on the task at hand.

**Default rule:** if the task qualifies for the Full Workflow (changes behavior,
touches multiple files, or has meaningful downstream effects), start at **Opus
4.8**. Drop to Sonnet/Haiku only when the work is genuinely well-scoped or
mechanical.

### Hand off to another tool (when available)

This repo ships sibling adapters. Route *out* of Claude when another tool is
clearly better suited, then route the result back:

- **Perplexity** → research-first tasks. Produce a clean handoff using
  [`../../../perplexity/ai-workflow/instructions/research-handoff.md`](../../../perplexity/ai-workflow/instructions/research-handoff.md)
  and feed it into the Context section of the brief.
- **Grok / GXP autonomous loop** → autonomous long-run build-verify-reflect work
  (a Reflexion + self-reward autonomous loop). Use when
  you want many unattended iterations, not a single careful pass.
- **Cursor** → in-editor edit/verify loops on a local repository.
- **Local model** (e.g. Ollama `qwen2.5-coder`, via `LLM_*` env vars) → offline,
  private, zero-cost, or CI/mock runs. Lower capability — reserve for cheap/bulk
  or air-gapped work, never for high-stakes correctness.

## Step 3 — Record the decision in the brief

Add one line to the Phase 1 Task Brief so the choice is explicit and reviewable:

```
Model: <engine + tier>  — <one-line reason tied to the task profile>
e.g. Model: Claude Opus 4.8 — multi-file refactor with correctness-critical edges.
e.g. Model: Perplexity (research) → Claude Sonnet 4.6 — gather sources, then implement.
```

An unrecorded model switch is a silent decision; recording it keeps Phase 0.5
honest and lets the operator override.

## Step 4 — Re-route at the Phase 4 gate

Model choice is not frozen. The anti-loop rule is the natural checkpoint:

- **Escalate** (Haiku → Sonnet → Opus, or Sonnet → Opus + deeper reasoning) when
  the same approach fails twice, the task turns out more ambiguous than Phase 0
  suggested, or verification keeps surfacing subtle correctness issues.
- **De-escalate** when the remaining work collapses into mechanical steps — push
  the long tail to a cheaper tier.
- **Switch tools** when the failure mode points elsewhere (e.g. you're guessing at
  facts → hand off to Perplexity; you need many unattended iterations → hand off
  to the Grok loop).

Whenever you re-route, update the `Model:` line and note *why* — this is failure
signal worth keeping.

## Anti-Patterns

- Defaulting to the largest model for trivial, reversible, single-file work.
- Using a weak local model for correctness- or security-critical tasks because
  it's free.
- Switching models mid-task without recording the reason in the brief.
- Routing research to a model with no live sources, then trusting the recall.
- Treating Fast mode as a quality downgrade — it is not; it is Opus, faster.

## Relationship to Core

Routing lives only in adapters — it is a way to apply the *same* methodology more
efficiently across the models you have. If a routing rule starts changing the
*process* (not just which model runs it), that change belongs in `../../../core/`
first. See `../../../core/README.md` and `../../README.md`.
