# GXP addendum for `AGENTS.md`

Add this compact guidance to a repository's `AGENTS.md`, adapting paths and commands to
the project. Keep the repository's own commands and constraints authoritative.

```md
## GXP workflow

For non-trivial changes, follow `.ai/workflow.md` (or this repository's GXP workflow):
audit applicable context, write a brief with 4-8 binary Ideal State Criteria, pass the
self-evaluation gate, make the smallest viable change, and verify each binding criterion.

Use Plan mode when the task is complex or unclear. Before handoff, report the files
changed, exact commands run and their results, criterion-by-criterion evidence, and any
remaining risks. Do not claim a check passed without its output.

For independent read-heavy work, parallel subagents may be used when explicitly requested
or called for by repository guidance. Do not run concurrent writers in the same working
tree; isolate them or keep implementation single-threaded.
```

Do not add broad personal preferences, secrets, or copied local project context to a
tracked `AGENTS.md`.
