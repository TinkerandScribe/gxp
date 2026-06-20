# Evals

Lightweight artifacts that help you tell whether a change improved or
regressed behavior. Not a replacement for the test suite — these are
human-readable signals.

- `golden/` — canonical inputs/outputs you expect to keep working.
- `regressions/` — things that previously broke; keep them here so they
  are checked first when something feels off.
- `canaries/` — cheap, fast signals that a change went sideways
  (e.g. a one-line script, a screenshot, a sample query).

Each subdirectory is initially empty. Add files as the project grows.
