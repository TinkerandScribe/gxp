# Task: merge overlapping intervals

## Deliverable

Implement `merge_intervals(intervals: list[list[int]]) -> list[list[int]]` in
`merge_intervals.py`.

## Spec

- Each interval is `[start, end]` with `start <= end` (integers).
- Merge all overlapping or **touching** intervals (e.g. `[1,2]` and `[2,3]` → `[1,3]`).
- Return merged intervals sorted by start ascending.
- Empty input → `[]`.
- Do not mutate the caller's list (return a new list).
- Invalid shapes are out of scope (tests only pass well-formed intervals).

## Constraints

- Stdlib only; edit only the starter tree; no hidden-test edits.

## Done means

Function matches the spec; note verification.
