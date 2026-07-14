# GXP brief — 06-lru-ttl

## Goal
Implement `LruTtlCache` per prompt so all hidden tests pass.

## Ideal State Criteria
- [ ] capacity < 1 raises ValueError containing "capacity"
- [ ] set updates value, refreshes TTL, marks MRU
- [ ] new insert reaps expired then evicts LRU if still full
- [ ] get on expired removes then KeyError; get does not refresh TTL
- [ ] __contains__ does not change recency; reaps expired
- [ ] __len__ reaps and counts live only
- [ ] delete returns True for present (incl. expired)

## Out of scope
Hidden tests, non-hashable keys, async/threading.

## Verification
Manual checklist against criteria; official score_trial after handoff.
