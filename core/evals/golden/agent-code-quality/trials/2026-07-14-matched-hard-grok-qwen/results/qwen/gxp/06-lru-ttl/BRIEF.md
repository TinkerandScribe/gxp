### Brief

**Goal**: Implement a bounded LRU cache with optional TTL expiration using only standard library components. The implementation must strictly adhere to capacity limits, LRU ordering (updated on `set` and `get`), and TTL expiration logic (checked on access and before insertion).

**Binary Criteria**:
1. **Capacity Validation**: `__init__` raises `ValueError` if `capacity < 1`.
2. **LRU Ordering**: `set` and `get` move accessed keys to the "most recently used" position; eviction removes the "least recently used" live entry.
3. **TTL Expiration**: Entries expire after `ttl` seconds from their last `set`. Expired entries are treated as missing in `get`, `__contains__`, and `__len__`.
4. **Reaping on Insert**: Before inserting a new key, all currently expired entries are removed to free capacity.
5. **No TTL Refresh on Get**: `get` updates LRU order but does *not* extend the TTL.
6. **Delete Behavior**: `delete` removes keys regardless of expiration status and returns `True` if present (even if expired), `False` otherwise.
7. **Contains/Len Semantics**: `__contains__` checks for live presence without changing LRU order. `__len__` returns count of live entries, triggering reaping of expired items.
8. **Clock Isolation**: All time calculations use the provided `clock` callable (defaulting to `time.monotonic`).

**Out of Scope**: Thread safety, persistence, complex key types beyond hashable primitives, non-stdlib dependencies.

**Verification**: I will verify by mentally tracing edge cases:
- Inserting into a full cache with expired items should reap first, then insert without eviction if space opens.
- Getting an expired item should remove it and raise `KeyError`.
- Updating an existing key should refresh its TTL and move it to MRU.
- `__len__` should accurately reflect live entries by cleaning up expired ones.

### Implementation
