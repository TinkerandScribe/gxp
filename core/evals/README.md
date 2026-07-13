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

_(none yet — add frozen coding fixtures when multi-run quality tracking starts)_
