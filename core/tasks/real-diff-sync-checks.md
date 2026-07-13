# Task brief — real sync-check content enforcement (audit P0-2, Option A)

**Status:** draft — not started (Milestone 1, item 1)
**Depends on:** nothing (first in sequence). Folds in audit P1-4 (Phase 8 + version
header for chatgpt/claude) — the new checks fail on today's drift, so the adapters
must be brought current in the same change.

## Goal

Replace whole-file drift allowlisting with checks that can actually fail: a
structural parity floor for intentionally rewritten adapter workflows, real per-hunk
diffs for files meant to be verbatim copies — and bring chatgpt/claude current so the
new floor passes on a clean tree.

## Context

- Review finding: at v1.1.2 the only CRITICAL comparison in claude/chatgpt/grok is
  allow-listed by label, so drift in `instructions/workflow.md` can never fail
  (empirically proven — appended drift still gave verify.sh exit 0).
- Claude/chatgpt/grok workflows are full rewrites by design ("informed alignment"),
  so a line-diff with regex allowlists degenerates to allow-everything for them; the
  honest floor is structural/semantic markers (the cursor adapter already models
  this). Verbatim-copy files (templates an adapter tracks) get real diffs.
- Current drift the new floor will catch: chatgpt "(v1.0)" header; Phase 8 missing
  from chatgpt and claude workflows. Fix these here, not later.

## Ideal State Criteria (draft — refine at pickup)

- [ ] 1. chatgpt and claude `instructions/workflow.md` contain Phase 8 (Handoff) and a
  version header matching core's workflow version; content consistent with core
  phases 0–8.
- [ ] 2. For each of claude/chatgpt/grok, the sync check (sh AND ps1) enforces a
  structural floor on `instructions/workflow.md`: Phases 0–8 present (incl. Handoff),
  4–8 binary criteria rule, anti-loop-after-two-failures, deterministic-first
  verification order, ratings fields (`ts`, `criteria_met`, `criteria_total`,
  `rating` 1–10).
- [ ] 3. Deleting the Phase 8 section from any of the three adapter workflows makes
  that adapter's sh check AND ps1 check exit non-zero (test then restore).
- [ ] 4. No allowlist entry can exempt a criterion-2 failure (whole-file
  "Workflow Definition" entries removed or narrowed to non-structural content).
- [ ] 5. Any file the sync config treats as a verbatim copy is byte-diffed; allowlist
  entries for such files are line-pattern regexes, not filenames/labels.
- [ ] 6. `bash scripts/verify.sh` exits 0 on the clean tree and 1 under the criterion-3
  induced deletion.

## Out of scope

- Build-time generation of adapter workflows (audit P0-2 Option B — Milestone 3
  candidate).
- CI (next brief); staleness markers (third brief).
- Perplexity/cursor sync checks (cursor already structural; perplexity presence-only
  by design for a research adapter — revisit in Milestone 3).

## Verification plan

Criterion 1: grep Phase 8 + header. Criteria 2–5: induced-mutation tests per adapter
per platform (bash + PowerShell 5.1), restore after each. Criterion 6: verify.sh runs
before/after. Deterministic first; no subjective checks needed.
