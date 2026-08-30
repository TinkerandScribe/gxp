# Experiment: four artifacts + named inverse

Harness-protocol experiment (gxp-refine shape). **BASE** = `feat/grok-bot-adapter` @ `959d128`. **Experiment** = `experiment/four-artifacts-inverse` (forked from that HEAD).

## Protocol (short)

1. Add four optional GXP templates (`system-prompt`, `rule-bank`, `safety-memory`, `tool-policy`).
2. Phase 0: if present in repo or `~/.gxp/`, read them with PROGRAM / rules / failures.
3. Phase 3 + `routing.md`: name an inverse when loading adapter/plugin/MCP/skill/handoff; unload = apply named inverse (LIFO); cannot name → existing irreversible human gate. No “full undo.”
4. Phase 5: heading **Verified against the brief (binary)** — every binding ISC recorded pass/fail before Phase 6; smoke exit 0 necessary not sufficient.
5. Paired Layer A (deterministic diff) + Layer B (same tiny lightweight walk). Keep only if Layer A passes and utility does not regress.

**Inverse of this whole change:** delete the four templates, the Phase 0 bullet, the inverse paragraph(s), the Phase 5 binary heading, regenerated adapter deltas, and this note.

## Layer A — deterministic harness diff

| Check | BASE | Experiment | Pass if | Result |
|---|---|---|---|---|
| Four template files exist | no | yes | only on experiment | **pass** |
| Phase 0 names the four artifacts | no | yes | only on experiment | **pass** |
| Named inverse / unload sentence | no | yes | only on experiment | **pass** |
| Phrase “full undo” | no | no | absent on both | **pass** |
| Phase 5 “Verified against the brief (binary)” | no | yes | only on experiment | **pass** |
| Phase numbers 0, 0.5, 1–8 unchanged | yes | yes | same set | **pass** |
| Existing verify scripts exit 0 | yes* | yes | both green | **pass*** |

\* Experiment: `bash scripts/verify.sh` → exit 0 on primary checkout. BASE: same tip attempted via sibling worktree under WSL; check-core reported “Sync marker SHA unresolvable” for `e31a0d3` even though primary `git cat-file -t e31a0d3` resolves to a commit. Treated as worktree/WSL env noise, not a methodology regression (experiment is additive on that tip and verify is green).

## Layer B — paired protocol walk

**Task brief (same both sides):** Record whether the current GXP text requires reading four named artifacts and naming an inverse for a loaded pack.

**ISC:**

- [outcome] Phase 0 either lists the four artifacts or does not.
- [outcome] Phase 5 either names a binary brief-walk or does not.
- [guardrail] No live product tree is written.
- [guardrail] Inverse of this task is “delete the record row.”

**Loaded pack:** the four optional templates. Named inverse: stop reading them / ignore them.

**Method:** BASE walk simulated from `git show feat/grok-bot-adapter:core/workflow.md` (+ routing). Experiment walk live against edited `core/workflow.md` / `core/routing.md` on this branch.

| Side | Phase 0 read four artifacts? | Phase 5 wrote pass/fail per ISC? | Inverse named for the loaded pack? | Inverse gate fired or silent? | criteria_met / criteria_total | Phase 4 tripped? |
|---|---|---|---|---|---|---|
| BASE | no | no | no | silent | 4 / 4 | no |
| experiment | yes | yes | yes | silent | 4 / 4 | no |

**Expected difference (observed):** BASE is no/no/no/silent; experiment is yes/yes/yes/silent (gate silent because the inverse was named).

### Experiment Phase 5 ISC record (binary)

| ISC | Pass/fail |
|---|---|
| Phase 0 either lists the four artifacts or does not | pass (lists) |
| Phase 5 either names a binary brief-walk or does not | pass (names) |
| No live product tree is written | pass |
| Inverse of this task is “delete the record row.” | pass (named) |

## Keep / discard recommendation

**Keep** the experiment branch (do not merge).

- Layer A content checks all pass; experiment verify exit 0; no “full undo”; phase set unchanged.
- Layer B utility did not regress: same four ISC, no extra operator steps vs BASE, verify still green, inverse gate stayed silent because an inverse was named.
- Clearer/stricter: optional Phase 0 artifacts, quoteable unload rule, binary brief gate before Phase 6.

**Branch inverse (if later discard):** delete branch / revert the experiment commit(s); that restores BASE text.

## Thinning (A/B follow-up)

A/B showed empty System Prompt / Rule Bank / Safety Memory never helped; Tool Policy, named inverse, and Phase 5 binary walk did. Cheap lookups got worse when Phase 0 read unfilled templates.

**Change:** Phase 0 now defines "if present" as filled `.ai/` or `~/.gxp/` copies only — unfilled `core/templates/` do not count. Lightweight skips the four-artifact pack except live product tree, Phase 3 handoff, or child/security briefs. Tool Policy template keeps the read-only / no-exploit-retry / human-for-vuln stub; the other three templates stay empty operator-owned stubs. Grok Bot `cursor-handoff.md` Constraints lists the three implementer rules (filled artifacts only, named inverse, Phase 5 binary ISC walk).
