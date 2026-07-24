# EXAMPLE gxp-refine run (dry-run only)

**Status:** EXAMPLE — fictional weakness; **no real core edit**.  
**Mode:** `gxp-refine` — **operator-invoked only**  
**Date:** 2026-07-23  
**Run slug:** EXAMPLE-gxp-refine-run

Copied from [`core/templates/gxp-refine-run.md`](../templates/gxp-refine-run.md).
Design: [`core/tasks/gxp-refine-design.md`](gxp-refine-design.md).

**Mutation budget = 1.** **No auto-apply / no auto-merge.**

---

## 0. Invocation check

- [x] Operator explicitly requested `gxp-refine` (example session).
- [x] Not framed as `gxp-rsi` / `gxp-auto`.

---

## 1. Evidence skim

### Exists now (observed)

- Ratings: several notes that thin smoke `verify.sh` exit 0 was treated as done (see workflow Verification ladder).
- Failures: `core/failures/verification-wrapper-swallows-exit-codes.md` (related class: silent pass).
- Eval / verify signals: `bash scripts/verify.sh` is adapter parity only.

### Proposed

- None in this dry-run.

---

## 2. One weakness

**Weakness:** Operators sometimes confuse weekly refine calendar skim with eval-gated refinement.

**Evidence:** `core/templates/weekly-refine.md` has no GATE 1/GATE 2; design brief distinguishes the modes.

---

## 3. One hypothesis

**Hypothesis:** A dedicated run template with explicit GATE 1 / GATE 2 headings reduces accidental batching of multiple methodology tweaks.

---

## 4. One target

**Target path:** `core/templates/gxp-refine-run.md` (already the v0 ship — this EXAMPLE does not edit it again).

**Risk tier:** 2 — templates.

**Hard-prohibit check:** [x] passed (example proposes no gate weakening).

---

## 5. One eval plan

| Field | Value |
|---|---|
| Pinned baseline SHA and/or tag | *(example)* `ad72c9f` design merge |
| Fixed corpus | `bash scripts/verify.sh`; `bash scripts/eval-gxp-refine-selftest.sh` |
| Primary metric | selftest exit 0 and required markers present |
| Regression set | `bash scripts/verify.sh` exit 0 |
| Repeated trials | n/a (deterministic) |
| Evaluator independence | example does not change the selftest in the same fictional promote |

---

## GATE 1 — Experiment approve

- **Operator decision:** defer *(EXAMPLE — do not treat as real approve)*
- **Notes:** Dry-run stops here for documentation.

---

## 6–8. Baseline / candidate / recommendation

Skipped in EXAMPLE (no candidate mutation).

---

## GATE 2 — Promotion approve

- **Operator decision:** defer *(EXAMPLE)*
- **Notes:** **No auto-apply. No auto-merge.**

---

## Handoff

- What was proposed: distinguish weekly refine vs gxp-refine via template markers.
- What was measured: n/a (dry-run).
- Parked: live refine targeting `core/workflow.md` wording (tier 4 — needs elevated stakes).
