# Task brief

**Date:** 2026-10-01
**Task slug:** zenith-reviewer-and-plan-checks
**Workflow:** full — changes `core/workflow.md` (methodology); multi-constraint even though the edit is docs-only.

## Goal

GXP's protocol docs state two borrowed checks — an independent final reviewer and acyclic exact-ownership plans — in the existing bounded style, with no new runtime.

## Context

- Related files: `core/workflow.md` (canonical), generated `adapters/{claude,chatgpt,grok,perplexity}/ai-workflow/instructions/workflow.md`, `core/failures/README.md`, `core/templates/failure-capture.md`, `core/ratings.jsonl` (`failure_ref`).
- Related PRs / tickets: operator ask; do not touch parked draft PR #24 or `experiments/jev-*`.
- Relevant rules: `core/rules/01-no-secrets-in-git.md` (no credentials in the attribution); `core/rules/02-local-context-never-committed.md` (no trial trees).
- Relevant failures: `core/failures/webfetch-summarizer-invents-plausible-details.md` — zenith sources were read via the GitHub API, not a page summary. `core/failures/jsonl-append-via-shell-heredoc-corrupts-escapes.md` — any ratings append goes through Python, not a shell heredoc.
- Background: Intelligent-Internet/zenith (Apache-2.0) terminal-reviewer and validator prompts, plus `task_validation.py` `check_acyclic` / `check_coverage`. Paraphrase only.
- Ontology: none.

**Strategy/Model:** Cursor cloud agent (Grok) — prose edit plus the existing generator; no new engine.

**Scaffolding tier:** standard — methodology text with a named verify command; unknown-model default, and the change does not need denser step scaffolding.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [cursor]
- **forbidden_engines:** live Jev/MCP services
- **exec_mode:** auto
- **output_contract:** protocol sentences in `core/workflow.md`, regenerated chat workflows if `--check` requires them, PR against `main` with the ISC checklist marked.

## Ideal State Criteria

- [outcome] `core/workflow.md` Phase 5 names an independent final reviewer that checks the finished result against the original request and the Ideal State Criteria, requires that reviewer to gather its own evidence, and states that implementer notes, reports, and mission artifacts are leads, not proof.
- [outcome] `core/workflow.md` states that a failed or unverifiable binding criterion is recorded with `templates/failure-capture.md` under `failures/` and a `ratings.jsonl` `failure_ref`, and that this uses those existing conventions (no second ledger).
- [outcome] `core/workflow.md` Standing checks extend **One node** so a plan that is a graph of nodes must be acyclic and every Ideal State Criterion has exactly one owning node (uncovered and double-owned both fail the plan).
- [outcome] `core/workflow.md` contains one short attribution line that names Intelligent-Internet/zenith, Apache-2.0, and that the wording is paraphrased from the terminal-reviewer prompt, the validator prompt, and `check_acyclic` / `check_coverage`.
- [guardrail] The diff against `main` contains no path under `experiments/jev-` and does not add a runtime, MCP server, persona, or dependency manifest change.
- [outcome] `bash scripts/verify.sh` from the repo root exits 0.
- [guardrail] `adapters/grok-bot/SKILL.md`, `adapters/cursor/ai-workflow/rule.mdc`, and Cowork skill files stay unmodified unless `scripts/verify.sh` fails without that edit. Generated `instructions/workflow.md` files may change only by running `scripts/generate-adapter-workflows.py`.
- [hypothesis] Regeneration is enough for claude, chatgpt, grok, and perplexity workflow parity; hand-managed adapters do not need a parallel copy of the new sentences.

**Anti-gaming:** The objective is a thin protocol sentence operators can follow, not a Zenith port. Copying prompt bodies or adding a validator script would meet a superficial "inspired by zenith" reading and miss the brief.

## Ontology / Domain Model (optional)

None.

## Out of scope

- Runtime, MCP server, persona, or dependency that executes the reviewer or the graph checks.
- Edits under `experiments/jev-*` and any change to parked draft PR #24.
- Calling a live Jev or MCP service.
- Hand-editing generated workflow bodies, or updating grok-bot / Cursor / Cowork copies unless a parity check fails.
- Wholesale paste of zenith prompt text.

## Verification plan

1. Deterministic: `bash scripts/verify.sh` (includes `generate-adapter-workflows.py --check` and adapter `check-core` scripts).
2. Criterion walk with `rg` on `core/workflow.md` for reviewer, leads/proof, failures/`failure_ref`, acyclic, exactly one owning node, and the attribution line.
3. `git diff --name-only origin/main` excludes `experiments/jev-` and dependency manifests; `git diff --name-only` on grok-bot, cursor `rule.mdc`, and cowork skills is empty unless verify forced an edit.

## Self-evaluation gate

- [x] **Completeness** — both borrowed checks, attribution, failure convention, verify, and the jev/runtime guardrails are binding.
- [x] **Ambiguity** — each binding line is true or false from a file read or a command exit code.
- [x] **Scope trap** — no adapter rewrite, no changelog, no runtime.
- [x] **Verification** — verify.sh plus greps named above.
- [x] **Approval gates** — none before the PR; the PR is the operator-facing review.
- [x] **Criteria quality** — outcomes and guardrails; the generator mechanism is a hypothesis, not a binding line.
- [x] **Anti-gaming** — recorded above.
- [x] **Ontology (if used)** — not used.

## Approval gates

None. Public methodology text; no production system.

## Dead ends

-

## Handoff notes

- What changed: `core/workflow.md` Standing checks (**One node** graph: acyclic, exactly one owning node per Ideal State Criterion) and Phase 5 **Independent final reviewer** (fresh evidence; worker reports are leads, not proof; failed or unverifiable binding criteria use `failures/` + `failure_ref`). One attribution blockquote names Intelligent-Internet/zenith (Apache-2.0). Chat workflows regenerated for claude, chatgpt, grok, and perplexity.
- What was verified (and how): `bash scripts/verify.sh` exit 0 (adapter `check-core` scripts, gxp-refine selftest, `generate-adapter-workflows.py --check`). Criterion greps on `core/workflow.md`. `git diff --name-only origin/main` is the brief, `core/workflow.md`, and the four generated workflows — no `experiments/jev-*`, no dependency manifest, no grok-bot / cursor `rule.mdc` / cowork skill edits.
- Explicitly not done / parked / follow-ups: no runtime. Grok Bot `SKILL.md` still summarizes the old three standing checks; parity did not require an edit. Cursor `rule.mdc` is unchanged for the same reason. The Cursor paste block inside `core/workflow.md` carries the new sentences; generated adapters skip the Cursor usage section.
- Approval gates hit and outcomes: none.
- New `failures/` entries or rules: none (no failed criterion).
- Rating entry reference: `core/ratings.jsonl` task `zenith-reviewer-and-plan-checks`.
