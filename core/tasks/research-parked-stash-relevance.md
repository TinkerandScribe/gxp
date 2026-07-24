# Research prompt — parked stash relevance vs current `main`

**Date:** 2026-07-24  
**Task slug:** research-parked-stash-relevance  
**Status:** done — executed 2026-07-24; follow-ups #7 + release-notes triage  
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

- [x] Every stash theme A–E has a KEEP / SUPERSEDED / PARTIAL / DROP / CONFLICT label.
- [x] Blind `stash pop` safety answered with evidence from current main.
- [x] Residual work (if any) is split into ≤3 focused PR proposals — or “none”.
- [x] Absolute-path runbook item called out if still present on main.
- [x] No recommendation weakens `core/workflow.md` / `core/routing.md` gates.

## Verification (after research returns)

Operator (or implement agent) spot-checks 2–3 cited paths on main and confirms
classifications before any restore PR.

## Out of scope

- Applying the stash
- Shipping 1.3.1 tag/release
- New gxp-refine experiments



---

## RESEARCH RESULTS (2026-07-24, main `4202a4c`)

Read-only audit of `stash@{0}` / W=`3f03726` vs base `ad72c9f` vs HEAD. **No stash apply.**

### 1. Classification table

| Theme | Classification | Evidence | Residual |
|---|---|---|---|
| A Release packaging (CHANGELOG/README 1.3.1) | **PARTIAL → KEEP rewrite** | HEAD still shows `## [1.3.0]` and README Latest **v1.3.0**. Stash draft claims skill-zip tracked source (`adapters/claude/skill-src/`, `scripts/build-skill-zip.sh`) — **absent on HEAD**. Verification ladder **is** in `core/workflow.md`; evals/trials + `_grok_fill/` gitignored; Grok productization commits exist but are not narrated in CHANGELOG post-1.3.0; runbook path fix **not** on HEAD. | Rewrite 1.3.1 notes against HEAD only (no blind stash); do **not** claim untracked skill-zip builder; tag/release remains operator-gated. |
| B Cursor ladder / ratings placement | **KEEP** (+ **CONFLICT** on START_SESSION) | `rule.mdc` lacks Verification ladder + where-to-append; full/lightweight triggers weaker than stash. `TEST_PROMPT.md` still 10 Qs. Cursor README lacks ladder bullets. sync `check-core.{sh,ps1}` lack ladder markers. HEAD `START_SESSION.md` has post-stash **Not gxp-refine** section (PRs #3/#5) that stash tip omits — blind apply would drop it. | Port stash intent into rule/TEST/README/sync; merge START_SESSION (ladder text + keep Not gxp-refine). |
| C Cowork ratings-schema hash fields | **KEEP** | `adapters/cowork/.../ratings-schema.md` optional table ends at `failure_ref`; no `prev_hash`/`entry_hash`. Core schema line + `scripts/validate-ratings-chain.py` already define the chain. | Add two optional-field rows (stash hunk is correct). |
| D ratings.jsonl orchestrator line | **DROP** | Stash adds `review-gxp-orchestrator-system-prompt` rating. Brief path **missing** on HEAD; task absent from ledger. Blind apply would collide with post-stash chained lines (`gxp-refine-*`). | Do not re-append orphan rating without public brief + clean chain re-anchor. |
| E OPERATOR_RUNBOOK absolute path | **KEEP (high)** | Line still has `C:\Users\Reepicheep\Claude\gxp-public\...` DEST example. | Relativize to `<repo>\...\trials\<date>-operator-blind\...` (rule-02 class). |

### 2. Blind `stash pop` safety

**NO.** Evidence: (1) `START_SESSION.md` diverged (gxp-refine disclaimer on HEAD); (2) `core/ratings.jsonl` grew chained refine ratings after stash base — applying stash tip would fight tip/history; (3) CHANGELOG 1.3.1 draft asserts skill-zip builder files that are not on HEAD; (4) multi-file Cursor content needs merge not replace.

### 3. Recommended next PRs (≤3)

1. **restore-parked-hygiene-cursor** — E + C + B (runbook path, cowork schema rows, Cursor ladder/placement + sync markers; preserve Not gxp-refine). Files: `OPERATOR_RUNBOOK.md`, `ratings-schema.md`, `rule.mdc`, `START_SESSION.md`, `TEST_PROMPT.md`, Cursor `README.md`, `sync/check-core.{sh,ps1}`.
2. **release-notes-1.3.1-rewrite** — rewrite CHANGELOG/README Latest against HEAD truths only; **no tag** until operator asks. Files: `CHANGELOG.md`, `README.md`.
3. *(none third)* — D dropped; skill-zip builder remains out of scope unless separately briefed.

### 4. Not relevant anymore

- Blind restore of stash ratings.jsonl line (D).
- Stash 1.3.1 bullet claiming tracked skill-zip builder / `build-skill-zip.sh` (not on tree).
- Any change that weakens `core/workflow.md` Verification ladder or `core/routing.md` rails (none proposed).

### 5. Confidence

**High** for E/C/B/D and blind-pop=NO (paths read + diffs vs SHAs). **Medium** for A release narrative (skill-zip may exist only as GitHub release asset, not source tree — not fully audited release assets). Not checked: GitHub release asset contents vs changelog claims; non-public local copies of orchestrator brief.

### Spot-check notes (operator)

- `OPERATOR_RUNBOOK.md` absolute path: confirmed present.
- `rule.mdc`: no "Verification ladder" string.
- `ratings-schema.md`: no prev_hash/entry_hash rows.

## Handoff notes

- Research executed 2026-07-24 on main `4202a4c` (post PR #6). Stash left parked (no pop).
- Follow-up briefs: `core/tasks/restore-parked-hygiene-cursor.md` (implement this tick if bounded);
  `core/tasks/release-notes-1.3.1-rewrite.md` (parked — no tag without operator).
- Sync status at prompt authoring: local `main` matched `origin/main` through PR #5; PR #6 shipped this prompt.

## CLOSED

Research complete; implement follow-ups handled. Stash residual superseded by #7 + 1.3.1 rewrite; DROP rating not restored.
