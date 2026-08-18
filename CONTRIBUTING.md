# Contributing to GXP

Thanks for your interest. GXP is a methodology, so contributions are mostly **prose,
templates, and small tooling** — clarity matters more than cleverness.

## The one rule that shapes everything

**`core/` is the single source of truth.** The adapters (`adapters/cursor`, `grok`,
`grok-build`, `grok-bot`, `claude`, `chatgpt`, `codex`, `perplexity`, `cowork`) re-express the same
methodology for a specific tool.

- A change to the **process or principles** goes into `core/` first.
- For **claude / chatgpt / grok / perplexity**, published
  `instructions/workflow.md` files are **generated** from `core/workflow.md` plus
  `adapters/<tool>/ai-workflow/deltas/workflow.delta.md`. Edit **core and the delta**,
  then run:
  `python scripts/generate-adapter-workflows.py`
  Do **not** hand-edit the generated workflow bodies (CI runs `--check`). After core
  methodology changes, always regenerate before claiming adapters are current.
- **Cursor** (`rule.mdc`), **Cowork** (build-time core copy), **Codex** (repo-native
  `AGENTS.md` / handoff guidance), **Grok Build** (personas + optional skill; no
  generated workflow body), and **Grok Bot** (thin chat + Cursor handoff; no generated
  workflow body) stay on their existing models.
- Each adapter has a `sync/check-core.*` script — run it after changes. Structural floor
  and live sync markers must keep working.

## Use the methodology on itself

This repo is dogfooded. For any non-trivial change, follow the loop in
[`core/workflow.md`](core/workflow.md): write a short brief with **4–8 binary criteria**,
make the smallest change that satisfies them, verify, and note what you checked. Small
docs typos can skip the ceremony.

## Good contributions

- Clarifying or tightening the methodology docs (concise > exhaustive).
- A new adapter for a tool not yet covered — copy an existing adapter's shape, add
  `sync/check-core.*`, and list it in [`adapters/README.md`](adapters/README.md).
- Fixing broken links, examples, or installer behavior.
- A captured failure pattern (see `core/templates/failure-capture.md`) that others would
  plausibly hit too.

## Before you open a PR

- `bash scripts/verify.sh` passes (adapters still ship their required files;
  when present, `scripts/eval-gxp-refine-selftest.sh` runs as part of verify).
- No secrets and no local/project-specific context — see
  [`core/rules/01-no-secrets-in-git.md`](core/rules/01-no-secrets-in-git.md) and
  [`core/rules/02-local-context-never-committed.md`](core/rules/02-local-context-never-committed.md).
- Keep the diff scoped to one thing; park "while we're here" cleanups.

## License

By contributing you agree your contributions are licensed under the repository's
[MIT License](LICENSE).
