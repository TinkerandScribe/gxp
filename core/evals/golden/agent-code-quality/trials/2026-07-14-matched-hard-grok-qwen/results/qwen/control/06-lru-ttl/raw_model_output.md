```python
"""Bounded LRU cache with optional TTL."""

from __future__ import annotations

import time
from collections import OrderedDict


class LruTtlCache:
    """A bounded LRU cache with optional TTL support.
    
    - capacity: Maximum number of live entries allowed.
    - ttl: Time-to-live in seconds for each entry. None means no expiration.
    - clock: A callable returning monotonic time (default: time.monotonic).
    """

    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError(f"capacity must be an integer >= 1, got {capacity}")
        
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock if clock is not None else time.monotonic
        
        # OrderedDict to maintain LRU order (most recent at end)
        # Values are tuples: (value, expiry_time_or_None)
        self._data: OrderedDict = OrderedDict()

    def _is_expired(self, key: any) -> bool:
        """Check if a key is expired. Returns False if TTL is disabled."""
        if self.ttl is None:
            return False
        if key not in self._data:
            return False
        _, expiry = self._data[key]
        if expiry is None:
            return False
        return self.clock() >= expiry

    def _remove_expired(self) -> None:
        """Remove all expired entries from the cache."""
        if self.ttl is None:
            return
        
        now = self.clock()
        keys_to_remove = []
        for key, (value, expiry) in self._data.items():
            if expiry is not None and now >= expiry:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._data[key]

    def _evict_lru(self) -> None:
        """Evict the least recently used entry (first item in OrderedDict)."""
        if self._data:
            self._data.popitem(last=False)

    def set(self, key, value) -> None:
        """Set a key-value pair in the cache.
        
        - If key exists and is not expired, update value and refresh TTL.
        - Before inserting new key, reap expired entries.
        - If at capacity after reaping, evict LRU entry.
        """
        now = self.clock()
        expiry = (now + self.ttl) if self.ttl is not None else None
        
        # If key already exists and is not expired, update it
        if key in self._data:
            _, old_expiry = self._data[key]
            # Check if it's expired; if so, treat as new insertion path
            if self.ttl is not None and old_expiry is not None and now >= old_expiry:
                del self._data[key]
            else:
                # Update value and refresh expiry, mark as most recent
                self._data[key] = (value, expiry)
                self._data.move_to_end(key)
                return
        
        # Key doesn't exist or was expired - need to insert new
        # First, reap all expired entries
        self._remove_expired()
        
        # If at capacity, evict LRU
        if len(self._data) >= self.capacity:
            self._evict_lru()
        
        # Insert new entry as most recently used
        self._data[key] = (value, expiry)

    def get(self, key):
        """Get a value from the cache.
        
        - Raises KeyError if missing or expired.
        - Marks key as most recently used if live.
        - Does NOT refresh TTL on get.
        """
        if key not in self._data:
            raise KeyError(key)
        
        # Check if expired
        if self._is_expired(key):
            del self._data[key]
            raise KeyError(key)
        
        # Mark as most recently used
        self._data.move_to_end(key)
        
        value, _ = self._data[key]
        return value

    def delete(self, key) -> bool:
        """Delete a key from the cache.
        
        - Returns True if key was present (even if expired).
        - Returns False if key was absent.
        """
        if key in self._data:
            del self._data[key]
            return True
        return False

    def __len__(self) -> int:
        """Return count of live (non-expired) entries.
        
        Reaps expired entries as part of computing length.
        """
        self._remove_expired()
        return len(self._data)

    def __contains__(self, key) -> bool:
        """Check if key is present and live.
        
        - Does not change recency order.
        - Does not refresh TTL.
        - May remove expired entry (treats as absent).
        """
        if key not in self._data:
            return False
        
        # Check if expired
        if self._is_expired(key):
            del self._data[key]
            return False
        
        return True
```