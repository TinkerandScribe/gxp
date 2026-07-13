# Canary artifact — BEFORE (v1.1.3 Claude workflow constraints)

**Workflow source:** `git show v1.1.3:adapters/claude/ai-workflow/instructions/workflow.md`  
**Constraint note:** v1.1.3 Claude workflow has Phases 0–7 (no Phase 8), no required
ratings field names, and check-core allowlists whole-file Workflow Definition.

## Task

Add one sentence to CONTRIBUTING.md under “Before you open a PR” reminding
contributors that adapter workflow drift is now structurally checked.

## Task brief (produced under before-constraints)

### Goal

Document that adapter drift is checked so contributors run the right verify step.

### Ideal State Criteria

1. CONTRIBUTING “Before you open a PR” mentions adapter sync / drift checking.  
2. Wording does not claim CI exists if the tag does not ship CI.  
3. Diff is one short sentence (or ≤2 lines).  
4. `bash scripts/verify.sh` still passes after the docs edit.

### Out of scope

- Changing adapters or check-core scripts.  
- Adding GitHub Actions.  
- Rewriting the whole CONTRIBUTING guide.

### Verification plan

1. Read the new sentence in context.  
2. Run `bash scripts/verify.sh` and record exit code.

### Model

Claude-optimized GXP v1.1.3-era workflow (no Phase 8 required).

## Simulated “done” notes (before-style)

Changed CONTRIBUTING.md with one reminder sentence. Verified by reading the file
and running verify.sh (exit 0). Rating: would append a 1–10 score to ratings.jsonl.

*(No separate Handoff phase in v1.1.3 Claude workflow — stop after failure capture /
final reminder sections.)*
