# Local context is never committed

This repo holds **public methodology** only — workflow, templates, adapters, rules.
A project's **filled instance** stays local-only and out of version control: private
configuration, credentials, proprietary data, internal knowledge bases, and any
machine-generated run artifacts.

Never commit (and never *suggest* committing):

- `.ai/PROGRAM.md` — the filled, project-specific instance of `core/PROGRAM.template.md`
- `knowledge/` — private domain knowledge, data, and reference material
- `~/.gxp/rule-packs/` — filled domain rule packs (templates in `core/templates/rule-packs/`)
- `adapters/local/` — private or project-specific skills and personas
- `local/` — any other local-only working files
- `core/tasks/generated/` and run-log dirs — machine-generated artifacts (already ignored)

The principle is broader than the list: if content describes **this specific project or
deployment** rather than **the methodology**, it is local-only — regardless of path. When
in doubt, keep it out of git and ask the operator.

Agents operating in this repo must not stage, commit, or propose committing the above,
and must not echo private values (credentials, proprietary data, internal metrics) into
tracked files — `README`, `ratings.jsonl` notes, or commit messages.
