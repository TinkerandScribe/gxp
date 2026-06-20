# Security Policy

GXP is a documentation and methodology repository. It ships Markdown, templates, and small
install/verify scripts (`scripts/`, adapter `sync/` helpers) — there is no backend, network
service, or data handling.

## Reporting an issue

If you find a problem with the scripts or repository content — including anything with a
potential security impact — please report it through GitHub:

- **Private report:** open a draft advisory under the repository's **Security → Report a
  vulnerability** tab, or contact the maintainer at https://github.com/TinkerandScribe.
- **Non-sensitive problems:** open a regular issue.

Please do not include secrets or private data in a report.

## Scope

- **In scope:** the installer scripts, adapter sync scripts, and repository content.
- **Out of scope:** the third-party AI tools the adapters target (Claude, Cursor, Grok,
  Perplexity). Report issues with those to their respective vendors.
