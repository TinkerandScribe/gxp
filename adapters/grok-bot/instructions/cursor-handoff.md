# Grok Bot → Cursor handoff

Use this packet after a Grok Bot **widget** approval. Paste it into a **Cursor cloud agent** or a local **`cursor-agent`** session on an existing checkout.

Grok Bot does not clone. A small, low-risk tweak (copy fixes, config values, a few lines in one or two files) may already be on the existing checkout. Bigger or risky work is this packet. Never edit payments, auth/sign-in, DB migrations, secrets, or legal text. Use the dashboard default model (no model pin). Same PR, review, and merge rules either way. The Cursor agent implements, verifies, and returns the fleet rating fields. Grok Bot appends them with one `bin/append.py` command.

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
- Dashboard default model (no model pin). Same PR, review, and merge rules as a bot small tweak.
- Never edit payments, auth/sign-in, DB migrations, secrets, or legal text.
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

## Fleet rating (required on return)

Fill these from the run. Grok Bot appends them with one `bin/append.py` command (`/home/box/shared/gxp/bin/append.py` on the box). Do not append the ledger from Cursor unless this checkout is the fleet store.

- task: <slug>
- brief: <path or one-line summary>
- criteria_met: <integer>
- criteria_total: <integer>
- rating: <integer 1-10>
- mode: full | lightweight
- outcome: success | failure | pivot | refusal
- failed_criteria: <comma-separated ids, or empty>
- notes: <honest note>
- failure: none, or slug + expected + actual + cause + regression check

## Handoff request

Read the repository guidance and this brief. Implement the smallest change that meets the binding criteria. Run the verification plan yourself. Return changed files, each named verify command with its exit code and pasted raw stdout/stderr, criterion-by-criterion evidence, the fleet rating fields above, and remaining risks. "tests pass" without pasted output is incomplete for Phase 5. Leave mechanical git (branch / commit / push) to the local CLI unless the operator already authorized those commands in this Cursor session.
```

## Verification evidence (required)

The Cursor agent must paste raw stdout/stderr and the exit code for every named verify command in the packet, plus the fleet rating fields. Grok Bot records whether that paste arrived, then runs:

```bash
python3 /home/box/shared/gxp/bin/append.py /home/box/shared/gxp \
  --task "<task>" \
  --brief "<brief>" \
  --criteria-met <criteria_met> \
  --criteria-total <criteria_total> \
  --rating <rating> \
  --mode <mode> \
  --outcome <outcome> \
  --notes "<notes>"
```

Add `--failed-criteria` and the failure flags when the packet's failure line is not `none`. A sentence such as "tests pass" without the pasted output is incomplete for Phase 5. A finished run with no `bin/append.py` exit code is missing its rating step.

## Surfaces

| Target | How |
|--------|-----|
| Cursor cloud agent | Paste the packet into the cloud agent prompt; point at the existing repo. |
| Local `cursor-agent` | Run in the existing working tree. Do not `git clone` first from Grok Bot. |

## Isolation

Do not spawn Grok Build personas (`gxp-researcher`, `gxp-architect`, `gxp-verifier`). Cursor follows its own GXP rule. Bot supplied the brief and widget approval; a small tweak, if any, is already on the checkout.
