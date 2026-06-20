# Rules

Durable, narrow rules for working in this repository. One rule per file.

Good rules are:

- **Narrow** — they apply to a specific situation, not "write good code".
- **Actionable** — a reader knows what to do or not do.
- **Justified** — they include the reason, so they can be re-evaluated later.

Suggested filename pattern: `NN-short-slug.md` (e.g. `01-no-network-in-tests.md`).

A rule that no longer holds should be deleted, not edited into vagueness.

## When rules conflict

Prefer the stricter constraint, in this order:

1. User request / task brief constraints (including explicit out-of-scope)
2. `.ai/PROGRAM.md` (project-specific commands and non-negotiables)
3. `.ai/rules/` (durable repo rules)
4. `.ai/workflow.md` (process loop)
5. Repo-local Cursor rules in `.cursor/rules/` if present (e.g. security behaviour)
6. General coding best practices
