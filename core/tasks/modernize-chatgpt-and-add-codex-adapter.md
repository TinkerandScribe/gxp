# Task brief

**Date:** 2026-07-25
**Task slug:** modernize-chatgpt-and-add-codex-adapter
**Workflow:** full

## Goal

Modernize the ChatGPT adapter for current ChatGPT Project/Work and Codex workflows, and add a dedicated Codex adapter without changing GXP core or existing non-ChatGPT adapters.

## Context

- Related files: `adapters/chatgpt/ai-workflow/`, `adapters/README.md`, `README.md`, `CONTRIBUTING.md`, `scripts/verify.sh`.
- Relevant `.ai/rules/` entries: `core/rules/01-no-secrets-in-git.md`; `core/rules/02-local-context-never-committed.md`.
- Relevant `.ai/failures/` entries: `core/failures/verification-wrapper-swallows-exit-codes.md`; `core/failures/webfetch-summarizer-invents-plausible-details.md`.
- Background: current official guidance distinguishes ChatGPT Projects and Work from Codex's repository-native workflow; old hard-coded model routing is no longer suitable.

**Strategy/Model:** Codex with current OpenAI documentation — the work is multi-file and needs precise, current product-surface guidance plus local verification.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [chatgpt | codex]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human
- **output_contract:** focused documentation and adapter files with deterministic verification evidence.

## Ideal State Criteria

- [outcome] `adapters/chatgpt/ai-workflow/README.md` presents ChatGPT Projects as the recommended long-running GXP surface, retains Custom GPTs as an optional reusable persona, and directs repository changes to Codex.
- [outcome] ChatGPT model-routing guidance contains no default recommendations for `o3`, `o4-mini`, `GPT-4o`, or `GPT-4o mini`; it routes by task profile and distinguishes ChatGPT from Codex.
- [outcome] A new `adapters/codex/` directory contains a README, a Codex handoff guide, an `AGENTS.md` addendum, a test prompt, and a sync check that exits 0 in this repository.
- [outcome] The Codex guidance covers repository context via `AGENTS.md`, planning, verification, review, and safe use of parallel delegation.
- [outcome] Root and adapter indexes list the Codex adapter and accurately retain existing adapters.
- [guardrail] Core methodology files and existing non-ChatGPT adapters are not edited; the required GXP task brief and rating are the only `core/` task-record changes, and the ChatGPT generated workflow is updated only through its delta and generator.
- [guardrail] The change contains no secrets, project-specific local context, or untracked evaluation artifacts.

**Anti-gaming (non-binding review question):** Does the implementation give an operator a usable surface-selection and handoff workflow, rather than merely renaming models? Yes: the criteria require ChatGPT-to-Codex boundary guidance and a testable Codex adapter.

## Out of scope

- Changes to GXP core methodology, routing policy, or any existing non-ChatGPT adapter.
- Publishing a release, creating a plugin package, or modifying the Cowork plugin.
- Automated live checks against third-party product interfaces.

## Verification plan

1. Search affected documentation for the retired default model names and verify expected current surface terms.
2. Run the Codex adapter sync check and its negative required-file check.
3. Run `python scripts/generate-adapter-workflows.py --check`.
4. Run `bash scripts/verify.sh`.
5. Inspect the final diff to confirm the scope guardrails.

## Self-evaluation gate

- [x] **Completeness** — covers the agreed ChatGPT modernization and separate Codex adapter.
- [x] **Ambiguity** — every binding criterion has a concrete file or command check.
- [x] **Scope trap** — plugin packaging, releases, and core changes are explicitly out of scope.
- [x] **Verification** — each binding criterion has a deterministic search, sync, generation, or repository verification check.
- [x] **Approval gates** — public documentation change approved by the user's “proceed as recommended” instruction.
- [x] **Criteria quality** — criteria are outcome-focused, binary, and independently checkable.
- [x] **Anti-gaming** — the planned output gives operational guidance and a testable adapter rather than only terminology changes.

## Approval gates

- Public-facing documentation: approved by user on 2026-07-25.

## Dead ends

- None.

## Handoff notes

- What changed: Modernized the ChatGPT Project/Custom GPT guidance and model routing; added a dedicated Codex adapter, handoff format, AGENTS.md addendum, test prompt, and sync check; listed Codex in repository indexes and parity verification.
- What was verified (and how): Codex sync check passes and fails when a required file is temporarily absent; generator check passes; focused static scope/content checks pass; `git diff --check` passes.
- Explicitly not done / parked / follow-ups: No core methodology, non-ChatGPT adapter, plugin, or release changes. Repository-wide `verify.sh` remains blocked by pre-existing stale sync markers in Claude, Grok, and Perplexity.
- Approval gates hit and outcomes: public documentation update approved.
- New `failures/` entries or rules: None; the unrelated stale-marker state is already visible through existing sync checks.
- Rating entry reference: `core/ratings.jsonl` entry for `modernize-chatgpt-and-add-codex-adapter`.
