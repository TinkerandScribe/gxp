# Task brief

**Date:** 2026-07-25
**Task slug:** install-gxp-codex-skill
**Workflow:** full

## Goal

Install a reusable `gxp-codex` skill into the local Codex app so future repository tasks can invoke the Codex-specific GXP workflow.

## Context

- Related files: `adapters/codex/`, `core/workflow.md`, and the local Codex skills directory.
- Relevant rules: no secrets or local project context may enter tracked repository files.
- Relevant failure: verification must surface, not swallow, a failed check.

**Strategy/Model:** Codex local skill installation — the user explicitly requested a durable app-level integration.

## Ideal State Criteria

- [outcome] `$CODEX_HOME/skills/gxp-codex/SKILL.md` (or the operator's local Codex skills directory equivalent) exists with valid `name` and `description` frontmatter.
- [outcome] The skill instructs Codex to read applicable `AGENTS.md` and `.ai`/core GXP context before non-trivial repository changes.
- [outcome] The skill requires binary criteria, deterministic-first verification, and an evidence-based handoff.
- [outcome] The installed skill's interface metadata identifies it as a Codex GXP workflow skill.
- [outcome] The skill validator exits 0 for the installed folder.
- [guardrail] Installation changes only the local Codex skills directory; no secrets or local project content is added to this repository.

## Out of scope

- Publishing a plugin or changing global Codex configuration.
- Changing the GXP core methodology or existing adapters.

## Verification plan

1. Run the skill validator against the installed folder.
2. Inspect the installed frontmatter and interface metadata.
3. Confirm the folder appears under the local Codex skills directory.

## Self-evaluation gate

- [x] Completeness — covers creation, installation, and discovery validation.
- [x] Ambiguity — every binding criterion is binary and checkable.
- [x] Scope trap — excludes plugins, config, and core changes.
- [x] Verification — each criterion has a concrete check.
- [x] Approval gates — global local-skill installation explicitly approved by the user.
- [x] Criteria quality — outcomes and guardrail are independently checkable.
- [x] Anti-gaming — validation checks the installed artifact, not only source text.

## Approval gates

- Local app skill installation: approved by user on 2026-07-25.

## Dead ends

- None.

## Handoff notes

- What changed: Installed `gxp-codex` under the local Codex skills directory with validated skill metadata and workflow instructions.
- What was verified (and how): `quick_validate.py` exited 0; the installed `SKILL.md` has no scaffold TODOs; the local skills directory lists `gxp-codex`.
- Explicitly not done / parked / follow-ups: No plugin publication, config changes, or core/adapters changes beyond this task record.
- Approval gates hit and outcomes: local app skill installation approved by the user.
- New `failures/` entries or rules: None.
- Rating entry reference: `core/ratings.jsonl` entry for `install-gxp-codex-skill`.
