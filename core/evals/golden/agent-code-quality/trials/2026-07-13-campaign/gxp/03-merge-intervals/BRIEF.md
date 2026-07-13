# GXP brief — 03-merge-intervals

## Goal
Merge overlapping/touching integer intervals; sorted; non-mutating.

## Ideal State Criteria
- [ ] Sort by start
- [ ] Merge overlap and touch (start <= prev_end)
- [ ] Empty → []
- [ ] Do not mutate input
- [ ] score_trial correctness 1.0

## Out of scope
Invalid intervals; hidden-test edits.

## Verification
score_trial.py --task 03-merge-intervals until 1.0.
