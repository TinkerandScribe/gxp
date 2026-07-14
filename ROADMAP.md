# Roadmap

## Part A — Verification hardening (complete)

Sequenced plan from the 2026-07 external audit and GXP review
(`core/tasks/review-external-audit-fix-plan.md`). **All milestones below are done.**

Ordering corrections that shaped delivery (kept for history):

1. **P0-2 before P0-1’s negative test** — whole-file workflow allowlist made the CI
   negative test dead until the structural floor landed.  
2. **Grok def-order before P0-3** — real SHA markers would crash under `set -u`.  
3. **Bold marker regex** — `core:** <sha>` must match, not only `core: <sha>`.

### Milestone 0 — unblockers (v1.1.3)

| Item | Status |
|---|---|
| Grok sync-check def-order fix | **done** |
| GxP naming disclaimer in README | **done** |
| Roadmap + P0 briefs | **done** |

### Milestone 1 — make drift checkable (v1.2.0)

| Item | Brief | Status |
|---|---|---|
| Structural floor / real sync checks (P0-2 + P1-4) | [`real-diff-sync-checks.md`](core/tasks/real-diff-sync-checks.md) | **done** |
| CI verify workflow (P0-1) | [`ci-verify-workflow.md`](core/tasks/ci-verify-workflow.md) | **done** |
| Staleness markers real SHA (P0-3) | [`staleness-marker-real-sha.md`](core/tasks/staleness-marker-real-sha.md) | **done** |

### Milestone 2 — narrative gap (v1.2.x)

| Item | Status |
|---|---|
| Installer subshell counter (P1-2) | **done** |
| Installer dry-run / docs (P1-3 / P2-5) | **done** |
| Workshop-template quarantine (P2-2) | **n/a** (not in tree) |
| Optional ratings hash-chain fields (P1-1 ledger) | **done** (partial: opt-in fields + validator) |
| Routing critic language (P1-1 critic) | **done** (descope: recommended-not-shipped) |

### Milestone 3 — positioning & ergonomics (v1.3.0)

| Item | Status |
|---|---|
| Eval fixtures (P2-1) + code-quality harness | **done** |
| Doc dedup hybrid generator (P2-4) | **done** — `scripts/generate-adapter-workflows.py` + deltas |
| Installer dry-run / non-force README | **done** |

### Deliberately not adopted (still)

- Second-model critic as a **required** subsystem.  
- Audit order P0-1 before P0-2.

---

## Part B — Next plan (post-hardening)

**Review:** [`core/tasks/review-post-hardening-and-roadmap.md`](core/tasks/review-post-hardening-and-roadmap.md)

**North star options (pick by operator goal):**

| Goal | Prioritize |
|---|---|
| Prove GXP improves *code* outcomes | M5 then M6 |
| Make the repo nicer to maintain | M4 then stop or M5 |
| Get value from GXP on real work | M7 (can run in parallel with M4) |

### Recommended default sequence

**M4 → M5 → M6**, with **M7 parallel** if a host project is ready; **M8 deferred**.

### Milestone 4 — tooling polish (small, first)

| Order | Item | Brief | Status |
|---|---|---|---|
| 1 | Shared Python discovery helper for bash scripts | [`shared-find-python.md`](core/tasks/shared-find-python.md) | **done** — `scripts/lib/find-python.sh` |
| 2 | Core prose `4 to 8` → `4–8`; drop generator floor inject | [`core-four-eight-prose.md`](core/tasks/core-four-eight-prose.md) | **done** |

### Milestone 5 — deepen the code-quality eval

| Order | Item | Brief | Status |
|---|---|---|---|
| 1 | Grow frozen task set (harder, less ceiling) | [`grow-code-quality-eval-tasks.md`](core/tasks/grow-code-quality-eval-tasks.md) | **done** — tasks `04-safe-join`, `05-count-words` |

**Why before multi-model:** multi-seed campaign showed control often near-perfect on
easy tasks; more tasks improve statistical and ecological validity of later runs.

### Milestone 6 — evidence (the open scientific question)

| Order | Item | Brief | Depends on |
|---|---|---|---|
| 1 | Blind multi-model control vs GXP campaign | [`blind-multi-model-code-quality-campaign.md`](core/tasks/blind-multi-model-code-quality-campaign.md) | M5 recommended; harness multi-runner selftest done |

**Why this is the real “prove it” item:** prior campaigns used fixture authors or
incomplete one-shot seeds. This requires **independent agents** that did not write
hidden tests, with frozen prompts and score-only operator.

**Claim gate:** do not market “GXP makes agents write better code” until this (or
equivalent) passes pre-registered success criteria in its brief.

### Milestone 7 — product dogfood (parallel track)

| Order | Item | Brief | Depends on |
|---|---|---|---|
| 1 | Dogfood GXP on an external host project | [`dogfood-gxp-external-project.md`](core/tasks/dogfood-gxp-external-project.md) | operator names a repo |

**Why parallel:** does not improve the methodology package’s scientific claims, but
is the best test of *usefulness*. Should not steal focus from M6 if the goal is proof.

### Milestone 8 — optional / deferred

| Item | Brief | When |
|---|---|---|
| Put Cursor `rule.mdc` on the generator | [`cursor-workflow-on-generator.md`](core/tasks/cursor-workflow-on-generator.md) | After M4–M5 stable; high risk (Phase -1 / rule shape) |

### Explicitly still out

- Shipping a multi-provider critic product.  
- Re-opening whole-file workflow allowlists.  
- Tag/release automation without operator request.

---

## How to use this roadmap

1. Operator picks a milestone (default: **M4** if unsure).  
2. Open the linked brief; refine Ideal State Criteria at pickup if needed.  
3. Run full GXP on that brief only — no silent scope expansion.  
4. Update this file’s status when an item lands (**done** / **partial** / **dropped**).
