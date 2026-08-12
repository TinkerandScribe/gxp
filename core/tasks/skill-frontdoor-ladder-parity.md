# Task brief

**Date:** 2026-08-10
**Task slug:** skill-frontdoor-ladder-parity
**Workflow:** full

## Goal

Bring the tracked `SKILL.md` front-doors that restate verification up to current core
methodology — the Verification ladder and the where-to-append ratings rule — and put
them under a marker check so they cannot silently fall behind again.

## Context

- Related files: `adapters/cowork/plugin-src/skills/gxp-workflow/SKILL.md` (153 lines),
  `adapters/grok/ai-workflow/SKILL.md` (143), `adapters/grok-build/SKILL.md` (123),
  `adapters/grok/ai-workflow/grok-web/gxp.skill.md` (175),
  `adapters/cowork/plugin-src/skills/gxp-rate/SKILL.md` (69);
  `adapters/cursor/ai-workflow/sync/check-core.{sh,ps1}` (the proven marker pattern);
  `adapters/cowork/build.sh` (frontmatter validation must keep passing).
- Related PRs / tickets: supersedes the scoping of
  `core/tasks/track-claude-skill-source.md` (see below).
- Relevant rules: `core/rules/02-local-context-never-committed.md` (public-facing copy).
- Relevant failures: `core/failures/powershell-double-quote-backtick-eats-markdown.md`
  — write markdown via Python/editor tooling, never PS double-quoted strings.
- Ontology (if used): none.

**Why this and why now.** The Verification ladder and the where-to-append ratings rule
are in `core/workflow.md`, and the cursor adapter enforces both across seven files. But
**every tracked `SKILL.md` front-door carries neither** — measured 2026-08-10:

```
cowork gxp-workflow / gxp-rate / gxp-brief / gxp-failure-capture   ladder=0  where-to-append=0
grok ai-workflow · grok-build · grok-web gxp.skill · perplexity    ladder=0  where-to-append=0
(published gxp-skill.zip SKILL.md — untracked)                     ladder=1  where-to-append=1
```

Severity is moderate, not critical: `references/workflow.md` is pulled from core at
build time for both the cowork plugin and the published zip, so an agent reading the
canonical reference does get the ladder. The gap is in the condensed front-door body —
it under-teaches, it does not misteach.

**This dissolves most of the skill-tracking problem as a side effect.** The published
`SKILL.md` differs from the tracked cowork sibling by exactly three hunks: frontmatter
(`name: gxp` vs `gxp-workflow` — intentional and permanent), the ladder (20 lines), and
where-to-append (1 line). Port the two content hunks and the published body becomes
reconstructible from tracked sources plus a frontmatter swap — so the "unique content
exists only inside a release zip" risk largely goes away without tracking a second copy.
Criterion 5 below makes that measurable. `track-claude-skill-source.md` should be
re-assessed only after this lands.

**Scope note — which files.** Only front-doors that *restate* the verification phase
need the ladder (measured: cowork `gxp-workflow`, grok, grok-build, grok-web all restate
Phase 5). `gxp-rate` does not restate verification but is the ratings skill, so it takes
the where-to-append rule only. `gxp-brief`, `gxp-failure-capture`, and the perplexity
adapter (0 Phase-5 restatement; presence-only research design) take neither.

**Strategy/Model:** claude-code / local-agent — additive prose insertions plus a
mechanical marker check mirroring an existing in-repo pattern.

**Scaffolding tier:** standard — established pattern, bounded file set, public-facing
copy warrants a wording gate but no novel design.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [claude-code, local-agent, cursor]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human
- **output_contract:** PR touching the 5 skill bodies + marker checks; `verify.sh` 0;
  cowork build 0; negative test demonstrated; rating appended.

## Ideal State Criteria

- [outcome] 1. `adapters/cowork/plugin-src/skills/gxp-workflow/SKILL.md`,
  `adapters/grok/ai-workflow/SKILL.md`, `adapters/grok-build/SKILL.md`, and
  `adapters/grok/ai-workflow/grok-web/gxp.skill.md` each contain the Verification
  ladder guidance (thin-suite-exit-0 is necessary-not-sufficient; walk each criterion
  with a named check; prefer a second layer), consistent with `core/workflow.md`.
- [outcome] 2. `adapters/cowork/plugin-src/skills/gxp-workflow/SKILL.md` and
  `adapters/cowork/plugin-src/skills/gxp-rate/SKILL.md` each state the where-to-append
  rule (a run's rating lives where its artifacts live; `.ai/ratings.jsonl` installed,
  `core/ratings.jsonl` for work whose subject is the source repo).
- [outcome] 3. A marker check asserts criteria 1–2 for each of those files, with `.sh`
  and `.ps1` parity, following the `adapters/cursor/ai-workflow/sync/check-core.*`
  pattern, and is reached by `bash scripts/verify.sh`.
