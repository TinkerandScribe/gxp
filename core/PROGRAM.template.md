# PROGRAM

This file is the project-specific customization point for the `.ai/` workflow.
Edit it to describe how *this* repository should be worked on. Everything else
in `.ai/` is generic.

## Project summary

One paragraph: what is this repo, who uses it, what does success look like.

## Stack and tooling

- Languages:
- Package manager:
- Test runner:
- Lint / format:
- CI:

## Repository map

Brief tour of the top-level directories and what lives in each.

## Operating modes

Full vs lightweight workflow is defined in `.ai/workflow.md`. Default to
**full** for anything that changes behaviour or touches multiple files; use
**lightweight** only for trivial, single-file, easily reversible edits.

## Domain context (optional — domain-specific; replace or delete)

If this project has real-world assets, environments, or constraints the agent should
assume, list them here (names only — no secrets in git). Examples depending on domain:

- _(services / hardware / environments this project depends on)_
- _(physical assets, devices, or equipment, if any)_

## Materials / inputs (optional)

Common inputs and constraints (placeholder bullets — fill real values locally only).

- _(allowed inputs, formats, size or range limits)_
- _(anything the agent must not assume or must validate)_

## Verification commands

Run these before declaring work done. Replace placeholders with this project's real commands.

| Check | Command | Notes |
|-------|---------|-------|
| Lint | _(e.g. `npm run lint`)_ | |
| Unit tests | _(e.g. `npm test`)_ | |
| Build | _(optional)_ | |
| Typecheck | _(optional)_ | |

```
# example block (delete or replace)
make lint
make test
```

## Ratings

After each task, append **one JSON object per line** to `.ai/ratings.jsonl`.
Use the field names documented in the schema line at the top of that file
(`ts`, `task`, `brief`, `criteria_met`, `criteria_total`, `rating`, optional
`mode`, `notes`, `failure_ref`). Do not parse or rate the `_schema` line itself.

## Security and secrets

Document project-specific secret handling here and/or via a repo-local Cursor
rule (e.g. copy `security.mdc` from the gxp Cursor adapter template).
Never commit live credentials; use `.env.example` patterns only.

## Coding conventions

Anything not obvious from the code itself. Naming, layering, what to avoid.
Cross-link to `.ai/rules/` entries for durable rules.

## Domains and glossary

Project-specific terms, acronyms, and concepts.

## Out of scope

Things explicitly not handled here, or done elsewhere.

## Open questions

Known unknowns. Update as they resolve.
