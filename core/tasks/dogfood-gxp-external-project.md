# Task brief — dogfood GXP on an external project (Roadmap M7.1)

**Status:** draft — ready for pickup  
**Depends on:** operator names a **host repo** path/URL  
**Workflow:** full (on the host repo)

## Goal

Run at least one non-trivial real feature/fix through full GXP **outside** the
gxp package repo, to test usefulness (not hidden-test science).

## Context

- Install via `scripts/install-ai-from-core.sh` / `.ps1` into the host.  
- Ratings and failures for the host stay in the host’s `.ai/` (live-for-fork-work).  
- Optional: short retrospective note in gxp `core/evals/` or a private log — no
  host secrets in the public gxp repo.

## Ideal State Criteria

- [ ] 1. Host repo has `.ai/workflow.md` (or equivalent) installed and
  `PROGRAM.md` filled with real verify commands.  
- [ ] 2. One task brief with 4–8 binary ISC completed under host `.ai/tasks/`.  
- [ ] 3. Implementation merged or PR’d on host; deterministic host verify ran first.  
- [ ] 4. One rating line in host `.ai/ratings.jsonl`.  
- [ ] 5. Retrospective (≤1 page) answers: what GXP helped, what hurt, one change
  proposal for gxp core/adapters — **no host secrets**.  
- [ ] 6. If retrospective is committed to gxp public tree, path is under
  `core/evals/` or `core/tasks/` and rule 01/02 clean.

## Out of scope

- Rewriting gxp methodology mid-dogfood unless a failure capture demands it.  
- Multi-model science campaign (M6).

## Verification plan

Host tests/linters green; brief/rating present; retrospective reviewed for secrets.

## Approval gates

- Operator must name the host project before implementation starts.
