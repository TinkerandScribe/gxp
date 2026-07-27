# Codex Adapter

This adapter applies GXP to **repository-native Codex work**: read a checkout, make a
focused change, run commands, review the diff, and return evidence.

## When to use Codex

Use Codex when a task needs access to a local repository, commands, tests, git state, or
code review. Use the ChatGPT adapter for planning, research, and reusable handoffs, then
send the approved brief to Codex for implementation.

## Setup

1. Add the relevant guidance from [`AGENTS.addendum.md`](AGENTS.addendum.md) to the
   repository's `AGENTS.md`; keep it concise and project-specific.
2. Keep GXP's portable workflow in `.ai/` using the repository installer, or reference
   `core/workflow.md` when working in this source repository.
3. Use [`instructions/codex-handoff.md`](instructions/codex-handoff.md) for every
   ChatGPT-to-Codex handoff and [`TEST_PROMPT.md`](TEST_PROMPT.md) to exercise the flow.

### Optional local Codex app skill

A local Codex app skill (for example `gxp-codex` under `$CODEX_HOME/skills/`) is
**optional** and **out-of-tree** relative to this published adapter. Operators may install
one on their machine for convenience; clones of this repo do not require it. Do not commit
machine-local skill paths or home-directory install state.

## Operating model

- Use Plan mode for complex or ambiguous work before editing.
- Read applicable `AGENTS.md` files and the GXP task brief before implementation.
- Make the smallest viable change, run the named checks, then inspect the diff or use
  `/review` before handoff.
- Delegate only independent, read-heavy work such as exploration, test analysis, or log
  triage. Keep concurrent writers isolated by worktree or avoid them.

## Relationship to core

`core/` remains the methodology source of truth. This adapter adds Codex-specific delivery
guidance; it does not change GXP phases, criteria, verification, ratings, or failure
capture. See [`../../core/README.md`](../../core/README.md) and
[`../chatgpt/ai-workflow/README.md`](../chatgpt/ai-workflow/README.md).

## Verify

```bash
bash adapters/codex/sync/check-core.sh
bash scripts/verify.sh
```
