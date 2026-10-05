# Grok Bot → Cursor handoff

Use this packet after a Grok Bot **widget** approval. Paste it into a **Cursor cloud agent** or a local **`cursor-agent`** session on an existing checkout.

Grok Bot must not clone the repo, edit files, or run git. The Cursor agent implements, verifies, and reports evidence. Mechanical git stays on the local CLI.

```md
## Goal

<one observable outcome>

## Context

- Repository / branch: <existing checkout; do not clone from Grok Bot>
- Relevant files: <paths>
- Applicable `AGENTS.md`, `.ai/PROGRAM.md` or `core/workflow.md`, rules, failures: <paths>
- Scaffolding tier: standard | frontier | constrained

## Constraints

- Follow GXP in `core/workflow.md` (or `.ai/workflow.md` in a target repo).
- Smallest viable change. Do not expand scope.
- For code: standing checks — change site greppable from each ISC; one ISC maps to one node/module; named verify command in this packet.
- Do not edit `adapters/grok/` or `adapters/grok-build/` unless this brief names them.
- Approval gates already passed in Grok Bot widgets; pause again only for new destructive/public steps.
- Load filled `.ai/` or `~/.gxp/` artifacts only; skip unfilled `core/templates/`.
- Name an inverse for any plugin/MCP/skill/handoff or treat as irreversible.
- Phase 5 records pass/fail per binding ISC before continuing.

## Ideal State Criteria

- [outcome] <binary outcome>
- [guardrail] <binary scope or safety guardrail>

## Verification plan

The **agent** runs these — do not tell the operator to run `check-core.sh`.

1. <exact deterministic command, e.g. `bash scripts/verify.sh`>
2. <criterion-edge check smoke would miss>
3. <diff review>

## Verification evidence (required)

Paste raw stdout/stderr and the exit code for every named verify command. A report that says "tests pass" without that pasted output is incomplete for Phase 5. Prose summaries are leads, not proof.

For each command, include:

- Command: `<exact command>`
- Exit code: `<N>`
- Raw stdout/stderr: paste the terminal transcript under the command

## Handoff request

Read the repository guidance and this brief. Implement the smallest change that meets the binding criteria. Run the verification plan yourself. Return changed files, each named verify command with its exit code and pasted raw stdout/stderr, criterion-by-criterion evidence, and remaining risks. "tests pass" without pasted output is incomplete for Phase 5. Leave mechanical git (branch / commit / push) to the local CLI unless the operator already authorized those commands in this Cursor session.
```

## Verification evidence (required)

The Cursor agent must paste raw stdout/stderr and the exit code for every named verify command in the packet. Grok Bot records whether that paste arrived. A sentence such as "tests pass" without the pasted output is incomplete for Phase 5.

## Surfaces

| Target | How |
|--------|-----|
| Cursor cloud agent | Paste the packet into the cloud agent prompt; point at the existing repo. |
| Local `cursor-agent` | Run in the existing working tree. Do not `git clone` first from Grok Bot. |

## Isolation

Do not spawn Grok Build personas (`gxp-researcher`, `gxp-architect`, `gxp-verifier`). Cursor follows its own GXP rule; Bot only supplied the brief and widget approval.
