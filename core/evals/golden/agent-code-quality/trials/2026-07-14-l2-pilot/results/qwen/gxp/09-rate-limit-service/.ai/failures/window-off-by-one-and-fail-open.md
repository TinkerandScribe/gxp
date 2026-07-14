# Failure: window off-by-one and fail-open config

**Symptom:** Clients get one extra request beyond `max_requests`; bad config
files accidentally allow unlimited traffic.

**Likely causes:**

1. Counting hits with `>=` inverted (record before check, or allow when
   `hits == max`).  
2. Using a fixed calendar bucket instead of a sliding window.  
3. On config parse error, returning a huge `max_requests` “default.”  
4. Single global hit list shared across all keys.

**Fix direction:** check-then-record; sliding window `(now - W, now]`; fail
closed (`max_requests=0`); per-key storage.
