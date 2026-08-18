# GXP — Guided eXecution Protocol

**A verification-first agent harness with binary Ideal State Criteria, anti-scope-creep rules, and scaffolding tiers.**

Designed so a strong model + this process reliably finishes multi-step work instead of exploring.

> **Naming note:** "GXP" here stands for **Guided eXecution Protocol**, an AI-coding
> workflow discipline. It is unrelated to — and makes no claim of compliance with —
> regulated-industry "GxP" (Good Manufacturing / Laboratory / Clinical Practice:
> GMP/GLP/GCP) frameworks used in pharmaceutical, biotech, and medical-device
> validation. Do not use this project as a substitute for validated GxP compliance
> tooling.

## Why this exists

Models keep getting better. The bottleneck is no longer raw capability — it is reliable *process* around the model. Without structure, even frontier agents drift, expand scope, declare victory on weak smoke tests, and repeat the same failure modes.

GXP is a lightweight, tool-agnostic harness that forces the opposite behavior:

- Write **4–8 binary, checkable criteria** for what "done" means *before* any non-trivial work
- Pass a self-evaluation gate
- Make the smallest viable change
- **Stop after two failed attempts** on the same approach
- Verify deterministically before trusting anything subjective
- Rate the outcome honestly and capture repeatable failures so they do not recur

It is deliberately **bounded** (L3/L4, not full autonomy): the agent works inside a written brief, does not expand scope on its own, and pauses at approval gates. The same discipline works with Claude, ChatGPT, Codex, Cursor, Grok (chat + Build + Bot), Perplexity, or a local model.

## The loop (Phases 0–8)

| Phase | Name | What happens |
|------:|------|--------------|
| 0 | **Repo audit** | Read the project's rules, known failures, and verification commands. |
| 0.5 | **Strategy & model** | Pick the least-capable engine that clears the criteria with margin. |
| 1 | **Task brief** | Goal, context, **4–8 binary Ideal State Criteria**, out-of-scope, verification plan. |
| 2 | **Self-eval gate** | Completeness, ambiguity, scope traps, verification, approval gates. |
| 3 | **Implementation** | Smallest viable change, scoped to the brief. |
| 4 | **Anti-loop** | Same approach fails twice → stop, document the dead end, change strategy. |
| 5 | **Verify** | Deterministic (test/lint/build) → optional ontology validation → behavioral → subjective. |
| 6 | **Rate** | One honest JSON line in `ratings.jsonl` (a real low rating beats a generous one). |
| 7 | **Failure capture** | Repeatable failure → write it down so it doesn't recur. |
| 8 | **Handoff** | What changed, what was verified, what's parked. |

The full process lives in **[`core/workflow.md`](core/workflow.md)**. If you can't write 4 strong binary criteria for a task, it isn't understood yet — clarify before coding.

**Full vs lightweight:** run all phases for anything that changes behavior, touches multiple files, or could regress. Use the lightweight variant (phases 1, 2, 3, 5) only for trivial, single-file, easily reversible edits.

Scaffolding intensity is adjustable via tiers (`frontier` / `standard` / `constrained`) so capable models are not over-prompted and weaker models get denser guardrails — without ever relaxing the core invariants. See [`core/docs/capability-scaffolding.md`](core/docs/capability-scaffolding.md).

## Install into your repo

Copies `core/` into your project as a portable `.ai/` layout (preserves an existing `.ai/PROGRAM.md` and `.ai/ratings.jsonl`).

**What lands under `.ai/`:** `PROGRAM.md`, `workflow.md`, `routing.md`, `ratings.jsonl`; top-level files from `rules/`, `failures/`, `wiki/`, `evals/`; empty `evals/{golden,regressions,canaries}/`; recursive `templates/` (including nested `ontology/`, `knowledge/`, `rule-packs/`); recursive `docs/` from `core/docs/`. `--dry-run` / `-DryRun` previews without creating directories or files.

