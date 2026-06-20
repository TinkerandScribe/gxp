# Weekly refine

**Week of:**

## Ratings review

Skim the last week of `ratings.jsonl` (one JSON object per line, ratings
on a 1–10 scale). Note anything surprising.

- Patterns in low-rated runs:
- Patterns in high-rated runs:
- Tasks where Ideal State Criteria felt wrong (too vague, too narrow):
- Tasks that hit the phase 4 anti-loop rule:

## Failures review

Look through `failures/`. For each entry:

- Still repeatable? If no, delete it.
- Did it recur this week? If yes, the existing prevention is not
  working — promote it harder.
- Convert recurring failures into one of:
  - **A test** — preferred. The failure becomes a checked invariant.
  - **A doc** in `.ai/PROGRAM.md` or `wiki/` — when behavior is
    non-obvious but cannot be cheaply tested.
  - **A rule** in `rules/` — when the lesson generalizes across tasks.
- Once converted, delete the failure entry (it's been promoted).

## Rules check

Skim `rules/`. Any rule that no longer applies — delete it. Vague rules
should either be sharpened or removed. Rules that have never been
referenced in a brief in months are probably stale.

## PROGRAM.md drift

Anything in `PROGRAM.md` that is now wrong or stale? Fix it. Commands
that have changed, conventions that have shifted, tools that have been
swapped — update or remove.

## Dead ends review

Skim phase-4 dead ends recorded in recent briefs. Any pattern? A
repeated dead end is usually a missing rule or a missing doc.

## One change to try next week

Pick one workflow tweak to experiment with. Capture it here so you can
evaluate it at the next refine.
