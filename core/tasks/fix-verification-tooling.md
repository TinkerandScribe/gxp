# Task brief

**Date:** 2026-07-02
**Task slug:** fix-verification-tooling
**Workflow:** full

## Goal

Fix the critical/high findings from the 2026-07-02 project review so that the repo's own
verification tooling actually verifies: `verify.sh` propagates failures and covers all
adapters, every sync check passes honestly on a clean checkout on both bash and
PowerShell, and the shipped artifacts (cowork plugin sources, perplexity workflow) no
longer contradict core.

## Context

- Related files: `scripts/verify.sh`, `scripts/install-ai-from-core.ps1`,
  `adapters/grok/ai-workflow/gxp.ps1`, `adapters/grok/ai-workflow/sync/check-core.{sh,ps1}`,
  `adapters/claude/ai-workflow/sync/` (new `drift-allowlist.txt` + `check-core.ps1`),
  `adapters/chatgpt/ai-workflow/sync/check-core.ps1`,
  `adapters/cursor/ai-workflow/sync/check-core.sh`,
  `adapters/cowork/sync/check-core.sh`,
  `adapters/cowork/plugin-src/skills/gxp-failure-capture/SKILL.md`,
  `adapters/cowork/plugin-src/skills/gxp-brief/SKILL.md`,
  `adapters/perplexity/ai-workflow/instructions/workflow.md`
- Rules that apply: `core/rules/02-local-context-never-committed.md` (nothing
  project-private in this brief or in ratings notes).
- Review provenance: findings verified by live execution during the review session
  (verify.sh PASS-while-failing, ps1 B3 no-ops, gxp.ps1 CommandNotFound, `-TargetRepo`
  junk directory, truncated SKILL.md, legacy perplexity schema).

**Strategy/Model:** current Claude Code session — fixes require live bash + PowerShell 5.1
verification on Windows, available here; smallest capable engine with margin.

## Ideal State Criteria

- [x] 1. `bash scripts/verify.sh` exits 0 on the clean tree, runs all six adapter sync
  checks (including `adapters/cowork/sync/check-core.sh`), and exits non-zero when a sync
  check fails (proven by a temporary induced drift, then restored).
- [x] 2. Dot-sourcing `adapters/grok/ai-workflow/gxp.ps1` in PowerShell 5.1 emits no
  error, and `gxp help` runs without `CommandNotFoundException`.
- [x] 3. `scripts/install-ai-from-core.ps1 -TargetRepo <scratch> -Force -IncludeCursorRule`
  creates `<scratch>\.cursor\rules\ai-workflow.mdc` and creates no directory named
  `-TargetRepo` anywhere.
- [x] 4. All six `check-core` bash scripts exit 0 on the clean tree in Git Bash; the
  cowork check reports a missing `python3` as an explicit skip/warning, not
  "invalid JSON".
- [x] 5. The chatgpt, claude, and grok `check-core.ps1` scripts, run from inside the
  repo, perform real checks (no "[B3] copy-install mode" short-circuit) and exit 0 on the
  clean tree; cursor and perplexity `check-core.ps1` still exit 0.
- [x] 6. `gxp-failure-capture/SKILL.md` ends with a complete sentence and trailing
  newline; `gxp-brief/SKILL.md` references only files that `build.sh`/`build.ps1`
  actually place in that skill's `references/`.
- [x] 7. The perplexity adapter's Phase 6 example uses the core schema (`ts`,
  `criteria_met`, `criteria_total`, integer `rating` 1–10) and `grep -ri timestamp
  adapters/perplexity/` returns no ratings-schema hits.
- [x] 8. `git status` shows changes only to the files named in this brief (plus this
  brief, `ratings.jsonl`, and any `failures/` capture).

## Out of scope

- `install-ai-from-core.sh` subshell counter bug (reporting-only; files copy correctly).
- ChatGPT/Claude adapters' missing Phase 8 and stale model-tier text; chatgpt "(v1.0)" header.
- macOS bash-3.2 empty-array portability; `find_repo_root` 4-level fallback.
- Grok `check-core.sh` latent unbound-`$YELLOW` crash in the dormant last-synced-marker
  block (parked as follow-up; the block never triggers today).
