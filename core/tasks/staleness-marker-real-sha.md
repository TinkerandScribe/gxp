# Task brief — live staleness markers (audit P0-3)

**Status:** done (Milestone 1, item 3) — 2026-07-13
**Depends on:** `ci-verify-workflow` (hosts the auto-bump job and needs
`fetch-depth: 0`). Prerequisite already landed: grok `check-core.sh` def-order fix
(the old code crashed under `set -u` the moment a marker parsed as a real SHA —
fixed in `verification-hardening-unblockers-and-roadmap`).

## Goal

Make the "Last synced from core" mechanism real: every adapter carries a valid commit
SHA, the checks hard-fail when an adapter falls more than a threshold behind core,
and CI keeps the markers fresh so they don't rot.

## Context

- At v1.1.2 the marker regex (`[0-9a-fA-F]+`) never matches the prose markers
  ("post-strategy-prototype-implementation"), and chatgpt/claude have no marker at
  all — the mechanism fires nowhere (audit claim 3, verified).
- **Found during the unblocker task (audit missed this):** the regex also cannot
  match the marker's own markdown format — `Last\ synced\ from\ core:\ ` requires
  colon-space, but the bold marker renders as `core:** <sha>`. Even a real SHA in the
  documented `> **Last synced from core:** <sha>` format never matches (proven by
  running the check with a real SHA in bold format: no NOTE; same marker unbolded:
  NOTE fires). The audit's P0-3 sketch keeps both the bold format and the regex, so
  as written it ships a mechanism that still never fires. Fix the regex to tolerate
  `:\*\*` (or standardize the marker format) as part of this task.
- The audit's sketch treats an unresolvable SHA as FAIL; in shallow clones that is a
  false failure — degrade to WARN when history is truncated, FAIL when the marker is
  absent or malformed.

## Ideal State Criteria

- [x] 1. chatgpt, claude, grok, and perplexity carry bold real-SHA markers; regex
  matches bold `core:** <sha>` and plain forms (sh + ps1).
- [x] 2. Checks hard-fail when behind threshold (default 3) or marker missing/malformed.
- [x] 3. Shallow/unresolvable well-formed SHA → WARN (not false FAIL).
- [x] 4. Aging past threshold fails the check (threshold/env `GXP_STALE_THRESHOLD`).
- [x] 5. CI `bump-markers` job + `scripts/update-sync-markers.sh`.
- [x] 6. Perplexity prints presence + staleness and enforces the same policy.

## Out of scope

- Hash-chained ratings ledger, critic descope (Milestone 2).
- Rewriting adapter content (markers only; content parity is `real-diff-sync-checks`).

## Verification plan

Behavioral marker-aging tests per adapter per platform (bash + PowerShell 5.1) with
restores; shallow-clone simulation via `git clone --depth 1` into a temp dir;
verify.sh before/after. Deterministic throughout.
