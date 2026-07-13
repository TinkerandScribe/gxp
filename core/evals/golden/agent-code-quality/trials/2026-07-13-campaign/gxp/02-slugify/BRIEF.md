# GXP brief — 02-slugify

## Goal
slugify() to ASCII lowercase hyphenated slug.

## Ideal State Criteria
- [ ] Lowercase
- [ ] Non [a-z0-9] runs → single `-`
- [ ] Trim edge dashes
- [ ] Empty/all-separator → ""
- [ ] Unicode letters dropped
- [ ] score_trial correctness 1.0

## Out of scope
i18n slug libraries; hidden-test edits.

## Verification
score_trial.py --task 02-slugify until 1.0.
