# Task: bounded LRU cache with optional TTL

## Deliverable

Implement class `LruTtlCache` in `lru_ttl.py`.

## Spec

```python
class LruTtlCache:
    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None): ...
    def set(self, key, value) -> None: ...
    def get(self, key): ...
    def delete(self, key) -> bool: ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> bool: ...
```

### Construction

- `capacity` must be an integer **≥ 1**. Otherwise raise `ValueError` whose
  message contains `capacity` (case-insensitive).
- `ttl` is seconds of life after each successful `set` (including updates).
  `ttl is None` means entries never expire by time.
- `clock` is a zero-arg callable returning a monotonic `float` (seconds).
  Default: `time.monotonic`. **All** time decisions use this clock only.

### `set(key, value)`

- Store `value` under `key`.
- If `key` already exists (and is not expired), **update** value, **refresh**
  expiry from now + `ttl` (if TTL enabled), and mark key as **most recently used**.
- Before inserting a **new** key, **reap** all currently expired entries.
- If still at capacity, **evict the least-recently-used live entry**, then insert.
- New inserts are most recently used.
- Expiry timestamp for a new/updated entry: `clock() + ttl` when `ttl` is not
  None; otherwise no expiry.

### `get(key)`

- If missing → `KeyError`.
- If present but expired → **remove** it, then raise `KeyError`.
- If live → return value and mark key as **most recently used** (do **not**
  refresh TTL on get — TTL is only refreshed on `set`).

### `delete(key) -> bool`

- If key present (even if expired), remove it and return `True`.
- If absent, return `False`.

### `__contains__(key) -> bool`

- Return whether the key is present **and live**.
- **Must not** change recency order.
- **Must not** refresh TTL.
- **May** remove the entry if it is expired (expired → treat as absent, return
  `False`). Prefer removing expired keys when observed.

### `__len__() -> int`

- Return count of **live** (non-expired) entries.
- Must reap expired entries as part of computing length (so len reflects live
  only and frees capacity for future sets).

### Other

- Stdlib only.
- Keys must be hashable (tests use strings/ints).
- Edit only the starter tree; no hidden-test edits.

## Done means

Hidden tests pass. Prefer a short note of edge cases you checked.
