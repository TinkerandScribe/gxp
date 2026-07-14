# Task brief — core “4–8” prose + drop generator inject (Roadmap M4.2)

**Status:** done  
**Depends on:** generator present (done); ideally after or with
[`shared-find-python.md`](shared-find-python.md)  
**Workflow:** full (touches core + regen)

## Goal

Make `core/workflow.md` use a structural-floor-friendly **4–8** token so generated
adapters no longer need a special “Adapter floor” inject line.

## Context

- Structural floor regex: `4[^[:alnum:]]+8` (matches `4-8`, `4–8`, not `4 to 8`).  
- Generator injects a floor line under Phase 1 today (`generate-adapter-workflows.py`).  
- Core is the source of truth — wording should be canonical there.

## Ideal State Criteria

- [x] 1. Core Phase 1 uses **4–8**.  
- [x] 2. Generator inject removed.  
- [x] 3. Regenerated; `--check` clean.  
- [x] 4. Structural floors PASS.  
- [x] 5. verify.sh 0.  
- [x] 6. No whole-file allowlist.  

## Out of scope

- Changing the numeric rule (still 4–8).  
- Cursor rule.mdc rewrite.

## Verification plan

Grep core for `4–8`/`4-8`; run generator --check; run each of three sh structural
checks; verify.sh; optional negative Phase 8 test.
