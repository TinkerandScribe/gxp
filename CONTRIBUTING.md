# Contributing to GXP

Thanks for your interest. GXP is a methodology, so contributions are mostly **prose,
templates, and small tooling** — clarity matters more than cleverness.

## The one rule that shapes everything

**`core/` is the single source of truth.** The adapters (`adapters/cursor`, `grok`,
`claude`, `chatgpt`, `perplexity`, `cowork`) re-express the same methodology for a specific tool.

- A change to the **process or principles** goes into `core/` first, then gets ported
  into the adapters that need it.
- An adapter may rephrase or optimize for its tool, but must not quietly diverge from
  core. Each adapter has a `sync/check-core.*` script — run it after changes.

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

- `bash scripts/verify.sh` passes (adapters still ship their required files).
- No secrets and no local/project-specific context — see
  [`core/rules/01-no-secrets-in-git.md`](core/rules/01-no-secrets-in-git.md) and
  [`core/rules/02-local-context-never-committed.md`](core/rules/02-local-context-never-committed.md).
- Keep the diff scoped to one thing; park "while we're here" cleanups.

## License

By contributing you agree your contributions are licensed under the repository's
[MIT License](LICENSE).
