# Research prompt — parked stash relevance vs current `main`

**Date:** 2026-07-24  
**Task slug:** research-parked-stash-relevance  
**Status:** ready to paste into a research / review agent  
**Stash under review:** `stash@{0}: park-unrelated-before-gxp-refine`  
**Stash base (when parked):** ~`ad72c9f` (after design PR #2)  
**Current main at prompt authoring:** pull latest; expect post–PR #5 + sync markers  

**Do not** `stash pop` / `stash apply` in this research pass. Read-only relevance audit only.

---

## OPERATOR PROMPT (copy-paste)

```
You are reviewing whether PARKED local work is still relevant against the CURRENT
gxp codebase on main (https://github.com/TinkerandScribe/gxp).

Repo: clone or open TinkerandScribe/gxp at latest main.
Local stash (do NOT apply): park-unrelated-before-gxp-refine
  Inspect with: git stash show --stat "stash@{0}"
               git stash show -p "stash@{0}" -- <path>

Context already shipped (assume on main unless you find otherwise):
- PR #2 design brief gxp-refine
- PR #3 gxp-refine v0 (template, how-to, Cursor GXP_REFINE, selftest)
- PR #4 verify.sh wires eval-gxp-refine-selftest.sh
- PR #5 Claude/Grok GXP_REFINE + PowerShell backtick failure capture + CONTRIBUTING note

Your job: for EACH parked hunk/theme below, compare stash intent vs what main
already has. Classify every item as one of:
  KEEP   — still a real gap on main; worth a focused follow-up PR
  SUPERSEDED — main already covers the intent (cite paths/commits/PRs)
  PARTIAL — some of the intent landed; list residual delta only
  DROP   — obsolete, harmful, or would pollute (e.g. stale release bump,
           conflicting ratings line, PII already fixed differently)
  CONFLICT — applying would clash with post-stash main; note conflict files

Also answer: is a blind `stash pop` safe? (Expect: no.) Recommend a split plan
if anything is KEEP/PARTIAL.

=== PARKED THEMES (from stash@{0}, 11 files) ===

A) Release packaging — CHANGELOG.md + README.md
   Stash adds draft ## [1.3.1] notes and bumps README "Latest" 1.3.0 → 1.3.1.
   On main today: latest changelog section is still 1.3.0; README says v1.3.0.
   Check: which claimed 1.3.1 bullets are ALREADY true on main after PRs #3–#5
   (gxp-refine, selftest-in-verify, Claude/Grok surfaces, PS failure, skill-zip,
   Verification ladder, ratings hash fields, etc.)? Which bullets are still false?
   Verdict: KEEP new 1.3.1 release notes (rewrite against HEAD), SUPERSEDED, or DROP?

B) Cursor Verification ladder + ratings placement — rule.mdc, START_SESSION.md,
   TEST_PROMPT.md, Cursor README.md, sync/check-core.{sh,ps1}
   Stash encodes Verification ladder, full-vs-lightweight triggers, where-to-append
   ratings (.ai/ vs core/ratings.jsonl), expands TEST_PROMPT quiz, adds sync markers.
   On main: gxp-refine added START_SESSION "Not gxp-refine" disclaimer and GXP_REFINE.md;
   rule.mdc may or may not already mention Verification ladder / where-to-append.
   Diff carefully against HEAD. Do NOT weaken gates. Note conflicts with gxp-refine
   START_SESSION / README edits from PRs #3/#5.
   Verdict per file: KEEP / PARTIAL / SUPERSEDED / CONFLICT.

C) Cowork ratings-schema optional hash fields —
   adapters/cowork/plugin-src/skills/gxp-workflow/references/ratings-schema.md
   Stash documents optional prev_hash / entry_hash.
   Check whether core schema line / validators / other adapters already document this.
   Verdict: KEEP / SUPERSEDED / DROP.

D) Ratings ledger append — core/ratings.jsonl
   Stash adds one line: task review-gxp-orchestrator-system-prompt (rating 8).
   Check: is that task already on main? Would appending break optional hash-chain
   validate-ratings-chain.py expectations? Prefer re-append at HEAD with Python
   json.dumps if KEEP, never blind stash apply onto ratings.jsonl.
   Verdict: KEEP (re-append cleanly) / SUPERSEDED / DROP.

E) OPERATOR_RUNBOOK path hygiene —
   core/evals/golden/agent-code-quality/OPERATOR_RUNBOOK.md
   Stash replaces absolute C:\Users\Reepicheep\… DEST example with a relative
   placeholder. On main the absolute path may still be present (PII/local leak risk).
   Verdict: KEEP (high priority if path still present) / SUPERSEDED.

=== REQUIRED OUTPUT ===
1. Table: Theme | Classification | Evidence (paths / quotes) | Residual work if any
2. Blind pop safety: YES/NO + why
3. Recommended next PRs (0–3), each with 1-sentence goal and file list
4. Explicit "not relevant anymore" list
5. Confidence (high/medium/low) and what you did not check

Rules: read-only; no commits; no stash apply; no inventing files that are not in
stash or on main. Cite concrete paths.
```

---

## Ideal State Criteria (for the research run itself)

- [ ] Every stash theme A–E has a KEEP / SUPERSEDED / PARTIAL / DROP / CONFLICT label.
- [ ] Blind `stash pop` safety answered with evidence from current main.
- [ ] Residual work (if any) is split into ≤3 focused PR proposals — or “none”.
- [ ] Absolute-path runbook item called out if still present on main.
- [ ] No recommendation weakens `core/workflow.md` / `core/routing.md` gates.

## Verification (after research returns)

Operator (or implement agent) spot-checks 2–3 cited paths on main and confirms
classifications before any restore PR.

## Out of scope

- Applying the stash
- Shipping 1.3.1 tag/release
- New gxp-refine experiments

## Handoff notes

- Sync status at prompt authoring: local `main` fast-forwarded to match `origin/main`;
  feature PRs #2–#5 already merged/pushed; only remote-ahead item was chore sync markers.
- Stash remains local-only until deliberately restored.
