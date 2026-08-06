# Task brief — M6 campaign re-scope (operator decision)

**Date:** 2026-08-06  
**Task slug:** m6-campaign-rescope  
**Workflow:** full (decision + freeze only; no campaign runs in this brief)  
**Status:** PARKED (2026-08-06) — operator decision; no campaign freeze  
**Parent brief:** [`blind-multi-model-code-quality-campaign.md`](blind-multi-model-code-quality-campaign.md)  
**Scaffolding tier:** standard  

## Goal

Unblock Roadmap **M6** by freezing a campaign scope that can pass the pre-registered claim gate: **harder tasks + matched models across control/GXP**, with protocol and success rule written **before** any agent run.

## Why this exists

Prior desktop blinds **failed** the claim gate (ceiling and/or unmatched models).  
Marketing “GXP improves code quality” remains **forbidden** until a new campaign passes a frozen rule.  
M5 grew the task set (`04`–`05` done; hard pack `06`–`10` exists). Scope is now an **operator product decision**, not a tooling gap.

## Context (evidence, not re-litigation)

- Protocol base: `core/evals/golden/agent-code-quality/PROTOCOL.md`  
- Task packs: easy `01`–`05` (ceiling-prone); hard `06`–`08`; multi-file L2 `09`–`10`  
- Prior trials under `core/evals/golden/agent-code-quality/trials/` (operator-blind, matched-*, l2-*)  
- Claim gate: do not ship lift language without CAMPAIGN_REPORT + pre-registered pass  

## Ideal State Criteria (this decision ticket)

- [outcome] Operator records choices for **A–E** in the Decision section (or explicitly parks M6).  
- [outcome] Frozen scope is written into either this file’s “Frozen campaign card” or a dated `PROTOCOL_FROZEN.md` under a new `trials/<date>-…/` tree **before** first agent run.  
- [outcome] Matched-model rule is explicit: same model/tool identity on control and GXP for each paired cell.  
- [outcome] Task set is not majority easy/ceiling-prone (`01`–`05`) unless operator documents why and lowers the success delta.  
- [guardrail] No agent runs, no scoring, no marketing claims under this brief alone.  
- [guardrail] Methodology (`core/workflow.md`) is not changed to “win” the campaign.  
- [hypothesis] Default proposal below is the smallest honest next campaign.

## Out of scope

- Running the campaign (separate dispatch after freeze).  
- Changing hidden tests mid-design.  
- Building a multi-provider critic product.  
- v1.4.0 release/tag.  
- Promoting experimental clarification protocol.

## Verification plan (for the decision only)

- All A–E fields filled or M6 marked parked with reason.  
- Frozen card path named and exists before any score JSON for the new campaign.  
- Parent M6 brief status can flip from BLOCKED → ready once frozen card exists.

---

## Operator decision (fill in)

### A. Campaign shape (pick one)

| Option | Description | Recommend? |
|---|---|---|
| **A1** Matched multi-model × hard pack | ≥2 models, each runs control+GXP on tasks `06`,`07`,`08` (≥3 tasks) | **Yes — default** |
| **A2** Matched multi-model × L2 multi-file | ≥2 models, tasks `09` and/or `10` (public-green vs GXP) | If multi-file signal is the claim |
| **A3** Single matched model, multi-seed hard pack | 1 model, control vs GXP, ≥3 seeds × ≥3 hard tasks | Cheaper; weaker external validity |
| **A4** Park M6 | Leave scientific claim closed; invest in dogfood/ACP | Valid if proof is not the north-star |

**Operator choice:** **A4 — Park M6** (2026-08-06)

**Park reason:** Claim gate already failed on ceiling effects. Another campaign without named matched models and real operator energy is low-ROI and risks another unsatisfying result. Parking preserves scientific honesty. When un-parking, start from **A1 + C1** and name two matched surfaces first.

### B. Models / tools (list exact pairs)

Must be **matched** per cell (same model string / product surface for control and GXP).

| Slot | Control surface | GXP surface | Notes |
|---|---|---|---|
| Model 1 | — | — | n/a while parked |
| Model 2 | — | — | n/a while parked |

**Operator choice:** **n/a (parked)**

### C. Success rule (pick one; freeze before runs)

| Option | Rule | Recommend? |
|---|---|---|
| **C1** Mean lift | GXP mean correctness − control mean ≥ **0.10** across tasks | Same as parent brief example |
| **C2** Majority win | GXP wins task-level mean on **majority** of tasks; no GXP scope/tamper DQ | Good if variance is high |
| **C3** Custom | Write exact numeric rule here | Only if operator needs different bar |

**Operator choice:** **n/a (parked)** — preferred on un-park: **C1** on hard pack

### D. Budget / stop rules

- Max wall-clock or $ / session: **n/a (parked)**  
- Max retries per trial: **n/a (parked)** (suggest 0 for blind purity when un-parked)  
- Peeking at `hidden_tests/` or `reference/`: **forbidden** (unchanged)

### E. Contamination owner

Who may see hidden tests / score mid-campaign?  
**Operator names:** **n/a (parked)**

---

## Frozen campaign card (fill after A–E; then this brief is done)

```text
Campaign id:     (none — M6 parked 2026-08-06)
Shape:           A4 park
Models:          n/a
Tasks:           n/a
Success rule:    n/a (on un-park prefer C1 + A1 hard pack)
Budget/stops:    n/a
Contamination:   n/a
Protocol path:   n/a
Status:          PARKED
```

## Default proposal (if operator wants a ready-made card)

- **Shape A1:** models = (operator names two matched surfaces); tasks = `06-lru-ttl`, `07-deep-merge`, `08-line-chunker`  
- **Success C1:** mean GXP − mean control ≥ 0.10  
- **Retries:** 0 for implementation arms after first score-eligible tree  
- **No** easy tasks in the primary matrix (optional canary `04` or `05` excluded from claim mean)  
- **Next action after freeze:** dispatch per `OPERATOR_RUNBOOK.md` + parent brief checklist — not this file

## Handoff

**2026-08-06:** Operator chose **A4 park**. Decision criteria satisfied (park with reason). No frozen campaign card; no runs. Parent M6 brief remains BLOCKED until un-park + A–E freeze. To resume: reply with `A1, models X+Y, C1` (or full A–E) and re-open this brief.
