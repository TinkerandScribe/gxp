# Implementation brief — `gxp-refine` (thin invocable surface + tests)

**Date:** 2026-07-23  
**Task slug:** gxp-refine-implement  
**Status:** done — shipped PRs #3–#5 (v0 + selftest-in-verify + Claude/Grok surfaces)  
**Depends on:** [`gxp-refine-design.md`](gxp-refine-design.md) (merged on `main`)  
**Workflow:** full  
**Suggested branch:** `feat/gxp-refine-v0`

---

## OPERATOR PROMPT (copy-paste into Cursor / Claude / Codex)

```
Follow GXP full workflow (verification-first, binary Ideal State Criteria, permission-first,
review-gated). Repo: https://github.com/TinkerandScribe/gxp — work on latest main.

Canon: core/workflow.md
Design (must obey): core/tasks/gxp-refine-design.md
This brief: core/tasks/gxp-refine-implement.md

=== AUTHORIZATION / SCOPE (hard limits) ===
You ARE authorized to:
- Pull latest main; create branch feat/gxp-refine-v0 (or repo-conventional equivalent).
- Implement a THIN operator-invoked gxp-refine surface as specified below.
- Add docs/templates needed for the mode + Windows-friendly validation notes.
- Add automated checks that prove the mode is documented, discoverable, and fail-closed
  (no auto-promote).
- Run bash scripts/verify.sh and any new selftests; fix failures caused by this change.
- Commit, push, open a DRAFT PR targeting main.

You are NOT authorized to:
- Merge the PR or push directly to main.
- Auto-apply or auto-merge refine candidates (no auto-promote).
- Change core/routing.md privacy/stakes rails, weaken Verification ladder / anti-loop /
  approval-gate / L3/L4 language in core/workflow.md.
- Edit golden hidden_tests/ mid-campaign or invent a continuous self-rewrite loop.
- Ship a multi-provider critic product.
- Rename the mode to gxp-rsi / gxp-auto.
- Expand into a full orchestration platform (graphs, telemetry product, etc.).

Stop after opening a DRAFT PR with green verify. Operator merges.

=== GOAL ===
Implement gxp-refine v0 per the design brief: an explicit, operator-invoked bounded
self-refinement mode with mutation budget = 1 and dual approval gates.

v0 = documentation + template + discoverability + fail-closed checks.
Prefer the smallest ship that an operator can invoke in Cursor/Claude by pasting or
loading a skill/section — not a large new runtime.

=== PHASE 0 ===
Read and ground on current versions of:
- core/tasks/gxp-refine-design.md (full)
- core/workflow.md (Verification ladder, Phase 6 where-to-append, L3/L4)
- core/templates/weekly-refine.md (complement; do not delete)
- core/templates/task-brief.md
- core/routing.md (hard rails)
- core/evals/README.md + PROTOCOL patterns for baseline-vs-candidate language
- adapters/cursor/ai-workflow/rule.mdc (if Cursor mention needed — pointer only)
- CONTRIBUTING.md, scripts/verify.sh
- ROADMAP.md (claim gate; explicitly-out items)

Search: refine, weekly refine, approval gate, mutation, promote.

=== REQUIRED DELIVERABLES (v0) ===
1) Template for a refine run, e.g. core/templates/gxp-refine-run.md
   Must encode: evidence skim → ONE weakness → ONE hypothesis → ONE target path →
   ONE eval plan (pinned baseline SHA/tag, fixed corpus, primary metric) →
   GATE 1 experiment approve → baseline/candidate results → recommend →
   GATE 2 promotion approve → no auto-apply.
   Mutation budget = 1 stated explicitly. Exists-now vs proposed labels.

2) Operator-facing how-to (short), e.g. section in README or core/docs / adapters
   README pointer — ONE place of truth preferred.
   Must say: Windows operator can run verify via Git Bash/WSL:
     bash scripts/verify.sh
   and how to invoke gxp-refine (paste START prompt / skill name).

3) Invocable prompt surface (pick ONE primary, document others as follow-ups):
   Preferred for this repo’s Cursor users:
   - adapters/cursor/... START snippet OR a small gxp-refine section in rule.mdc
     that ONLY activates when operator says "gxp-refine" / "run gxp-refine"
     (must NOT run during ordinary tasks).
   OR a Claude skill fragment under adapters/claude/ if that matches existing skill-src.
   Do NOT invent a second parallel surface in the same PR unless trivial cross-links.

4) Automated tests / checks (Windows-aware):
   - bash scripts/verify.sh still exits 0.
   - Add a small selftest script (sh) and/or structural checks that assert:
     a) gxp-refine template exists and contains required markers
        (mutation budget, GATE 1, GATE 2, operator-invoked, no auto-merge).
     b) design brief still referenced / linked from the how-to.
     c) forbidden strings absent from invocable surface: gxp-rsi, auto-merge promote,
        unattended self-rewrite (reasonable grep).
   - Document running the selftest on Windows via Git Bash:
       bash scripts/eval-gxp-refine-selftest.sh   # name may vary; create it

5) Optional but valuable: one dry-run example refine brief under core/tasks/ as
   EXAMPLE-gxp-refine-run.md (fictional weakness; no real core edit). Mark as example.

=== IDEAL STATE CRITERIA (binary) ===
- [x] 1. core/templates/gxp-refine-run.md exists and contains explicit mutation-budget=1,
      GATE 1, GATE 2, operator-invoked-only, and “no auto-apply/auto-merge” language.
- [x] 2. An operator how-to exists and links to gxp-refine-design.md + the run template;
      includes Windows Git Bash verify + selftest commands.
- [x] 3. An invocable surface exists that activates only on explicit operator request
      (documented trigger phrases); ordinary GXP start prompts do not auto-enter refine.
- [x] 4. bash scripts/verify.sh exits 0 on the branch.
- [x] 5. A new selftest script exits 0 and fails if required markers are removed
      (negative check documented or implemented).
- [x] 6. No edits to core/routing.md hard rails; no weakening of Verification ladder /
      anti-loop / approval gates / L3/L4 in core/workflow.md (diff review).
- [x] 7. Naming is gxp-refine only (no gxp-rsi / gxp-auto in shipped surface).
- [x] 8. DRAFT PR opened; main not merged by the agent; rating line appended to
      core/ratings.jsonl for this implement run.

=== OUT OF SCOPE ===
- Actually running a live refine that mutates core/workflow.md in this PR.
- Changing golden hidden_tests or claiming M6 scientific lift.
- Full multi-adapter skill ports (can park as follow-up).
- Auto-promotion machinery.

=== GIT / PR ===
- Branch from latest main.
- Keep diff focused; park unrelated dirty local files.
- Commit messages: feat/docs/test as appropriate (conventional).
- Push; open DRAFT PR.
- PR body: link design brief; list ISC checklist; verify + selftest results;
  Windows run notes; “no auto-promote”.

=== COMPLETION REPORT ===
Return: branch, SHAs, files changed, verify/selftest commands+exits, draft PR URL,
confirmation main untouched / not merged.
```

