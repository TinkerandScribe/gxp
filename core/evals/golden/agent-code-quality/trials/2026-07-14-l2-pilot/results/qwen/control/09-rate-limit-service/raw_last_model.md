```json
{
"action": "done",
"content": "Fixed the rate-limit service by repairing `service/limiter.py`. The original code had two critical bugs:\n\n1. **Record-before-check**: It recorded a hit first, then checked if hits exceeded the limit — allowing one extra request beyond `max_requests`.\n2. **Off-by-one comparison**: Used `hits <= self.max_requests + 1` instead of proper check-then-record logic.\n3. **Zero max_requests not handled**: When `max_requests == 0`, it would still record a hit before comparing.\n\nThe fix implements proper **check-then-record** semantics:\n- If `max_requests == 0`, always deny without recording.\n- Check current hits in window first; if `hits >= max_requests`, deny without recording.\n- Only record a hit when the request is actually allowed.\n\nThe `service/config.py` and `service/store.py` were already correct — config properly fails closed on errors, and store uses per-key storage with proper half-open interval `(now - window_seconds, now]`."
}
```