```bash
# Mac / Linux / Git-Bash — preview first, then install (add --force only to refresh templates)
bash scripts/install-ai-from-core.sh /path/to/your/repo --dry-run
bash scripts/install-ai-from-core.sh /path/to/your/repo --include-cursor-rule
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -TargetRepo C:\path\to\your\repo -DryRun
powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -TargetRepo C:\path\to\your\repo -IncludeCursorRule
```

Then fill in `.ai/PROGRAM.md` with your project's verification commands.

### Refresh GXP across many host repos

Scan a folder of projects (default root: `$HOME/Claude` or `$env:USERPROFILE\Claude` when that directory exists; otherwise pass `--roots` / `-Roots`), optionally pull, re-apply the scaffold, commit, and push.

**Safe defaults:** report-only dry-run; only repos that already have `.ai/workflow.md`; ff-only pull; never force-push. Writing and publishing require explicit flags.

```powershell
# Report only (default; uses $env:USERPROFILE\Claude when present)
powershell -ExecutionPolicy Bypass -File scripts/sync-gxp-hosts.ps1

# Explicit roots
powershell -ExecutionPolicy Bypass -File scripts/sync-gxp-hosts.ps1 -Roots "$env:USERPROFILE\Claude"

# Apply updates to existing .ai trees
powershell -ExecutionPolicy Bypass -File scripts/sync-gxp-hosts.ps1 -Apply

# Apply + commit + push
powershell -ExecutionPolicy Bypass -File scripts/sync-gxp-hosts.ps1 -Apply -Commit -Push
```

```bash
bash scripts/sync-gxp-hosts.sh
bash scripts/sync-gxp-hosts.sh --apply
bash scripts/sync-gxp-hosts.sh --apply --commit --push
# Custom roots:
bash scripts/sync-gxp-hosts.sh --roots "$HOME/Claude" --apply
```

Use `--bootstrap` / `-Bootstrap` only if you want GXP installed into git repos that do not yet have `.ai/workflow.md`. The GXP monorepo itself is always skipped.

## Using it

GXP is a discipline you put your AI agent through — there's no binary to run. Two ways to drive it:

**With an adapter (automatic).** Install the adapter for your tool (see below) and it loads the workflow for you: in Cursor the rule applies automatically; in Grok chat, invoke the `gxp` skill; in **Grok Build**, install the dedicated `gxp-build` skill / personas; in **Grok Bot**, invoke `gxp-bot` (brief/criteria/status only — Cursor implements); in ChatGPT, use a Project for planning and hand repository work to Codex; in Claude or the Cowork plugin, just say *"use gxp on …"*.

**With any agent (manual).** Point the agent at `.ai/workflow.md` and tell it to follow GXP. A prompt that works in any chat-based coding agent:

> Follow the GXP workflow in `.ai/workflow.md`. Before coding, write a task brief with 4–8 binary Ideal State Criteria and pass the self-evaluation gate. Make the smallest change, stop after two failed attempts on the same approach, verify deterministically first, then append one honest line to `.ai/ratings.jsonl`.

As you work, GXP reads and writes a few well-known locations in your repo:

| Artifact | Path | Purpose |
|---|---|---|
| Project context | `.ai/PROGRAM.md` | your verification commands + conventions (read in Phase 0) |
| Task briefs | `.ai/tasks/<slug>.md` | one per task — criteria + verification plan |
| Ratings ledger | `.ai/ratings.jsonl` | one honest JSON line per run (Phase 6) |
| Failure notes | `.ai/failures/<slug>.md` | repeatable traps, so they don't recur (Phase 7) |

Start small: run one real task through the full loop — write the brief first, and rate it honestly.

## Use it as a Claude skill (download)

Want a one-click install instead of copying files? Download the packaged skill and add it the normal way:

