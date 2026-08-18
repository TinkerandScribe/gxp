# Adapters

This directory contains AI-specific implementations and optimizations of the core methodology.

## Philosophy

The core methodology lives in `../core/`. Adapters exist to make that methodology **excellent** for a particular AI's strengths and interface, rather than forcing a lowest-common-denominator experience.

## Rules for Adapters

- Significant changes to the *process* or *principles* must be made in `core/` first.
- **claude / chatgpt / grok / perplexity:** edit `deltas/workflow.delta.md` (tool-specific)
  and regenerate with `python scripts/generate-adapter-workflows.py`. Do not hand-edit
  generated `instructions/workflow.md` bodies (CI `--check`).
- **cursor / cowork / codex / grok-build / grok-bot:** keep their existing models (`rule.mdc`; build-time core copy; Codex references the canonical workflow through repository guidance; Grok Build personas + optional skill; Grok Bot thin chat + Cursor handoff). No generated `instructions/workflow.md` for those surfaces.
- Every adapter has sync/check tooling; unjustified drift fails `verify.sh`.

## Current Adapters

- `cursor/` — Cursor rule, Phase -1 capability gate, `install-cursor-rule.ps1`, `security.mdc.template`
- `grok/` — Installable skill (`gxp`) for grok.com / chat; also ships example Grok Build personas under `examples/grok-build-strategy/`
- `grok-build/` — **Dedicated Grok Build adapter** (personas, Heavy multi-agent patterns, install scripts, optional `gxp-build` skill, lightweight `sync/check-core`, `examples/heavy-front-half.md`). Independent of the chat skill; installers never write `gxp-ai-workflow`
- `grok-bot/` — **Dedicated Grok Bot adapter** (thin chat: brief/criteria/status only; widget gates not `/plan`; Cursor cloud agent or `cursor-agent` implements; mechanical git on local CLI). Independent of `grok/` and `grok-build/`; never clones or edits repos in the Bot conversation
- `claude/` — Instructions and context-loading patterns (targets the claude.ai web app)
- `chatgpt/` — ChatGPT Project and Custom GPT planning guidance, context loading, and Codex handoffs
- `codex/` — repository-native execution guidance: `AGENTS.md`, planning, verification, review, and delegation (`sync/check-core.sh` presence + markers)
- `perplexity/` — Research-phase workflow and collections strategy (trust-boundary handoffs)
- `cowork/` — Cowork plugin (`gxp.plugin`): four skills — workflow / brief / rate / failure-capture. Built from `core/` (option (a): references generated at build time, not checked in). Run `bash adapters/cowork/build.sh` to produce `dist/gxp.plugin`, then install in Cowork via Settings → Capabilities.

**Core methodology note:** optional ontology validation lives in `core/`, not in a separate
adapter. Regenerated chat workflows pick it up via `scripts/generate-adapter-workflows.py`.

## Adding a New Adapter

1. Create a new directory under `adapters/`.
2. Reference or copy from `core/` as your starting point.
3. Add whatever optimizations make sense for the target AI.
4. Add appropriate sync/check tooling so the adapter can stay aligned with core over time.
5. Add the new adapter’s required files under step 2 of `scripts/verify.sh`, and ensure any `sync/check-core.sh` is picked up by the existing glob (step 3).

## Verify adapter parity

From repo root:

```bash
bash scripts/verify.sh
```

**Negative test:** temporarily rename a required file (e.g.
`adapters/perplexity/ai-workflow/TEST_PROMPT.md`) and re-run — the script must exit
non-zero with a named adapter error. Restore the file after.
