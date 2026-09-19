# Coding-agent brief — experimental branch + paired main-vs-branch test

You are a local coding agent on an existing checkout. Do not clone. Do not merge to main. Do not push. Do not open a PR. Do not touch PRs #24 or #25.

## Repo
- Local source of truth: C:\Users\Reepicheep\Claude\gxp
- GitHub: https://github.com/TinkerandScribe/gxp
- Last remote snapshot we read: main @ 080d282. Re-audit Phase 0 on the local tree before editing.
- If the working tree is dirty or already on feat/grok-bot-adapter, do not stash-destroy work. Create the experimental branch from the current HEAD and keep the change additive.

## Goal
Put the four named SHE-style artifacts and one Cordis-style inverse rule on an **experimental git branch**, then compare that branch to current main (or the current default) with a paired protocol test. Decide keep/discard the same way SHE does: keep only if the new protocol is stricter or clearer AND utility does not regress (existing verify still passes; no extra operator burden on a normal task).

This is a harness-protocol experiment, not a model-evolution run. Do not expect ASR/UA deltas.

## Branch
- Name: `experiment/four-artifacts-inverse`
- One reversible candidate (gxp-refine shape). Inverse of the whole change: delete the four templates, the Phase 0 bullet, the inverse paragraph, the Phase 5 heading, and the experiment notes.
- Leave main / the default branch untouched.

## Out of scope
- SHE 20-round diagnose-edit evolution, Ω judges, Agent-SafetyBench
- Cordis TypeScript runtime, ctx.effect, fibers, HMR
- Intern-S2, I-SDPO, LOPD, MemDec
- idea-gate / mooring-line / scribe-workbench / Heartwood
- Rewriting Phase 5’s verification ladder
- Touching #24 alignment text
- Personas
- Merge, push, PR

## Smallest change (on the experimental branch only)

1. Four optional GXP-style markdown templates (match `core/templates/rule-packs/`, not SHE JSONL):
   - `core/templates/system-prompt.md.template`
   - `core/templates/rule-bank.md.template`
   - `core/templates/safety-memory.md.template`
   - `core/templates/tool-policy.md.template`
   Each: title, one-paragraph purpose, empty or one GXP-shaped stub, “operator-owned; not auto-evolved.”
2. `core/workflow.md` Phase 0: one bullet — if those four artifacts are present in the repo or `~/.gxp/`, read them with PROGRAM / rules / failures.
3. `core/workflow.md` Phase 3 or 4 (shorter insertion) plus one sentence in `core/routing.md` reversibility:
   - If you load an adapter, plugin, MCP, skill, or Phase 3 handoff, name its inverse (how to unload it).
   - Unload = apply the named inverse (left-inverse, LIFO if several).
   - If you cannot name an inverse, treat the action as irreversible and use the existing human gate.
   - Inverse correctness is the author’s obligation; GXP does not verify it.
   - Do not write the slogan “full undo.”
4. `core/workflow.md` Phase 5: named binary gate, do not replace the ladder:
   - Heading: “Verified against the brief (binary)”
   - Before Phase 6, every binding ISC has a recorded pass/fail.
   - Smoke / verify exit 0 is necessary, not sufficient.
   - If any binding ISC is unmet, Phase 5 fails.
5. Tool Policy stub only: a coding agent pointed at a live product tree (Kickoff, WorkshopOS, lumen, fab-shop, or any unnamed “find issues” brief) is read-only unless the brief names writes; no exploit-chain retry; vuln-shaped findings escalate to a human.
6. If `scripts/generate-adapter-workflows.py` regenerates adapter bodies from `core/workflow.md`, run it and keep the generated delta limited to the new sentences. Do not edit grok-bot SKILL/handoff unless you are already on #25 and the edit is a one-line mention; prefer leaving #25 alone.
7. Add `experiments/four-artifacts-inverse.md` on the branch: short protocol + the record table below + the keep/discard rule. This is the experiment log, not a new phase.

## Paired test (required)

Two layers. Do both. Record results in `experiments/four-artifacts-inverse.md`.

