# Failure capture

**Date:** 2026-07-02
**Task / context:** Project review + `fix-verification-tooling` — the repo's own parity
check reported PASS while most of the checks it wraps were failing or never ran.

## Expected

`scripts/verify.sh` exits non-zero when any adapter sync check fails, and runs every
adapter's `check-core.sh`. Each adapter's `.sh` and `.ps1` sync checks enforce the same
thing on both platforms.

## Actual

Three compounding silent failures:
1. `bash "$sh" || echo "(drift reported — review above)"` swallowed every sync-check
   exit code — verify.sh printed `=== PASS ===` while three checks exited 1.
2. The glob `adapters/*/ai-workflow/sync/check-core.sh` never matched
   `adapters/cowork/sync/check-core.sh`, so that check was silently never run.
3. In claude/chatgpt/grok `check-core.ps1`, a copy-install guard tested
   `<adapter>/core` **before** walking up to the repo root — a path that never exists —
   so on Windows the scripts printed "[B3] copy-install mode detected" and exited 0
   without checking anything, while the bash variants ran (and failed) on Linux.
4. Grok's `check-core.ps1` was UTF-8 **without BOM** with `—`/`✓` inside double-quoted
   strings. PS 5.1 reads BOM-less files as ANSI, so the em dash's trail byte (0x94)
   became a curly closing quote: the banner string ended early, `(PowerShell)` became a
   subexpression spawning a child powershell that blocked on stdin (runs appeared hung),
   quote parity flipped for later lines (phantom "term 's' not recognized" at a line
   that never executes), and the checks were skipped — while still exiting 0.

## Root cause

Proximate: `|| echo` on a command whose exit code is the product; a guard evaluated
against an unresolved path. Underlying: the wrappers and guards were never negative-tested
— nobody ever made a check fail on purpose and confirmed the failure propagated.

## Detection

- A verification wrapper that prints PASS while its own transcript contains
  `ACTION REQUIRED` / `exit 1` lines is lying — read the transcript, not the verdict.
- `[B3] copy-install mode detected` appearing when running **inside** the repo means the
  guard fired on a wrong path.
- A `.ps1` that "passes" without printing its per-item output did not run; a `.ps1` run
  that hangs with empty output, or errors citing a line that cannot execute, suggests
  no-BOM UTF-8 + smart punctuation being misparsed as ANSI curly quotes.
- Smell in a diff: `cmd || echo ...` around anything whose exit code matters; early-exit
  guards placed before path resolution completes.

## Resolution

`scripts/verify.sh` now sets `fail=1` when a sync check exits non-zero and globs both
`adapters/*/ai-workflow/sync/` and `adapters/*/sync/`; the three `check-core.ps1` scripts
resolve the repo root before applying the B3 guard; grok `check-core.ps1` and `gxp.ps1`
got a UTF-8 BOM prepended (content unchanged). Fixed in the `fix-verification-tooling`
task (see `core/tasks/fix-verification-tooling.md`).

## Prevention

- Negative-test every verification wrapper once: induce a failure, confirm the wrapper
  exits non-zero, restore. (Done for verify.sh in this task.)
- Platform-parity scripts (`.sh`/`.ps1`) must be run on both platforms after edits —
  "exits 0" alone is not evidence; confirm the check actually executed (look for its
  per-item output).
- Any `.ps1` containing non-ASCII (em dashes, ✓/✗, arrows) must be saved as UTF-8
  **with BOM**, or kept pure ASCII — Windows PowerShell 5.1 reads BOM-less files as ANSI.

## Follow-up

- [ ] Add a CI job (or documented pre-release step) that runs `bash scripts/verify.sh`
      AND the five `check-core.ps1` scripts, so both halves are exercised.
- [ ] Fix the parked tail: grok `check-core.sh` latent unbound-`$YELLOW` crash,
      `install-ai-from-core.sh` subshell counters, `adapters/README.md` negative-test doc.

## Repeatable?

Yes — "wrapper swallows exit code" and "guard runs before path resolution" are generic
footguns for any repo that wraps per-component checks in a top-level script.
