# BRIEF — Rate Limit Service Repair

## Goal
Fix multi-factor bugs in the rate-limit service so it correctly implements:
- Sliding window counting with half-open interval `(now - W, now]`
- Per-key isolation in HitStore
- Fail-closed config (missing/invalid → `max_requests=0`)
- Check-then-record logic (deny if already at max, don't record denied hits)
- `max_requests == 0` always denies

## Binary Criteria
1. **Fail-closed config**: missing file or parse error returns `max_requests=0`, not a huge number.
2. **Per-key isolation**: hits for key "a" never counted for key "b".
3. **Sliding window**: only timestamps in `(now - window_seconds, now]` are counted (left-exclusive, right-inclusive).
4. **Check-then-record**: if hits >= max_requests, return False WITHOUT recording.
5. **Exact limit enforcement**: exactly `max_requests` calls succeed, the next is denied.
6. **Zero max denies all**: `max_requests=0` always returns False and records nothing.
7. **from_config works**: loads defaults when path=None, fails closed on bad file.
8. **Public tests pass**: `python -m unittest discover -s tests_public -v` exits 0.

## Out of Scope
- Adding third-party dependencies
- Changing the public API signatures
- Rewriting unrelated files

## Verification
Run: `python -m unittest discover -s tests_public -v`
Plus manual integration checks for all criteria above.
