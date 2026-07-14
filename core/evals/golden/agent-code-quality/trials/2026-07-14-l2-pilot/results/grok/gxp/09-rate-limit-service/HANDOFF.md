## Changed
- `service/config.py` — fail closed on missing/invalid config
- `service/store.py` — per-key sliding window counts
- `service/limiter.py` — check-then-record; max 0 denies
- `BRIEF.md` — criteria + Phase 0 notes

## Verified
- `python -m unittest discover -s tests_public -v` → exit 0
- Manual: multi-key isolation, max boundary, missing config deny (criteria)

## Not done
- Hidden scorer (operator)
- Stronger public tests (optional)
