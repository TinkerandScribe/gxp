# Task brief

**Date:** 2026-08-10
**Task slug:** track-claude-skill-source
**Workflow:** full
**Status:** DEFERRED — do not pick up as written. Re-assess only after
`skill-frontdoor-ladder-parity.md` lands.

> **Why deferred (2026-08-10, same day as drafting).** After this brief was written, a
> hunk analysis showed the published `SKILL.md` differs from its tracked cowork sibling
> by exactly three hunks: frontmatter (intentional), the Verification ladder (20 lines),
> and where-to-append (1 line). Porting those two content hunks — the work this brief
> put *out of scope* — makes the published body reconstructible from tracked sources
> plus a frontmatter swap, which removes most of this brief's justification. The
> ordering here was backwards: the reconciliation is the higher-value first step and it
> largely dissolves the tracking problem. See
> `core/tasks/skill-frontdoor-ladder-parity.md` criterion 5, which measures exactly how
> much unique content remains. If that criterion passes, what is left of this brief is
> probably a one-line note in the release process rather than a tracked file.

## Goal

Bring the published Claude skill's `SKILL.md` under version control and under the
existing marker-check discipline, so the project's most methodologically current skill
body is recoverable from git rather than only from a downloaded release asset.

## Context

- Related files: released `gxp-skill.zip` asset (v1.3.1) — `gxp/SKILL.md`;
  `scripts/verify.sh` (`require` idiom); `adapters/cursor/ai-workflow/sync/check-core.{sh,ps1}`
  (proven marker-assertion pattern for ladder / where-to-append);
  `adapters/cowork/plugin-src/skills/gxp-workflow/SKILL.md` (nearest tracked sibling).
- Related PRs / tickets: supersedes nothing; this is the "separately briefed" path that
  `core/tasks/research-parked-stash-relevance.md` left open
  (*"skill-zip builder remains out of scope unless separately briefed"*).
- Relevant rules: `core/rules/02-local-context-never-committed.md` — the content to be
  tracked was leak-scanned (0 hits) before this brief was written.
- Relevant failures: `core/failures/powershell-double-quote-backtick-eats-markdown.md`
  — write markdown via Python/editor tooling, not shell heredocs or PS double quotes.
- Ontology (if used): none.

**Background — why this is not the twice-rejected work.** The earlier parked draft
proposed a tracked *builder* (`scripts/build-skill-zip.sh` + `skill-src/`) justified as
fixing silent drift of the released asset. That justification was **disproven** on
2026-08-10: every released zip (v1.1.1, v1.3.0, v1.3.1) is byte-exact with `core/` at
its own tag, all files, modulo line endings — the hand-assembly has been correct 3/3,
and the reference files are pulled from core at assembly time. The prior rejections
were right on the evidence they addressed.

The residual problem is narrower and different: of the six files in the zip, five are
generated from tracked core sources, but **`SKILL.md` has no tracked source anywhere in
the repo**. It exists only inside published release assets, and each release is
assembled by reading the *previous release's extracted copy* from a gitignored scratch
dir. It has also diverged upward — the shipped `SKILL.md` is the only skill body in the
project carrying the Verification ladder and the where-to-append ratings rule; all
eight tracked `SKILL.md` front-doors carry neither, and nothing asserts their content.
Severity is moderate, not critical: `references/workflow.md` *is* pulled from core and
does carry the ladder, so users' agents reading the canonical reference get the full
methodology — the gap is in the condensed front-door body only.

**Strategy/Model:** claude-code / local-agent — single tracked file plus a mechanical
marker check mirroring an existing in-repo pattern; criteria are string and exit-code
checks.

**Scaffolding tier:** standard — established pattern (cursor `check-core` markers,
`verify.sh require`), no novel design.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [claude-code, local-agent, cursor]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human (operator approves the brief before implementation)
- **output_contract:** PR adding one tracked source file + verify wiring; `verify.sh`
  exit 0; negative test demonstrated; rating appended.

## Ideal State Criteria

- [outcome] 1. A tracked `SKILL.md` source exists in the repo whose content is
  byte-identical (ignoring line endings) to `gxp/SKILL.md` in the published v1.3.1
  `gxp-skill.zip`.
- [outcome] 2. `bash scripts/verify.sh` `require`s that path, and exits non-zero when
  the file is absent (tested by temporary rename, then restored).
- [outcome] 3. A marker check asserts the tracked skill body carries, at minimum:
  `Verification ladder`, where-to-append ratings guidance, and Phase 0–8 coverage
  including Handoff — following the `adapters/cursor/ai-workflow/sync/check-core.{sh,ps1}`
  pattern, with both `.sh` and `.ps1` parity.
- [outcome] 4. Deleting any one asserted marker from the tracked file makes the check
  exit non-zero (demonstrated once, then restored); `bash scripts/verify.sh` exits 0 on
  the clean tree.
- [guardrail] 5. No changes to `core/workflow.md`, `core/routing.md`, or any
  `core/templates/*` — this task tracks an adapter-side artifact only.
