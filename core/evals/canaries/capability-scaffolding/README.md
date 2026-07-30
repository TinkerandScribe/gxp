# Canary — capability scaffolding tiers

**Purpose:** Same task brief, two scaffolding tiers — confirm frontier does not
drop verification invariants and constrained does not invent a second workflow.

## Setup

1. Pick a **fixed** multi-file but reversible task in a throwaway branch.
2. Write one task brief with 4–8 binding Ideal State Criteria and a strong
   deterministic verification plan.
3. Run twice (new sessions), changing only:
   - `Scaffolding tier: frontier`
   - `Scaffolding tier: constrained`
4. Keep model constant when possible (or record both model and tier).

## Score (binary)

For each run:

- [ ] Binding criteria still required and checked (no tier skipped Phase 5)
- [ ] Anti-loop still applied if failures occurred
- [ ] Rating line appended with `notes` mentioning scaffolding tier
- [ ] No silent deletion of host CLAUDE.md / skills / hooks
- [ ] Frontier run used higher-level brief style OR explicitly noted why not
- [ ] Constrained run used denser steps/gates OR explicitly noted why not

## Pass bar (v1)

- Both runs meet the same binding criteria set (or document criterion failure
  as a model capability issue, not a tier license to skip checks).
- No invariant violation on frontier.
- `bash scripts/verify.sh` remains green on the methodology repo after any
  scaffolding doc edits.

## Artifacts

Store transcripts/ratings under local-only trial paths if needed
(`core/evals/**/trials/` is local-only per project rules). Do not commit
raw trial dumps to the public ledger unless deliberately curated.