**⬇️ [`gxp-skill.zip`](https://github.com/TinkerandScribe/gxp/releases/latest/download/gxp-skill.zip)** — from the [latest release](https://github.com/TinkerandScribe/gxp/releases/latest). Self-contained (the full workflow + bundled templates); no repo checkout needed.

- **claude.ai** → Settings → Capabilities → **Skills** → **Upload**, then select the zip. *(Requires a plan where custom Skills are enabled.)*
- **Claude Code:**
  ```bash
  cd ~/.claude/skills
  curl -L -o gxp.zip https://github.com/TinkerandScribe/gxp/releases/latest/download/gxp-skill.zip
  unzip gxp.zip && rm gxp.zip        # creates ~/.claude/skills/gxp/
  ```
  Restart Claude Code, then invoke with `/gxp` (or just say "use gxp").

## Adapters

Each adapter re-expresses GXP for a specific tool's interface and strengths. All derive from `core/`; see [`adapters/README.md`](adapters/README.md).

- **`cursor/`** — Cursor rule + capability gate + installer.
- **`grok/`** — installable Grok **chat** skill (`gxp`) with sync checks.
- **`grok-build/`** — dedicated **Grok Build** adapter: Heavy multi-persona front-half, install scripts, optional `gxp-build` skill (never overwrites the chat skill), lightweight `sync/check-core`.
- **`grok-bot/`** — dedicated **Grok Bot** adapter: thin chat (brief/criteria/status), widget gates, Cursor cloud agent or `cursor-agent` implementation, local-CLI git. Does not stretch `grok/` or `grok-build/`.
- **`claude/`** — custom instructions and context-loading patterns for Claude.
- **`chatgpt/`** — ChatGPT Project and Custom GPT planning, context-loading, and Codex handoffs.
- **`codex/`** — repo-native execution guidance for Codex: `AGENTS.md`, planning, verification, review, and delegation.
- **`perplexity/`** — research-phase workflow and collections strategy (trust-boundary handoffs).
- **`cowork/`** — a Cowork plugin (`gxp`) packaging four skills, built from `core/`.

### Optional ontology guardrails

Projects may declare a formal domain model and bind Ideal State Criteria to it. Phase 5 then runs optional ontology validation (after deterministic checks, before behavioral/subjective). See [`core/docs/ontology-guardrails.md`](core/docs/ontology-guardrails.md) and [`core/templates/ontology/`](core/templates/ontology/). Opt-in only — projects without an ontology skip the step.

## Repository layout

```
core/        the methodology — workflow, routing, rules, failures, templates, docs
adapters/    per-tool integrations (cursor, grok, grok-build, grok-bot, claude, chatgpt, codex, perplexity, cowork)
scripts/     installer (.ps1 + .sh), workflow generator, and adapter-parity check (verify.sh)
```

## Bounded self-refinement (`gxp-refine`)

Operator-invoked only (mutation budget = 1, dual approval gates, no auto-merge).
How-to: [`core/docs/gxp-refine.md`](core/docs/gxp-refine.md). Design:
[`core/tasks/gxp-refine-design.md`](core/tasks/gxp-refine-design.md).
Invoke paste surfaces (operator-only):
[`Cursor`](adapters/cursor/ai-workflow/GXP_REFINE.md) ·
[`Claude`](adapters/claude/ai-workflow/GXP_REFINE.md) ·
[`Grok`](adapters/grok/ai-workflow/GXP_REFINE.md).

## Verify the repo

```bash
bash scripts/verify.sh   # required files + adapter sync checks + generate-adapter-workflows.py --check
```

## Releases

See [`CHANGELOG.md`](CHANGELOG.md). Tagged release: **v1.3.1**. Main also carries post-tag work (criteria taxonomy / anti-fixation, Grok Build adapter, Codex adapter, ChatGPT↔Codex handoffs, optional ontology guardrails) — see **Unreleased** in the changelog.

Planned work lives in [`ROADMAP.md`](ROADMAP.md) (Parts A–C mostly complete; Part B M6 evidence still open; Part D tracks recent adapter/methodology ships).

## License

[MIT](LICENSE) © 2026 Tinker & Scribe Workshop.
