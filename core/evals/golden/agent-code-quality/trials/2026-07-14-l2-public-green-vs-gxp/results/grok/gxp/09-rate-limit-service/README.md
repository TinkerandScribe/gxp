# Rate limit service (broken starter)

Modules:

- `service/config.py` — load limits from a simple text file  
- `service/store.py` — hit timestamps  
- `service/limiter.py` — `RateLimiter.allow(key)`

Public smoke tests: `tests_public/`.

See `.ai/PROGRAM.md` for the verify command.
