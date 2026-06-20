# ratings.jsonl schema

The ratings ledger records one honest line per GXP run. **One JSON object per line. No arrays. No multi-run lines.**

## Required fields

| Field            | Type   | Notes                                                                  |
| ---------------- | ------ | ---------------------------------------------------------------------- |
| `ts`             | string | ISO-8601 timestamp, e.g. `2026-06-19T22:00:00Z`                        |
| `task`           | string | Short task slug — matches the brief filename                           |
| `brief`          | string | Path to the brief markdown file, or a one-line inline summary          |
| `criteria_met`   | int    | How many Ideal State Criteria passed                                   |
| `criteria_total` | int    | Total criteria in the brief                                            |
| `rating`         | int    | Overall outcome, **1–10**. Honest. Not stamped flat.                   |

## Optional fields

| Field         | Type   | Notes                                                                  |
| ------------- | ------ | ---------------------------------------------------------------------- |
| `mode`        | string | `full` or `lightweight` — which workflow variant ran                   |
| `notes`       | string | Free text. One line. What's verified, what's parked, why the rating.   |
| `failure_ref` | string | Path under `failures/` if a failure was captured this run; else `""`   |

## Example lines

A clean run:

```json
{"ts": "2026-06-19T08:30:00Z", "task": "shop-skills-rule-packs", "brief": "core/tasks/shop-skills-rule-packs.md", "criteria_met": 7, "criteria_total": 7, "rating": 8, "mode": "full", "notes": "quote_feasibility SKILL skeleton; rule-pack templates; 172 pytest pass. Parked: quoting math.", "failure_ref": ""}
```

A partial — criteria slipped, rating drops:

```json
{"ts": "2026-06-19T18:00:00Z", "task": "desktop-cdp-control-v2", "brief": "core/tasks/desktop-cdp-control-v2.md", "criteria_met": 13, "criteria_total": 15, "rating": 7, "mode": "full", "notes": "Phase-2 routing done; Live desktop smoke not verified (Store MSIX CDP bind failed in session).", "failure_ref": "claude-desktop-cdp-unofficial.md"}
```

## Honesty rules

- The rating should **drop** when criteria slip. A 7/15 criteria run is not an 8/10.
- A no-op or fallback run (e.g. offline mock that exercises plumbing only) is **not** an 8.
- "Did anything at all run" is **not** what `rating` measures. `rating` measures whether the *task* was accomplished against the criteria the brief set.
- If the agent itself authored the rating, prefer a **low default** — humans audit and adjust upward when warranted, not the other way around.

## Legacy field names

Older project logs may use `timestamp`, `score`, `criteria_passed`. New entries should use the schema above.