- [outcome] 4. Deleting a ladder marker from any one covered file makes that check exit
  non-zero and `bash scripts/verify.sh` exit non-zero (demonstrated once, then
  restored); both exit 0 on the clean tree.
- [outcome] 5. After the port, the published v1.3.1 `gxp/SKILL.md` differs from
  `adapters/cowork/plugin-src/skills/gxp-workflow/SKILL.md` **only** in the YAML
  frontmatter block (`name:` / `description:`) — verified by a normalized diff whose
  every hunk lies within the frontmatter.
- [guardrail] 6. No changes to `core/workflow.md`, `core/routing.md`, or
  `core/templates/*`; changes to the five skill bodies are additive (no existing
  guidance removed or weakened), and the perplexity / `gxp-brief` /
  `gxp-failure-capture` bodies are untouched.
- [guardrail] 7. `bash adapters/cowork/build.sh` exits 0 with frontmatter validation
  passing, and the built plugin still contains all four skills — i.e. the edits do not
  break packaging.
- [hypothesis] 8. Insertion point is each file's Phase 5 / verification section, reusing
  the wording already proven in the published `SKILL.md` and the cursor adapter rather
  than authoring new prose. The implementer may adapt wording per adapter voice.

**Anti-gaming (non-binding review question):** Does each edit actually teach the ladder
where an agent will read it, or merely place the literal string where a grep finds it?
A marker check rewards string presence; the objective is that an agent following the
front-door alone performs the second verification layer. Prefer inserting into the
verification section over appending a decorative block.

## Ontology / Domain Model (optional)

Not in use.

## Out of scope

- `core/` methodology changes of any kind — the ladder text already exists there; this
  task propagates it, it does not redefine it.
- The remaining Phase-8/Handoff gap in `adapters/{claude,chatgpt}/.../custom-instructions.md`
  (same unenforced-periphery theme, different files) — **recommended follow-up**.
- Tracking the published `SKILL.md` as a source file — deferred to
  `track-claude-skill-source.md`, to be re-assessed after criterion 5 shows how little
  unique content remains.
- Cutting a release, rebuilding the published zip, or changing what it ships.
- The perplexity adapter's presence-only sync check design.

## Verification plan

Deterministic first:

1. **C1/C2** — `grep -c` each marker in each covered file → ≥1; read each insertion in
   context to confirm it sits in the verification/rating section, not appended.
2. **C3** — run the new/extended check directly (`.sh`, and `.ps1` under Windows
   PowerShell 5.1) → exit 0; confirm both assert the same marker list; confirm
   `scripts/verify.sh` reaches it.
3. **C4** — delete one ladder marker line → check exits non-zero and `verify.sh` exits
   non-zero; `git checkout` the file; re-run both → exit 0; `git status` clean.
4. **C5** — extract `gxp/SKILL.md` from the published v1.3.1 asset; `diff` with
   `tr -d '\r'` normalization against the cowork body; assert every reported hunk falls
   inside the frontmatter line range.
5. **C6** — `git diff` shows no `core/` paths and no deletions in the five bodies
   (additions only, apart from any deliberate frontmatter-adjacent edit).
6. **C7** — `bash adapters/cowork/build.sh` → exit 0; list the built plugin's skills.

Behavioral: none required. Subjective: read each edited section once for voice and flow
in its adapter's register.

## Self-evaluation gate

- [x] **Completeness** — covers which files, what content, enforcement, non-regression
  of packaging, and the measurable dissolution of the tracking problem.
- [x] **Ambiguity** — every binding criterion is a grep count, an exit code, a diff, or
  a hunk-range assertion.
- [x] **Scope trap** — Phase-8 custom-instructions gap, skill tracking, releases, and
  core edits are all explicitly parked with pointers.
- [x] **Verification** — each binding criterion has a concrete check; criterion 4 is
  proven by induced failure.
- [x] **Approval gates** — this edits public-facing instructional copy, so wording gets
  a gate (below); nothing destructive or irreversible.
- [x] **Criteria quality** — 1–5 outcomes, 6–7 guardrails, 8 non-binding mechanism.
  Criterion 5 is an outcome about state, not about how the port is written.
- [x] **Anti-gaming** — answered above; the risk is grep-satisfying placement, which the
  in-context review in the verification plan is designed to catch.
- [x] **Ontology (if used)** — n/a.

## Approval gates

- **Gate 1 — brief approval** before implementation.
- **Gate 2 — wording review** of the inserted copy before it lands, since these files
  are published instructional surfaces (claude.ai skill, Cowork plugin, Grok skills).

## Dead ends

- (none yet)

## Handoff notes

To fill in at the end:

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Approval gates hit and outcomes:
- New `failures/` entries or rules:
- Rating entry reference:
