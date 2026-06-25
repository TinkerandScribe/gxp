# Model Routing (Phase 0.5 — Model Selection)

> **Canonical definition:** core/workflow.md Phase 0.5 (tool-agnostic Strategy
> & Model Selection).
>
> This document is the **ChatGPT specialization** of the core process. It sits
> between Phase 0 (repo audit / context) and Phase 1 (Task Brief): once you
> understand the task, deliberately choose the *right model* (or engine) before
> committing to a brief.
>
> Routing decisions are an **adapter-level optimization**. The core principles
> (binary Ideal State Criteria, verification-first, anti-loop, honest ratings)
> are unchanged no matter which engine is chosen.

## Why route at all

Using one model for everything is wasteful in both directions: a reasoning model
on trivial mechanical work burns cost and latency for no quality gain, and a
fast default model on ambiguous, high-stakes work produces confident-but-wrong
output that the workflow then has to catch. The goal of Phase 0.5 is to spend the
*least* capability that can clear the task's Ideal State Criteria with margin.

**ChatGPT Note**: Model names and availability change. Classify the *task profile*
first; map to the best current ChatGPT tier second. Record the actual model used
in the brief.

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

### Within ChatGPT (default engine for planning and explanation)

| Task profile | Model tier | Why |
| --- | --- | --- |
| Reasoning-heavy; Full Workflow default; architecture; security review; Phase 2 self-critique | **o3** or latest **reasoning** model | Extended reasoning for ambiguity and correctness-critical edges. |
| Same profile but lower latency / cost acceptable | **o4-mini** (or current mini reasoning tier) | Reasoning with faster turnaround for interactive pairing. |
| Well-scoped implementation, routine refactors, test writing, clear features | **GPT-4o** | Strong default for structured implementation and synthesis. |
| Mechanical, high-volume, low-ambiguity work | **GPT-4o mini** | Cheapest and fastest; ideal for bulk and triage. |

**Default rule:** if the task qualifies for the Full Workflow (changes behavior,
touches multiple files, or has meaningful downstream effects), start at a
**reasoning** tier (o3 / o4-mini). Drop to GPT-4o / mini only when the work is
genuinely well-scoped or mechanical.

### Hand off to another tool (when available)

This repo ships sibling adapters. Route *out* of ChatGPT when another tool is
clearly better suited, then route the result back:

- **Perplexity** → research-first tasks with live citations. Produce a clean
  handoff and feed it into the Context section of the brief.
- **Strong coding agent / Cursor** → in-repo edit, test, and verify loops on a local
  repository. ChatGPT plans and briefs; the IDE agent executes deterministically.
- **Grok / GXP autonomous loop** → autonomous long-run build-verify-reflect work
  (a Reflexion + self-reward autonomous loop). Use for many unattended iterations,
  not a single careful pass.
- **Local model** (e.g. Ollama) → offline, private, zero-cost runs. Lower
  capability — reserve for cheap/bulk or air-gapped work, never for high-stakes
  correctness.

## Step 3 — Record the decision in the brief

Add one line to the Phase 1 Task Brief so the choice is explicit and reviewable:

```
Model: <engine + tier>  — <one-line reason tied to the task profile>
e.g. Model: ChatGPT o3 — multi-file security fix with correctness-critical edges.
e.g. Model: Perplexity (research) → GPT-4o — gather sources, then implement.
```

An unrecorded model switch is a silent decision; recording it keeps Phase 0.5
honest and lets the operator override.

## Step 4 — Re-route at the Phase 4 gate

Model choice is not frozen. The anti-loop rule is the natural checkpoint:

- **Escalate** (mini → GPT-4o → reasoning) when the same approach fails twice,
  the task turns out more ambiguous than Phase 0 suggested, or verification keeps
  surfacing subtle correctness issues.
- **De-escalate** when the remaining work collapses into mechanical steps.
- **Switch tools** when the failure mode points elsewhere (facts → Perplexity;
  runnable tests in repo → strong coding agent or Cursor; unattended loops → Grok autonomous loop).

Whenever you re-route, update the `Model:` line and note *why*.

## Anti-Patterns

- Defaulting to a reasoning model for trivial, reversible, single-file work.
- Using GPT-4o mini for security- or correctness-critical tasks because it is fast.
- Switching models mid-task without recording the reason in the brief.
- Claiming verification passed in ChatGPT without Code Interpreter or user-confirmed runs.
- Treating web browsing output as verified fact without sources in the brief.

## Relationship to Core

Routing lives only in adapters — it is a way to apply the *same* methodology more
efficiently across the models you have. If a routing rule starts changing the
*process* (not just which model runs it), that change belongs in `../../../core/`
first. See `../../../core/README.md` and `../../README.md`.