---

## Goal (brief form)

Ship **gxp-refine v0**: template + how-to + operator-triggered surface + automated
marker/selftest checks, fully compliant with
[`gxp-refine-design.md`](gxp-refine-design.md), runnable/validated on Windows via
Git Bash/`verify.sh`.

## Context

- Design merged: `ad72c9f` / PR #2 — `core/tasks/gxp-refine-design.md`.  
- Weekly refine template stays; gxp-refine is the heavier eval-gated mode.  
- Windows operators: prefer Git Bash or WSL for `bash scripts/*.sh`.  
- Risk ladder and dual gates are binding.

**Strategy/Model:** Cursor or Claude Code on Windows — full GXP; stop at draft PR.

## Ideal State Criteria

Same checklist as in the operator prompt above (items 1–8).

## Out of scope

Same as operator prompt.

## Verification plan

1. `bash scripts/verify.sh` → exit 0.  
2. New `bash scripts/eval-gxp-refine-selftest.sh` (or chosen name) → exit 0; include a
   documented negative case.  
3. `git diff origin/main...HEAD` reviewed: no routing/core gate weakening.  
4. Manual: trigger phrases documented; ordinary START_SESSION does not imply refine.  
5. Subjective: an operator can complete a dry-run refine brief without inventing gates.

## Approval gates

- **Gate I:** Operator reviews DRAFT PR before merge.  
- **Gate II (post-merge):** First real refine that targets routing/core requires design
  risk-ladder stakes and separate experiment + promotion approvals.

## Dead ends

-

## Handoff notes

- Paste the **OPERATOR PROMPT** block into a fresh agent session.  
- Keep local unrelated dirty files out of the PR.  
- After merge, first live refine is a **separate** operator-invoked run using the new
  template — not part of v0 ship unless explicitly authorized.
