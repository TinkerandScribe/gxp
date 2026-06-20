---
name: gxp-rate
description: Append one honest JSON line to `ratings.jsonl` recording the outcome of a GXP task. Use at the end of a `gxp-workflow` run (Phase 6), or when the user says "rate that", "log the rating", "append the rating", "record this in ratings.jsonl", or "score this run gxp-style". Forces honesty — drops the rating when criteria slipped, refuses to stamp a flat 8, requires a real `criteria_met / criteria_total` count. One JSON object per line, never an array, never a multi-run line.
---

# GXP Rate (Phase 6)

Append one honest line to `ratings.jsonl` (or `core/ratings.jsonl` in a gxp repo) summarizing the run that just completed.

## Gather the inputs

Before writing, confirm these from the conversation context (or ask if any are missing):

- **Task slug** — short kebab-case identifier; matches the brief filename if one exists.
- **Brief path** — `tasks/<slug>.md` or `core/tasks/<slug>.md`, or a one-line inline summary if no brief was written (lightweight mode).
- **Criteria met / total** — actual counts from the brief's Ideal State Criteria. Walk them. Do not approximate.
- **Mode** — `full` or `lightweight`.
- **Notes** — one line. What was verified, what's parked, why the rating is what it is.
- **Failure ref** — path under `failures/` if a failure was captured this run; else empty string.

## Pick the rating honestly

`rating` is an integer 1–10. Rules:

- **10** — every criterion met, verification thorough across deterministic/behavioral/subjective, no caveats. Rare.
- **8–9** — every criterion met, minor caveats or one criterion confirmed by eyeball rather than mechanical check.
- **6–7** — some criteria slipped (or were skipped with reason), but the core goal landed.
- **4–5** — partial. Useful work done but the brief's goal didn't fully land.
- **1–3** — the run didn't accomplish the task. Includes runs that hit the anti-loop and stopped.

**Drop the rating when criteria slip.** A 13/15 criteria run is not an 8 — it's a 7. A 7/15 run is not a 5 — it's a 3 or 4.

**Refuse to stamp a flat 8 every run.** If multiple recent entries in `ratings.jsonl` already read 8, ask whether the run actually went that well or whether the rating should reflect reality.

**No-op or fallback runs** (offline mocks that exercise plumbing only, not task intelligence) score low — usually 1–3 — and the notes explain "plumbing only, no real task completion."

## Write the line

Format:

```json
{"ts": "<ISO-8601>", "task": "<slug>", "brief": "<path or summary>", "criteria_met": <int>, "criteria_total": <int>, "rating": <1-10>, "mode": "full|lightweight", "notes": "<one line>", "failure_ref": "<path or empty string>"}
```

Hard rules:

- **One JSON object per line.** Never a JSON array. Never two runs on one line.
- Append to the file with a newline at the end. Do not overwrite the file. Do not pretty-print.
- ISO-8601 timestamp. Use the current time.

## After writing

Read back the appended line and confirm to the user:

- The file path it was appended to.
- The full line as written.
- A one-sentence justification of the rating ("8/10 because 7/7 criteria met, deterministic + behavioral verification, one eyeball confirmation on the UX text").

If the user disagrees with the rating, **don't** silently overwrite — ask them what to change and append a correction note or a follow-up entry. The point of the ledger is the audit trail.

## What this skill is NOT

- Not a substitute for honest self-assessment. The agent does not auto-stamp ratings; this skill walks the user through one rating, deliberately.
- Not for batch rewriting historical ratings. If old entries need cleaning up, that's a separate conversation.
- Not for hiding bad runs. A low rating on a real run is more valuable than a generous one.

## Reference

`references/ratings-schema.md` (in the `gxp-workflow` skill) has the full schema and examples.
