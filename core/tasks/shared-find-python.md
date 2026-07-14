# Task brief — shared find-python helper (Roadmap M4.1)

**Status:** draft — ready for pickup  
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

- [ ] 1. `scripts/lib/find-python.sh` (or equivalent) sets `PY` to an executable
  interpreter via `"$candidate" -c ""` probe (`python3` then `python`).  
- [ ] 2. At least these call sites use it (or equivalent sourced one-liner):  
  `eval-agent-code-quality-selftest.sh`, `eval-gxp-process-guarantees.sh`,
  `generate-adapter-workflows.py` invocation in CI/docs, `cowork/build.sh`.  
- [ ] 3. `bash scripts/eval-agent-code-quality-selftest.sh` exits 0.  
- [ ] 4. `bash scripts/verify.sh` exits 0.  
- [ ] 5. Failure capture follow-up checkbox updated; no bare critical `python3` in
  those call sites.  
- [ ] 6. Rating appended if full workflow.

## Out of scope

- Rewriting PowerShell scripts (optional note only).  
- Changing generator logic beyond how Python is invoked.

## Verification plan

Run selftest + verify.sh on Windows Git Bash if available; otherwise WSL/Linux
and document the Store-stub path as covered by unit probe in the helper.
