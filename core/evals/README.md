# Evals

Lightweight artifacts that help you tell whether a change improved or
regressed behavior. Not a replacement for the test suite — these are
human-readable signals.

- `golden/` — canonical inputs/outputs you expect to keep working.
- `regressions/` — things that previously broke; keep them here so they
  are checked first when something feels off.
- `canaries/` — cheap, fast signals that a change went sideways
  (e.g. a one-line script, a screenshot, a sample query).

## Current canaries

| Path | Purpose |
|---|---|
| [`canaries/gxp-version-comparison/`](canaries/gxp-version-comparison/) | Before/after (`v1.1.3` vs HEAD): process-guarantee scorecard + brief/handoff canaries. Run `bash scripts/eval-gxp-process-guarantees.sh v1.1.3 HEAD`. See `REPORT.md`. |
| [`regressions/verification-wrapper-must-fail-on-drift.md`](regressions/verification-wrapper-must-fail-on-drift.md) | Induced structural drift must fail `verify.sh`. |

## Current golden

| Path | Purpose |
|---|---|
| [`golden/agent-code-quality/`](golden/agent-code-quality/) | **Prove whether agents write better code** (control vs GXP). Tasks **01–05** (easier) + hard pack **06–08** (`lru-ttl`, `deep-merge`, `line-chunker`) for ceiling headroom. Self-test: `bash scripts/eval-agent-code-quality-selftest.sh`. Multi-seed: `python scripts/run-code-quality-seeds.py` → [`trials/2026-07-13-multiseed/`](golden/agent-code-quality/trials/2026-07-13-multiseed/). |
