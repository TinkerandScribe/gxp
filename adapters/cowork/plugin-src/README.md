# GXP — Verification-First Workflow

A Cowork plugin packaging the GXP methodology from [gxp](https://github.com/TinkerandScribe/gxp): a verification-first, binary-criteria discipline for bounded L3/L4 agent work.

## What this gives you

Four skills Claude will invoke when relevant:

- **`gxp-workflow`** — full GXP loop (Phases 0–8). Triggers on phrases like "run gxp on X", "use gxp methodology", "verification-first on X", or any non-trivial task where Claude should not skip discipline.
- **`gxp-brief`** — draft a task brief only, do not implement. Triggers on "draft a brief for X", "write a gxp brief", "what are the ideal state criteria for X".
- **`gxp-rate`** — append one honest JSON line to a `ratings.jsonl` after a task. Triggers at the end of a GXP run or when the user says "rate that" / "log the rating".
- **`gxp-failure-capture`** — capture a repeatable failure in the `failures/` directory with expected/actual/root-cause/detection/resolution/prevention. Triggers when something broke and the lesson is worth remembering.

## Core principles (short version)

- **Bounded agent.** Work within the brief. Don't self-direct or expand scope. Pause at approval gates.
- **Binary Ideal State Criteria.** 4–8 statements each clearly true or false. "Tests pass" is too vague; "`python -m pytest tests/foo -q` exits 0" is checkable. If you can't write 4 strong binary criteria, the task isn't understood — clarify first.
- **Self-evaluation gate before coding.** Completeness, ambiguity, scope, verification, approval gates.
- **Anti-loop.** Same approach fails twice → stop, document the dead end, change strategy.
- **Verification order.** Deterministic (test/lint/build) → behavioral → subjective.
- **Radical honesty in ratings.** A low rating on a real run is more useful than a generous one.

## Where artifacts live

GXP writes to a few well-known locations in whatever folder you're working in:

| Artifact          | Path                  | Format            |
| ----------------- | --------------------- | ----------------- |
| Task briefs       | `tasks/<slug>.md`     | Markdown          |
| Ratings ledger    | `ratings.jsonl`       | One JSON / line   |
| Failure entries   | `failures/<slug>.md`  | Markdown          |
| Repo rules        | `rules/`              | Markdown per rule |

If you're working in a repo that already uses the `.ai/` portable layout (or the `core/` layout from gxp), the skills detect and reuse those paths instead.

## Credit

GXP is from [gxp](https://github.com/TinkerandScribe/gxp) — Tinker & Scribe Workshop. This plugin is a Cowork packaging of that methodology.
