# Canary artifact — AFTER (current / v1.2.0+ Claude workflow constraints)

**Workflow source:** `adapters/claude/ai-workflow/instructions/workflow.md` @ HEAD  
**Constraint note:** Phase 8 Handoff required; ratings fields `ts`, `criteria_met`,
`criteria_total`, `rating` required; structural floor + live sync markers enforced
by check-core / CI.

## Task

Add one sentence to CONTRIBUTING.md under “Before you open a PR” reminding
contributors that adapter workflow drift is now structurally checked.

## Task brief (produced under after-constraints)

### Goal

Document structural drift checking so PR authors know verify/CI will fail on
Phase/structure regressions, not only missing files.

### Ideal State Criteria

1. CONTRIBUTING “Before you open a PR” states that adapter `workflow.md` drift is
   **structurally** checked (phases / criteria markers), not only file presence.  
2. Mentions `bash scripts/verify.sh` (and that CI runs it on PRs, if accurate at HEAD).  
3. Diff is one short sentence (or ≤2 lines).  
4. `bash scripts/verify.sh` exits 0 after the edit.  
5. No secrets or project-specific paths introduced.  
6. Handoff lists what changed / verified / parked.

### Out of scope

- Changing check-core implementations.  
- Editing ROADMAP or CHANGELOG.  
- Multi-paragraph CONTRIBUTING rewrite.

### Verification plan

1. Deterministic: `bash scripts/verify.sh` → exit 0.  
2. Deterministic: `rg -n "structur" CONTRIBUTING.md` (or equivalent) hits the new line.  
3. Subjective: sentence is accurate for HEAD tooling.

### Model

Claude-optimized GXP v1.1 + v1.2.0 enforcement (Phase 8 + ratings schema).

## Phase 8 — Handoff (required after)

- **Changed:** (simulated) one sentence under CONTRIBUTING “Before you open a PR”.  
- **Verified:** `bash scripts/verify.sh` exit 0; line present in file.  
- **Not done / parked:** none for this canary.  
- **Approval gates:** none.  
- **Dead ends:** none.  
- **Rating:** append JSON line with fields `ts`, `criteria_met`, `criteria_total`,
  `rating` (1–10) to the appropriate `ratings.jsonl`.  
- **Failures:** none.

## Ratings reminder

```json
{"ts":"<ISO-8601>","task":"canary-contributing-structural-drift","brief":"core/evals/canaries/gxp-version-comparison/after/canary-brief-only.md","criteria_met":6,"criteria_total":6,"rating":8,"mode":"lightweight"}
```
