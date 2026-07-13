# GXP brief — 01-parse-kv

## Goal
Implement parse_kv per prompt: KEY=VALUE dict with validation and quote rules.

## Ideal State Criteria
- [ ] Valid lines produce correct key/value pairs
- [ ] Comments and blanks ignored
- [ ] Invalid lines raise ValueError mentioning invalid + count
- [ ] Quoted values unwrap outer `"` only; interior spaces preserved
- [ ] Last duplicate key wins
- [ ] Scorer: `score_trial.py --task 01-parse-kv` correctness == 1.0

## Out of scope
Network, non-stdlib, editing hidden tests.

## Verification
Run score_trial.py; fix failures until 1.0 or two failed same approach.
