# Adapters

This directory contains AI-specific implementations and optimizations of the core methodology.

## Philosophy

The core methodology lives in `../core/`. Adapters exist to make that methodology **excellent** for a particular AI's strengths and interface, rather than forcing a lowest-common-denominator experience.

## Rules for Adapters

- Significant changes to the *process* or *principles* must be made in `core/` first.
- Adapters may duplicate content from core when it enables meaningfully better results for that AI.
- Every adapter should have a clear way to stay in sync with core (strong instructions + convenient tooling).
- The verification system treats unjustified drift as a failure.

## Current Adapters

- `cursor/` — Cursor rule, Phase -1 capability gate, `install-cursor-rule.ps1`, `security.mdc.template`
- `grok/` — Installable skill (`gxp`); sync via `check-core.ps1` / `check-core.sh`
- `claude/` — Instructions and context-loading patterns (targets the claude.ai web app)
- `perplexity/` — Research-phase workflow and collections strategy
- `cowork/` — Cowork plugin (`gxp.plugin`): four skills — workflow / brief / rate / failure-capture. Built from `core/` (option (a): references generated at build time, not checked in). Run `bash adapters/cowork/build.sh` to produce `dist/gxp.plugin`, then install in Cowork via Settings → Capabilities.

## Adding a New Adapter

1. Create a new directory under `adapters/`.
2. Reference or copy from `core/` as your starting point.
3. Add whatever optimizations make sense for the target AI.
4. Add appropriate sync/check tooling so the adapter can stay aligned with core over time.
5. Update `scripts/verify.sh` step 5 to cover the new adapter.

## Verify adapter parity

From repo root:

```bash
bash scripts/verify.sh
```

**Negative test:** temporarily rename a required file (e.g.
`adapters/perplexity/ai-workflow/TEST_PROMPT.md`) and re-run — the script must exit
non-zero with a named adapter error. Restore the file after.