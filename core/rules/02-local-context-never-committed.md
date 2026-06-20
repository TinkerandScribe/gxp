# Local context is never committed

This repo holds **public methodology** only — workflow, templates, adapters, rules.
The **filled shop instance** stays local-only and out of version control: machine
specs, material and cost data, margins, customer patterns, safety rules, brand voice,
and machine-generated run artifacts.

Never commit (and never *suggest* committing):

- `.ai/PROGRAM.md` — the filled shop instance of `core/PROGRAM.template.md`
- `knowledge/` — machine specs, cost sheets, material data
- `~/.gxp/rule-packs/` — filled safety and materials rule packs (templates in `core/templates/rule-packs/`)
- `adapters/local/` — private or shop-specific skills and personas
- `local/` — any other local-only working files
- `core/tasks/generated/` and run-log dirs — machine-generated artifacts (already ignored)

The principle is broader than the list: if content describes **this shop** rather than
**the methodology**, it is local-only — regardless of path. When in doubt, keep it out
of git and ask the operator.

Agents operating in this repo must not stage, commit, or propose committing the above,
and must not echo shop-specific values (costs, margins, customer data) into tracked
files — `CLAUDE.md`, `README`, `ratings.jsonl` notes, or commit messages.