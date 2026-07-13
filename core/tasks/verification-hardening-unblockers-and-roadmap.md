# Task brief

**Date:** 2026-07-13
**Task slug:** verification-hardening-unblockers-and-roadmap
**Workflow:** full

## Goal

Ship the two trivial unblockers from the audit review (grok sync-check def-order fix;
GxP naming disclaimer) and author the verification-hardening roadmap plus draft briefs
for the three P0 items, with the review's corrected sequencing (P0-2 → P0-1 → P0-3)
and interaction bugs baked in.

## Context

- Source: `core/tasks/review-external-audit-fix-plan.md` (verdict + per-item
  disposition) and the external audit doc it reviewed.
- Known interactions to encode: P0-1's negative-drift test is dead until P0-2 lands
  (allowlisted "Workflow Definition"); P0-3 wakes grok's dormant pre-definition crash
  (fixed by this task).
- Checked: chatgpt/claude `check-core.sh` do NOT share grok's `log`/`$YELLOW`
  use-before-definition (no such identifiers in either) — only grok needs the fix.
- Rules 01/02 apply (public-facing README text; nothing private).
- Briefs for P1/P2 items are deliberately NOT written now — GXP writes briefs at
  pickup, not months ahead; the roadmap marks them brief-on-pickup.

**Strategy/Model:** current Claude Code session — small script edit + docs authoring
with live bash verification; smallest capable engine.

## Ideal State Criteria

- [ ] 1. In grok `check-core.sh`, the last-synced NOTE block executes only after
  `log()`/`$YELLOW` are defined; with a real hex SHA temporarily substituted into the
  grok marker, the script runs with no "unbound variable" error and exits 0
  (restored afterward).
- [ ] 2. README contains a GxP naming disclaimer (Guided eXecution Protocol vs
  GMP/GLP/GCP) visible near the top; `grep -i "GMP" README.md` matches.
- [ ] 3. `ROADMAP.md` exists at repo root: corrected sequence with explicit dependency
  notes for both interaction bugs, milestone grouping, and per-item status; README
  links to it.
- [ ] 4. Three draft briefs exist under `core/tasks/` (P0-2 real-diff sync checks;
  P0-1 CI workflow; P0-3 staleness marker), each with 4–8 binary ISC, out-of-scope,
  verification plan, and a **Depends on** line.
- [ ] 5. `bash scripts/verify.sh` exits 0 after all changes.
- [ ] 6. `git status` shows only: grok `check-core.sh`, `README.md`, `ROADMAP.md`,
  new/changed files under `core/tasks/`, and the `ratings.jsonl` append (plus the
  prior review run's still-uncommitted artifacts).
- [ ] 7. Rating appended to `core/ratings.jsonl` per live-ledger policy.

## Out of scope

- Implementing P0-2, P0-1, P0-3 themselves (briefs only).
- Briefs for P1/P2 items (roadmap lists them as brief-on-pickup).
- The grok ps1 twin (its NOTE path sits after function definitions in main execution —
  not affected).
- Committing/pushing (operator decides after review).

## Verification plan

C1: temporary-SHA behavioral test + restore, plus shellcheck-style read. C2/C3: grep +
file reads. C4: file existence + section checks. C5: run verify.sh, record exit code.
C6: git status --short. C7: tail ratings.jsonl.

## Self-evaluation gate

- [x] **Completeness** — covers both approved unblockers + roadmap + P0 briefs.
- [x] **Ambiguity** — criteria are exit codes, grep hits, and file-state checks.
- [x] **Scope trap** — P1/P2 briefs and all P0 implementation explicitly parked.
- [x] **Verification** — concrete check per criterion.
- [x] **Approval gates** — none: reversible working-tree edits; no commit/push/release.

## Approval gates

- None.

## Dead ends

- None. But the criterion-1 behavioral test surfaced a new defect beyond the audit:
  the marker regex (`core:\ `) can never match the bold marker format (`core:** `),
  so P0-3 as sketched ships a mechanism that still never fires. Evidence and the fix
  requirement now live in `core/tasks/staleness-marker-real-sha.md` and ROADMAP
  correction 3.

## Handoff notes

- What changed: grok `check-core.sh` (staleness NOTE relocated after helper
  definitions), `README.md` (GxP naming disclaimer + ROADMAP link), new `ROADMAP.md`,
  three P0 draft briefs under `core/tasks/`, this brief, one rating line, one new
  failure entry (`jsonl-append-via-shell-heredoc-corrupts-escapes.md`).
- Verified: aged regex-matching marker → NOTE prints, no set-u crash, exit 0
  (restored); real-SHA-in-bold-format → no match (the new finding); verify.sh exit 0;
  README greps; all ratings lines parse as JSON.
- Parked: all P0/P1/P2 implementation (briefs/roadmap only); P1/P2 briefs are
  brief-on-pickup.
- Approval gates: none hit. Not committed — operator decides.
- Rating: core/ratings.jsonl ts 2026-07-13T10:40:00-03:00, 7/7, rating 9.
