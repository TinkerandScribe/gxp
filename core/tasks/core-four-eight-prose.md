# Task brief — core “4–8” prose + drop generator inject (Roadmap M4.2)

**Status:** draft — ready for pickup  
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

- [ ] 1. `core/workflow.md` Phase 1 states **4–8** (ASCII hyphen or en-dash) binary
  criteria, not only the prose form `4 to 8`.  
- [ ] 2. Generator no longer injects a special floor-only Phase 1 line (or inject is
  a no-op / removed).  
- [ ] 3. `python scripts/generate-adapter-workflows.py` rewritten outputs; `--check`
  clean after commit.  
- [ ] 4. All of claude/chatgpt/grok structural floors still PASS (incl. 4-8 marker).  
- [ ] 5. `bash scripts/verify.sh` exit 0; Phase 8 delete still fails verify (spot-check).  
- [ ] 6. No reintroduction of whole-file workflow allowlist.

## Out of scope

- Changing the numeric rule (still 4–8).  
- Cursor rule.mdc rewrite.

## Verification plan

Grep core for `4–8`/`4-8`; run generator --check; run each of three sh structural
checks; verify.sh; optional negative Phase 8 test.