- [guardrail] 6. No build/assembly script is added, no release is cut, no tag is pushed,
  and `_grok_fill/` and `gxp-release-asset/` remain gitignored with nothing committed
  from them other than the single `SKILL.md` body in criterion 1.
- [guardrail] 7. `git grep` for `C:\Users`, `/mnt/c/Users`, and the operator username
  over tracked files returns zero hits after the change (rule 02).
- [hypothesis] 8. Path is `adapters/claude/skill-src/SKILL.md` (an empty untracked
  directory of that name is already present as leftover and would be either used or
  removed). The implementer may choose a better-justified location — e.g. alongside the
  existing claude adapter — without amending this brief.

**Anti-gaming (non-binding review question):** Does this satisfy the operator's actual
objective — that the current skill body survive loss of the release assets and stop
silently diverging from core — rather than merely placing a file in git? A tracked copy
that nothing asserts, and that the next release does not actually build from, would
pass the literal checklist while leaving the objective unmet. Flag this at Phase 3 if
the marker check (criteria 3–4) turns out not to bite.

## Ontology / Domain Model (optional)

Not in use for this task.

## Out of scope

- **A tracked builder / assembly script** (`build-skill-zip.sh` or equivalent) — the
  drift justification is disproven; assembly stays a one-off operator step. If a
  builder is ever wanted, it needs its own brief and its own justification.
- **Porting the Verification ladder and where-to-append rule into the other eight
  tracked `SKILL.md` front-doors** (cowork ×4, grok, grok-build, grok-web, perplexity).
  This is real and worth doing — it is the same unenforced-periphery theme as the
  Phase-8 gap in `custom-instructions.md` — but it edits methodology content across
  four adapters and deserves a separate brief. **Recommended follow-up.**
- Cutting v1.3.2, rebuilding any release asset, or changing what the published zip
  contains.
- Deciding whether released assets should track `[Unreleased]` — they should not;
  current tag-tracking behavior is correct and this brief does not change it.

## Verification plan

Deterministic first:

1. **C1** — extract `gxp/SKILL.md` from the v1.3.1 asset; `diff` against the tracked
   file with `tr -d '\r'` normalization on both sides → zero differing lines.
2. **C2** — `bash scripts/verify.sh` → exit 0; then `mv` the tracked file aside, re-run
   → exit non-zero and `MISSING:` printed; restore; confirm `git status` clean.
3. **C3** — read both check scripts; run each directly → exit 0; confirm the `.sh` and
   `.ps1` assert the same marker list (PowerShell 5.1 for the `.ps1`).
4. **C4** — delete one marker line, run the check → exit non-zero; `git checkout` the
   file; re-run `verify.sh` → exit 0; `git status` clean.
5. **C5/C6** — `git status --short` and `git diff --stat` show no `core/` paths, no new
   script under `scripts/`, and no files from the two ignored dirs.
6. **C7** — `git grep -nI "C:\\\\Users\|/mnt/c/Users\|Reepicheep"` over tracked files →
   zero hits.

Behavioral: none required beyond the negative tests (this artifact is consumed by
agents reading it, not executed). Subjective: confirm the tracked body still reads as a
coherent standalone skill after any frontmatter reconciliation.

## Self-evaluation gate

- [x] **Completeness** — covers the durable fix (tracked source), the thing that keeps
  it honest (marker check + negative test), and the leak/scope rails. The larger
  front-door reconciliation is named and parked rather than silently dropped.
- [x] **Ambiguity** — every binding criterion is a diff, an exit code, or a grep count.
- [x] **Scope trap** — the builder and the eight-file ladder port are both explicitly
  out of scope; the path choice is non-binding so layout debate cannot block the work.
- [x] **Verification** — each binding criterion has a concrete check above; criteria 2
  and 4 are proven by induced failure, not just by a green run.
- [x] **Approval gates** — no destructive, irreversible, or outward-facing step; the
  brief itself is the gate (operator approves before implementation).
- [x] **Criteria quality** — 1–4 are outcomes, 5–7 are guardrails, 8 is explicitly a
  non-binding layout hypothesis (learning directly from the prior rejection, which
  objected to an invented path being asserted as fact). No style-only binding lines.
- [x] **Anti-gaming** — answered above; the stated risk is a tracked-but-unasserted
  file, which criteria 3–4 exist to prevent.
- [x] **Ontology (if used)** — n/a.

## Approval gates

- **Gate 1 — brief approval.** Operator approves this brief before any implementation.
  Rationale: this theme has been declined twice on a since-disproven justification;
  proceeding without explicit sign-off on the *revised* justification would repeat that
  loop.
- No further gates during implementation (all changes reversible, nothing published).

## Dead ends

- Prior approach (twice declined): tracked builder + `skill-src/` justified as fixing
  silent asset drift. **Reframe after disproof:** the assumption "released assets drift
  from core" is false — verified 3/3 tags byte-exact. What is actually unversioned is
  one hand-maintained file, and what is actually unenforced is its content. Discarded
  assumption: that the fix required build automation.

## Handoff notes

To fill in at the end:

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Approval gates hit and outcomes:
- New `failures/` entries or rules:
- Rating entry reference:
