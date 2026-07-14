# Task brief — grow code-quality eval task set (Roadmap M5.1)

**Status:** draft — ready for pickup  
**Depends on:** harness + selftest (done)  
**Blocks:** recommended before
[`blind-multi-model-code-quality-campaign.md`](blind-multi-model-code-quality-campaign.md)  
**Workflow:** full

## Goal

Add frozen coding tasks so control arms no longer hit a correctness ceiling as
often, and multi-model campaigns cover more failure modes.

## Context

- Today: `01-parse-kv`, `02-slugify`, `03-merge-intervals`.  
- Multi-seed incomplete controls still average ~0.7; some seeds ≥0.9.  
- Need tasks where partial implementations systematically fail more tests.

## Ideal State Criteria

- [ ] 1. At least **+2** new tasks under
  `core/evals/golden/agent-code-quality/tasks/` with
  `prompt.md`, `starter/`, `reference/`, `hidden_tests/`, `meta.json`.  
- [ ] 2. Each new task: reference scores **1.0**; starter scores **≤0.5** correctness.  
- [ ] 3. `scripts/eval-agent-code-quality-selftest.sh` covers all tasks (or a clear
  list update) and exits 0.  
- [ ] 4. `scripts/run-code-quality-seeds.py` extended with ≥2 control seeds per new
  task OR documented why seeds are deferred.  
- [ ] 5. Stdlib only; no network; no secrets.  
- [ ] 6. `bash scripts/verify.sh` exit 0.  
- [ ] 7. Short note in `agent-code-quality/README.md` listing new tasks.

## Out of scope

- Running the blind multi-model campaign (separate brief).  
- Non-Python tasks (unless explicitly chosen and scored automatically).

## Verification plan

Selftest; score starter/reference per task; run multi-seed if extended; verify.sh.

## Suggested task themes (non-binding)

- Path normalization / traversal rejection  
- Idempotent config merge with conflict rules  
- Small stateful CLI with exit codes  