- `adapters/README.md` negative-test doc and cursor README `Select-String` doc fixes.
- Rebuilding/shipping `dist/gxp.plugin`; committing or pushing anything.

## Verification plan

Deterministic first: run `bash scripts/verify.sh` (criterion 1), each `check-core.sh`
directly (4), each `check-core.ps1` via `powershell -File` (5), `grep -ri timestamp
adapters/perplexity/` (7), byte-check SKILL.md tail (6), `git status --short` (8).
Behavioral: induced-drift test for verify.sh (1), dot-source + `gxp help` in a fresh
PS 5.1 process (2), scratch-repo install run under the scratchpad dir (3).

## Self-evaluation gate

- [x] **Completeness** — covers every critical/high review finding; medium tail parked.
- [x] **Ambiguity** — each criterion is a command with an exit code or a byte check.
- [x] **Scope trap** — grok latent crash + counter bug explicitly parked.
- [x] **Verification** — every criterion has a concrete check above.
- [x] **Approval gates** — none: all edits reversible in-tree; no commits, no deletes,
  scratch installs confined to the session scratchpad.

## Approval gates

- None (reversible working-tree edits only; nothing destructive, public-facing, or
  production-touching).

## Dead ends

- Criterion 5 was initially marked verified on flawed evidence: grok `check-core.ps1`
  "exited 0" but was misparsing. The file was UTF-8 **without BOM** with `—`/`✓` inside
  double-quoted strings; PS 5.1 reads BOM-less files as ANSI, so the em dash's 0x94 trail
  byte became a curly closing quote — the banner string ended early, `(PowerShell)`
  became a subexpression that spawned a child powershell blocking on stdin (observed as
  stuck background runs), quote parity flipped, and the real checks were skipped.
  Resolution: prepended UTF-8 BOM to grok `check-core.ps1` and `gxp.ps1` (content
  unchanged); re-ran non-quiet — banner, 8 ALLOW lines, ✓ summary, exit 0, no hang.
  Lesson: "exit 0" alone is not evidence a check ran — require its per-item output.

## Handoff notes

- What changed: `scripts/verify.sh` (propagate sync-check failures, cover
  `adapters/*/sync/`), `scripts/install-ai-from-core.ps1` (named-parameter cursor-rule
  invocation), `adapters/grok/ai-workflow/gxp.ps1` (removed self-shadowing alias;
  UTF-8 BOM prepended), `adapters/grok/.../check-core.ps1` (UTF-8 BOM prepended —
  see Dead ends),
  `adapters/{chatgpt,claude,grok}/.../check-core.ps1` (repo-root resolution before B3
  guard), `adapters/grok/.../check-core.{sh,ps1}` (allowlist matches paths as documented),
  new `adapters/claude/.../sync/drift-allowlist.txt`, `adapters/cursor/.../check-core.sh`
  (structural markers mirroring the ps1, replacing the impossible byte-compare),
  `adapters/cowork/sync/check-core.sh` (python3-missing reported as WARN/skip),
  `adapters/cowork/plugin-src/skills/{gxp-failure-capture,gxp-brief}/SKILL.md`
  (truncation completed; dangling reference reworded),
  `adapters/perplexity/.../instructions/workflow.md` (Phase 6 on core ratings schema).
- What was verified: all 8 criteria — deterministic (verify.sh exit codes incl. induced
  drift, 6 sh + 5 ps1 sync checks, greps, byte tail, git status) and behavioral
  (dot-source + `gxp help`, scratch-repo install with cursor rule).
- Explicitly not done / parked: install-ai-from-core.sh subshell counters; chatgpt/claude
  Phase 8 omission and stale chatgpt model tiers / "(v1.0)" header; macOS bash-3.2
  empty-array portability; find_repo_root 4-level fallback; grok latent unbound-$YELLOW
  block; adapters/README negative-test doc; cursor README Select-String doc; rebuilding
  dist/gxp.plugin (sources fixed — rebuild before next release).
- Approval gates hit: none (none declared; nothing destructive or public-facing).
- Dead ends: none — no approach failed twice; anti-loop not triggered.
- Rating entry: `core/ratings.jsonl` ts 2026-07-02T09:43:17-03:00, 8/8, rating 9.
- New failures entry: `core/failures/verification-wrapper-swallows-exit-codes.md`.
