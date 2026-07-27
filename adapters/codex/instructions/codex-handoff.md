# ChatGPT-to-Codex Handoff

Use this format when ChatGPT planning or research is ready for repository execution.

```md
## Goal

<one observable outcome>

## Context

- Repository / branch: <location and relevant state>
- Relevant files and source links: <paths or URLs>
- Applicable `AGENTS.md`, `.ai/PROGRAM.md`, rules, and known failures: <paths>

## Constraints

- <scope, safety, compatibility, or approval constraint>

## Ideal State Criteria

- [outcome] <binary outcome>
- [guardrail] <binary scope or safety guardrail>

## Verification plan

1. <exact deterministic command>
2. <behavioral or edge check>
3. <diff review or `/review` target>

## Handoff request

Read the applicable repository guidance and brief. Use Plan mode if the task is ambiguous.
Make the smallest viable change. Run the verification plan, inspect the diff or use
`/review`, and return changed files, exact commands and results, criterion-by-criterion
evidence, and remaining risks. Stop for approval at any named gate.
```

## Delegation rule

Use subagents only for independent work such as repository exploration, log analysis, or
test-gap review. Give each agent a bounded question and ask for a concise evidence-backed
summary. Avoid concurrent edits in one working tree; use separate worktrees when writes
must be isolated.
