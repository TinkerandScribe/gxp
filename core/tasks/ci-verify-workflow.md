# Task brief — CI for verify.sh and platform checks (audit P0-1)

**Status:** done (Milestone 1, item 2) — 2026-07-13
**Depends on:** `real-diff-sync-checks` — landed (structural floor makes the
negative-drift test real).

## Goal

Add GitHub Actions CI that runs the repo's verification on every push/PR on both
platforms, builds the cowork plugin, and proves the checks can fail via an induced
negative test.

## Context

- The repo's own failure entry (`verification-wrapper-swallows-exit-codes.md`) lists
  CI as the undone follow-up; the audit's P0-1 sketch is the starting point but has
  three defects the review found:
  1. Its negative test appends drift to claude `workflow.md` — an allow-listed file —
     so the assert can never trigger pre-P0-2 (and post-P0-2 the induced drift should
     be a structural deletion, which the new floor catches).
  2. `windows-latest` Git Bash has no `zip`; the cowork build step must be
     ubuntu-only or install zip.
  3. If staleness markers (next brief) use `git rev-list`, shallow checkout
     (`fetch-depth: 1` default) breaks SHA resolution — use `fetch-depth: 0`.
- The ps1 checks target **Windows PowerShell 5.1** semantics (the BOM/ANSI failure
  class lives there) — run them with `shell: powershell`, not `pwsh`.

## Ideal State Criteria

- [x] 1. `.github/workflows/verify.yml` runs on push and pull_request; matrix
  ubuntu-latest + windows-latest with `fail-fast: false`; checkout uses
  `fetch-depth: 0`.
- [x] 2. `bash scripts/verify.sh` runs and gates on both OSes (Git Bash on Windows).
- [x] 3. Every `adapters/**/sync/check-core.ps1` runs on Windows under
  `shell: powershell` (5.1), aggregated so any non-zero exit fails the job.
- [x] 4. `adapters/cowork/build.sh` runs on ubuntu and its exit code gates the job.
- [x] 5. A negative-test step induces structural Phase 8 deletion, asserts
  verify.sh exits non-zero, and restores the tree (local smoke OK; first main CI run
  is the live proof).
- [x] 6. The workflow is green on main at merge —
  https://github.com/TinkerandScribe/gxp/actions/runs/29279663570

## Out of scope

- Staleness auto-bump job (belongs to `staleness-marker-real-sha`).
- Release automation, badges, branch protection settings.

## Verification plan

Push to a branch; observe matrix runs. Criterion 5 requires one deliberately red run
(sabotage commit) and its restoration — link both runs. Deterministic throughout.
