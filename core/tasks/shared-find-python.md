# Task brief — shared find-python helper (Roadmap M4.1)

**Status:** done  
**Depends on:** nothing  
**Workflow:** lightweight or full (small multi-file)

## Goal

One shared bash helper that resolves a working Python interpreter so scripts stop
re-implementing (and forgetting) the Windows Store-stub probe.

## Context

- Pattern proven in `scripts/eval-agent-code-quality-selftest.sh`,
  `scripts/eval-gxp-process-guarantees.sh`, `adapters/cowork/build.sh`.  
- Failure: `core/failures/windows-git-bash-python3-store-stub.md`.  
- Cowork `check-core.sh` already has a partial probe; align if easy.

## Ideal State Criteria

- [x] 1. `scripts/lib/find-python.sh` sets `PY` via executable probe.  
- [x] 2. Call sites: selftest, process-guarantees, CI generate `--check`, cowork build.  
- [x] 3. Selftest exit 0.  
- [x] 4. verify.sh exit 0.  
- [x] 5. Failure capture updated.  
- [x] 6. Rating on the combined proceed commit.  

## Out of scope

- Rewriting PowerShell scripts (optional note only).  
- Changing generator logic beyond how Python is invoked.

## Verification plan

Run selftest + verify.sh on Windows Git Bash if available; otherwise WSL/Linux
and document the Store-stub path as covered by unit probe in the helper.
