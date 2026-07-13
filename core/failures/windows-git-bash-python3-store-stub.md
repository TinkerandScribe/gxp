# Failure capture

**Date:** 2026-07-13
**Task / context:** Running `scripts/eval-agent-code-quality-selftest.sh` (and similar
eval scripts) under Windows Git Bash after the agent-code-quality harness landed.

## Expected

`python3` or a documented fallback runs the scorer; self-test exits 0.

## Actual

1. `command -v python3` succeeded but the binary was the **Microsoft Store stub**,
   which cannot execute Python — the `|| PY=python` fallback never ran.
2. Separately, hardcoding `/tmp/...` inside a Python heredoc disagreed with paths
   bash rewrites when the same string is passed as a CLI argument (Git Bash
   path conversion), so writer and reader used different files.

## Root cause

Existence ≠ executability on Windows. Store aliases and Git Bash path munging
create two independent footguns for shell scripts that assume Unix `python3` + `/tmp`.

## Detection

- Script fails with Store-related errors or empty/missing temp JSON despite
  `command -v python3` succeeding.
- Self-test fails only on Windows Git Bash while WSL/Linux is green.

## Resolution

Probe with `"$PY" -c ""` before trusting `python3`; fall back to `python`.
Use `mktemp -d` and pass the directory into Python via `argv` (not a hardcoded
path inside the heredoc). Applied in `scripts/eval-agent-code-quality-selftest.sh`
and `scripts/eval-gxp-process-guarantees.sh`.

## Prevention

- Prefer the repo pattern: `PY=python3; "$PY" -c "" >/dev/null 2>&1 || PY=python`.
- Never hardcode `/tmp` inside mixed bash/Python path construction on Git Bash.
- Cowork `build.sh` still has a bare `python3` — same class; fix when touched.

## Follow-up

- [ ] Audit remaining `python3` invocations under `scripts/` and `adapters/*/build*`.

## Repeatable?

Yes — any Windows Git Bash environment with the Store Python alias and no real
`python3` on PATH.
