# gxp-refine run

**Mode:** `gxp-refine` — **operator-invoked only**
**Date:**
**Run slug:**
**Operator:**

> Copy this template into `core/tasks/<slug>-gxp-refine-run.md` (or `.ai/tasks/` in an
> installed project). Do **not** enter this mode from an ordinary GXP implement session,
> weekly refine skim, or rating append. Start only when the operator explicitly says
> **gxp-refine** / **run gxp-refine**.

**Mutation budget = 1** — exactly one weakness, one hypothesis, one logical change,
one named target path, one eval plan. Park everything else.

**No auto-apply / no auto-merge.** Dual gates below are mandatory and fail-closed.

Design canon: [`core/tasks/gxp-refine-design.md`](../tasks/gxp-refine-design.md)
Operator how-to: [`core/docs/gxp-refine.md`](../docs/gxp-refine.md)

---

## 0. Invocation check

- [ ] Operator explicitly requested `gxp-refine` (not implied by ordinary START / implement).
- [ ] This run will **not** rename/frame the mode as `gxp-rsi` or `gxp-auto`.

If either box is unchecked → **abort** (success: fail-closed).

---

## 1. Evidence skim

Label every bullet **observed** or **proposed**.

### Exists now (observed)

- Ratings:
- Failures / dead ends:
- Eval / verify signals:
- Other:

### Proposed (not yet in tree / not yet approved)

-

---

## 2. One weakness (budget slot)

**Weakness (one sentence):**

**Evidence pointers (paths / lines / rating ts):**

---

## 3. One hypothesis (budget slot)

**Hypothesis (causal / fixability claim):**

---

## 4. One target (budget slot)

**Target path (one named artifact):**

**Risk tier (1 adapter / 2 templates-rules-evals / 3 routing / 4 core methodology):**

**Hard-prohibit check:** this candidate must **not** weaken approval gates, privacy/stakes
rails, Verification ladder, anti-loop, or L3/L4 bounded-autonomy language.

- [ ] Hard-prohibit check passed (or abort)

---

## 5. One eval plan (budget slot) — preregister before edits

| Field | Value |
|---|---|
| Pinned baseline SHA and/or tag | |
| Fixed corpus (named scripts / docs / task IDs) | |
| Primary metric (one success rule) | |
| Regression set (must hold ~100%) | at minimum: `bash scripts/verify.sh` exit 0 |
| Repeated trials if stochastic (N) | N= / n/a |
| Evaluator independence | target change must **not** also change harness/metric/corpus |

---

## GATE 1 — Experiment approve (operator)

Operator must approve weakness + hypothesis + target + eval plan **before** any
candidate edits.

- **Operator decision:** approve / reject / defer
- **Signed by / date:**
- **Notes:**

If not approved → **stop**. Do not edit the target. (Abort without GATE 1 is success.)

---

## 6. Baseline results (after GATE 1)

Run the fixed corpus on the pinned baseline. Keep raw outputs.

| Check | Result |
|---|---|
| Primary metric | |
| Regression set | |
| Commands / artifact paths | |

---

## 7. Candidate (one logical change only)

Describe the single edit intent. Prefer a single file.

**Change summary:**

**Files touched:**

Then evaluate the **same** corpus on the candidate. Keep raw outputs — including
unfavorable ones.

| Check | Result |
|---|---|
| Primary metric | |
| Regression set | |
| Commands / artifact paths | |

---

## 8. Recommendation

- **Verdict:** promote / reject / inconclusive
- **Rationale (capability vs regression):**
  A capability win that breaks the regression set is a **reject**.

---

## GATE 2 — Promotion approve (operator)

Separate from GATE 1. Required before any merge or apply of the candidate.

- **Operator decision:** promote / reject / defer
- **Signed by / date:**
- **Notes:**

**No auto-apply. No auto-merge.** Apply only if GATE 2 is an explicit promote.

---

## Handoff

- What was proposed:
- What was measured:
- Parked weaknesses (budget overflow):
- Rating line reference (if this refine run is rated):
