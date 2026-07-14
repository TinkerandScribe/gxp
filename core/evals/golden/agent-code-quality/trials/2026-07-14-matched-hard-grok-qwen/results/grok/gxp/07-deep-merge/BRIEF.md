# GXP brief — 07-deep-merge

## Goal
Implement `deep_merge` with deep-copy, list modes, and None-delete.

## Ideal State Criteria
- [ ] Never mutate base/override trees
- [ ] Nested plain dicts recurse
- [ ] None override deletes key
- [ ] list_mode replace/extend/unique correct
- [ ] Unknown list_mode raises ValueError with list_mode
- [ ] Mismatched types: override wins via deep-copy
- [ ] Base-only and override-only keys preserved/copied

## Out of scope
Custom mapping types, concurrent merge.

## Verification
Self-check mutation isolation and list modes; scorer later.
