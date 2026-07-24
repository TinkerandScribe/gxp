# gxp-refine run

**Mode:** `gxp-refine` — **operator-invoked only**
**Date:** 2026-07-23
**Run slug:** 2026-07-23-wire-refine-selftest-into-verify
**Operator:** approved GATE 1 verbally (`approve`)

> Live dogfood run after `gxp-refine` v0 merge. Operator said **run gxp-refine**.

**Mutation budget = 1** — exactly one weakness, one hypothesis, one logical change,
one named target path, one eval plan. Park everything else.

**No auto-apply / no auto-merge.** Dual gates below are mandatory and fail-closed.

Design canon: [`core/tasks/gxp-refine-design.md`](gxp-refine-design.md)
Operator how-to: [`core/docs/gxp-refine.md`](../docs/gxp-refine.md)

---

## 0. Invocation check

- [x] Operator explicitly requested `gxp-refine` (message: `run gxp-refine`).
- [x] This run will **not** rename/frame the mode as `gxp-rsi` or `gxp-auto`.

---

## 1. Evidence skim

### Exists now (observed)

- Ratings:
  - `2026-07-02` fix-verification-tooling (rating 9): verify must actually gate
    (`core/failures/verification-wrapper-swallows-exit-codes.md`).
  - `2026-07-23` gxp-refine-implement (rating 8): selftest shipped separately from verify.
- Failures:
  - `core/failures/verification-wrapper-swallows-exit-codes.md`
- Eval / verify signals:
  - `.github/workflows/verify.yml` runs `bash scripts/verify.sh` only.
  - Pre-candidate `scripts/verify.sh` did not call `eval-gxp-refine-selftest.sh`.

### Proposed

- Wire selftest into verify.sh (this experiment).

---

## 2. One weakness

**Weakness:** Default CI/`verify.sh` did not run `eval-gxp-refine-selftest.sh`, so refine
markers could regress silently.

**Evidence:** `scripts/verify.sh` pre-candidate; CI workflow; rating 2026-07-23 implement.

---

## 3. One hypothesis

**Hypothesis:** Invoking the existing selftest from verify.sh (propagate non-zero into
`fail`) closes the gap without changing marker definitions.

---

## 4. One target

**Target path:** `scripts/verify.sh`

**Risk tier:** tooling / verify harness (not routing/core methodology).

- [x] Hard-prohibit check passed

---

## 5. One eval plan

| Field | Value |
|---|---|
| Pinned baseline SHA and/or tag | `85d188acb25ac08c8fddbe506bec50665b278867` |
| Fixed corpus | (A) `bash scripts/verify.sh`; (B) `bash scripts/eval-gxp-refine-selftest.sh`; (C) strip `GATE 1` from template → verify → restore |
| Primary metric | Candidate: clean verify=0 AND negative probe verify≠0. Baseline: clean=0 AND negative still=0 (gap). |
| Regression set | clean-tree verify=0; adapter sync still pass; selftest script unchanged |
| Repeated trials | n/a |
| Evaluator independence | only `scripts/verify.sh` edited |

---

## GATE 1 — Experiment approve (operator)

- **Operator decision:** approve
- **Signed by / date:** operator chat reply `approve` — 2026-07-23
- **Notes:** Proceed to baseline + candidate.

---

## 6. Baseline results (after GATE 1)

| Check | Result |
|---|---|
| Primary metric | Gap confirmed: clean verify **0**; strip GATE 1 → verify still **0** |
| Regression set | clean verify **0**; selftest alone **0** |
| Commands / artifact paths | `bash scripts/verify.sh` → 0; `bash scripts/eval-gxp-refine-selftest.sh` → 0; Python negative probe restored template |

---

## 7. Candidate (one logical change only)

**Change summary:** Add verify.sh step 4: if `scripts/eval-gxp-refine-selftest.sh`
exists, run it and set `fail=1` on non-zero (same pattern as adapter sync). Update
final PASS/FAIL banners accordingly.

**Files touched:** `scripts/verify.sh` only

| Check | Result |
|---|---|
| Primary metric | **met** — clean verify **0**; strip GATE 1 → verify **1** (selftest FAIL propagates) |
| Regression set | **held** — clean verify **0**; adapter sync still PASS; selftest script not modified |
| Commands / artifact paths | candidate clean `bash scripts/verify.sh` → 0; negative probe → 1; template restored |

---

## 8. Recommendation

- **Verdict:** **promote**
- **Rationale (capability vs regression):** Primary metric improved (marker removal now
  fails verify/CI path). Regression set held on clean tree. No gate/rail language changes.

---

## GATE 2 — Promotion approve (operator)

Separate from GATE 1. Required before any merge or apply of the candidate.

- **Operator decision:** promote
- **Signed by / date:** operator chat reply `promote` — 2026-07-23
- **Notes:** Promotion authorized. Ship `scripts/verify.sh` + this run record via PR and merge.

---

## Handoff

- What was proposed: wire gxp-refine selftest into `scripts/verify.sh`.
- What was measured: baseline gap (neg verify 0) → candidate catch (neg verify 1); clean 0→0.
- Parked weaknesses:
  - Claude/Grok skill ports of gxp-refine
  - CONTRIBUTING.md selftest mention (likely redundant after promote)
  - PowerShell backtick-eating failure capture
  - Ratings hash-chain backfill
- Rating line reference: `core/ratings.jsonl` task `gxp-refine-wire-selftest-into-verify` (2026-07-23)
