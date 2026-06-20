# Failure capture

**Date:** 2026-06-17
**Task / context:** `scripts/launch-background-job.py` detached run launcher (audit #5 / Telegram dispatch).

## Expected

a background-job launcher detaches a `<your-cli> run @<goalfile>` child, returns fast, and the
child writes its full output to the dated `logs/*.log`. The launcher→worker
auto-route depends on this.

## Actual

**Every** detached run produced an empty log (just the header) and no artifacts —
the child died at launch. This was misread for days as "the engine no-ops"
(blamed on the trust gate, then `--approve-reversible`), when the launcher was at fault.

## Root cause

Two Windows-specific bugs:
1. `finally: os.unlink(temp_goal_file)` deleted the `@goal` temp file ~1.5s after
   detaching — **racing** the child, which reads it only after Python startup → the
   child crashed on a missing file.
2. The child ran via `cmd /c "<inner> >> log 2>&1"` under `DETACHED_PROCESS`, which
   **captured no output** on Windows — so even the crash was invisible.

## Detection

Smell: a launcher that deletes an input file in `finally` after detaching a child
that still needs it; shell-string redirection (`>> log 2>&1`) for a detached process.
Behavioral: detached-run logs contain only the header; no artifacts/cards appear.

## Resolution

Stopped deleting the goal file (the OS temp dir reclaims it); handed the log file to
the child as **inherited `stdout`/`stderr`** via `Popen(..., stdout=logf, stderr=STDOUT,
creationflags=CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW)` (no shell, no quoting). Also
made the launcher respect an explicit `LLM_DISABLE` instead of force-clearing it.
Verified: detached run executes (5 approved, `success=true`, `api_client.py` written),
log fully captured, then proven live via Telegram.

## Prevention

- A detached child must own its inputs — don't delete a temp file the child reads
  after the parent returns.
- Capture detached output via inherited file handles, **not** shell redirection +
  `DETACHED_PROCESS`, on Windows.
- When a downstream "produces nothing," verify the *launcher/transport* before
  blaming the engine — this cost days of misattribution.

## Repeatable?

Yes — detached-process launching on Windows is a recurring footgun (handle
inheritance, temp-file lifetime, console flags).
