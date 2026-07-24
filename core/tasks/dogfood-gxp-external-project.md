# Task brief — dogfood GXP on an external project (Roadmap M7.1)

**Status:** DONE (2026-07-24)  
**Host:** operator-named private Flask business-management app  
**Retrospective:** [`core/evals/dogfood-m7-external-host-2026-07-24.md`](../evals/dogfood-m7-external-host-2026-07-24.md)  
**Workflow:** full (on the host repo; closed from existing host evidence + public retrospective)

## Goal

Run at least one non-trivial real feature/fix through full GXP **outside** the
gxp package repo, to test usefulness (not hidden-test science).

## Context

- Install via `scripts/install-ai-from-core.sh` / `.ps1` into the host.  
- Ratings and failures for the host stay in the host’s `.ai/` (live-for-fork-work).  
- Optional: short retrospective note in gxp `core/evals/` or a private log — no
  host secrets in the public gxp repo.

## Ideal State Criteria

- [x] 1. Host repo has `.ai/workflow.md` (or equivalent) installed and
  `PROGRAM.md` filled with real verify commands.  
- [x] 2. One task brief with 4–8 binary ISC completed under host `.ai/tasks/`.  
- [x] 3. Implementation merged or PR’d on host; deterministic host verify ran first.  
- [x] 4. One rating line in host `.ai/ratings.jsonl`.  
- [x] 5. Retrospective (≤1 page) answers: what GXP helped, what hurt, one change
  proposal for gxp core/adapters — **no host secrets**.  
- [x] 6. If retrospective is committed to gxp public tree, path is under
  `core/evals/` or `core/tasks/` and rule 01/02 clean.

## Out of scope

- Rewriting gxp methodology mid-dogfood unless a failure capture demands it.  
- Multi-model science campaign (M6).

## Verification plan

Host tests/linters green; brief/rating present; retrospective reviewed for secrets.

## Approval gates

- Operator must name the host project before implementation starts. **Named 2026-07-24.**

## Close-out (2026-07-24)

Host already had multi-cycle GXP use (full + lightweight), deterministic verify
floor, and eleven host rating lines. Public work product is the sanitized
retrospective only. ROADMAP M7 marked **done**. Follow-up proposal (refresh
workflow-only recipe + ratings field migration note) is backlog, not required
to close M7.