### Layer A — deterministic harness diff (must pass)

Compare `experiment/four-artifacts-inverse` to the branch you forked from (call it BASE).

| Check | BASE | Experiment | Pass if |
|---|---|---|---|
| Four template files exist | no | yes | only on experiment |
| Phase 0 names the four artifacts | no | yes | only on experiment |
| Named inverse / unload sentence | no | yes | only on experiment |
| Phrase “full undo” | no | no | absent on both |
| Phase 5 “Verified against the brief (binary)” | no | yes | only on experiment |
| Phase numbers 0, 0.5, 1–8 unchanged | yes | yes | same set |
| Existing verify scripts exit 0 | yes | yes | both green |

Run existing `scripts/verify.sh` (or the Windows equivalent) on the experiment branch. If you can run it on BASE without checking out (or via a second worktree), do that too. Do not destroy local work to get a second checkout.

### Layer B — paired protocol walk (one same task)

Do **not** invent a product feature. Use a tiny in-repo GXP lightweight walk (Phases 1, 2, 3, 5) whose only “implementation” is something already reversible (for example: add a one-line comment to an experiment note, or fill the record table). The task must **load** something so the inverse rule can fire or stay silent: treat the four templates as a loaded pack whose inverse is “stop reading them / ignore them.”

Run the same task brief twice in the log (you may simulate the BASE walk from BASE’s workflow.md text if a second live agent run is impossible; say which you did):

Task brief (use this):
- Goal: Record whether the current GXP text requires reading four named artifacts and naming an inverse for a loaded pack.
- ISC:
  - [outcome] Phase 0 either lists the four artifacts or does not.
  - [outcome] Phase 5 either names a binary brief-walk or does not.
  - [guardrail] No live product tree is written.
  - [guardrail] Inverse of this task is “delete the record row.”
- Verify: the record table has one BASE row and one experiment row.

Record per side:

| Side | Phase 0 read four artifacts? | Phase 5 wrote pass/fail per ISC? | Inverse named for the loaded pack? | Inverse gate fired or silent? | criteria_met / criteria_total | Phase 4 tripped? |
|---|---|---|---|---|---|---|
| BASE | | | | | | |
| experiment | | | | | | |

Expected difference: BASE is no/no/no/silent; experiment is yes/yes/yes/silent (gate silent because the inverse *was* named). If the experiment side cannot name an inverse, the gate must fire and that is a fail of the change, not a pass.

Keep/discard:
- Keep the experiment (leave the branch; still do not merge) only if Layer A passes AND Layer B utility did not regress (verify green; the walk did not need extra operator steps that BASE did not need).
- Discard = delete the branch / revert the commit. Write that recommendation at the bottom of the experiment note.

## Ideal State Criteria (binary)
- [outcome] Branch `experiment/four-artifacts-inverse` exists and main/default is untouched.
- [outcome] Four named optional templates exist on that branch.
- [guardrail] Phase list stays 0, 0.5, 1–8.
- [guardrail] A quoteable unload/inverse sentence exists; “full undo” does not.
- [outcome] Phase 5 names “verified against the brief” as a binary gate.
- [outcome] `experiments/four-artifacts-inverse.md` has Layer A results and a Layer B table with both rows filled.
- [guardrail] No SHE evolution scripts, no Cordis dependency.
- [hypothesis] “Cannot name an inverse” still maps to the existing irreversibility human gate.
- [guardrail] Existing verify still passes on the experiment branch.
- [guardrail] No merge, push, or PR.

## Verify
1. `git branch --show-current` is `experiment/four-artifacts-inverse`.
2. `git merge-base` / log shows main/default was not moved.
3. Layer A table all pass.
4. Existing verify exit 0 on the experiment branch.
5. Layer B table has BASE and experiment rows, with the expected difference named in one sentence.
6. Recommendation: keep branch or discard, with the inverse named.

## Stop
Two same-shape failures → stop, document, reframe. Do not add a fifth artifact, a new phase, or a SHE Ω loop to get a “result difference.”
