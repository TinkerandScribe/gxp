"""LruTtlCache: Bounded LRU cache with optional TTL."""

from __future__ import annotations

import time
from collections import OrderedDict


class LruTtlCache:
    """
    A Least Recently Used (LRU) cache with optional Time-To-Live (TTL) expiration.
    
    - Capacity is strictly enforced.
    - TTL is checked on access and before new insertions.
    - LRU order is updated on both set and get operations.
    - TTL is only refreshed on set operations.
    """

    def __init__(self, capacity: int, ttl: float | None = None, *, clock=None):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError(f"capacity must be an integer >= 1, got {capacity}")
        
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock if clock is not None else time.monotonic
        
        # OrderedDict maintains insertion order. 
        # We move items to the end on access to simulate LRU (end = most recent).
        # Value stored: tuple of (value, expiry_timestamp) or (value, None) if no TTL.
        self._data: OrderedDict = OrderedDict()

    def _is_expired(self, key: any) -> bool:
        """Check if a key is expired. Returns False if key doesn't exist or has no TTL."""
        if key not in self._data:
            return False
        
        value, expiry = self._data[key]
        
        # If ttl is None, entries never expire
        if self.ttl is None:
            return False
            
        if expiry is None:
            return False
            
        return self.clock() >= expiry

    def _reap_expired(self) -> None:
        """Remove all expired entries from the cache."""
        if self.ttl is None:
            return

        keys_to_remove = []
        for key in self._data:
            if self._is_expired(key):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._data[key]

    def set(self, key, value) -> None:
        """
        Store value under key.
        - If key exists and is not expired: update value, refresh TTL, mark as MRU.
        - If key exists but is expired: treat as new insert (reap first).
        - Before inserting a NEW key: reap all expired entries.
        - If at capacity after reaping: evict LRU live entry.
        """
        
        # Check if key already exists and is valid (not expired)
        if key in self._data:
            # Check expiration explicitly for existing keys
            if self._is_expired(key):
                # Treat as new insert logic below, but first remove the expired one
                del self._data[key]
            else:
                # Update value and refresh TTL
                now = self.clock()
                expiry = now + self.ttl if self.ttl is not None else None
                self._data[key] = (value, expiry)
                # Move to end to mark as Most Recently Used
                self._data.move_to_end(key)
                return

        # If we are here, it's a new key or the old one was expired/removed.
        
        # 1. Reap all currently expired entries before inserting new key
        self._reap_expired()

        # 2. Check capacity and evict LRU if necessary
        if len(self._data) >= self.capacity:
            # Popitem(last=False) removes the first item (Least Recently Used)
            self._data.popitem(last=False)

        # 3. Insert new key
        now = self.clock()
        expiry = now + self.ttl if self.ttl is not None else None
        self._data[key] = (value, expiry)
        # New inserts are most recently used (OrderedDict appends to end by default)

    def get(self, key):
        """
        Retrieve value for key.
        - If missing or expired: remove if present, raise KeyError.
        - If live: return value and mark as MRU.
        """
        if key not in self._data:
            raise KeyError(key)

        # Check expiration
        if self._is_expired(key):
            del self._data[key]
            raise KeyError(key)

        # Retrieve value
        value, _ = self._data[key]
        
        # Mark as Most Recently Used
        self._data.move_to_end(key)
        
        return value

    def delete(self, key) -> bool:
        """
        Remove key from cache.
        - Returns True if key was present (even if expired).
        - Returns False if key was absent.
        """
        if key in self._data:
            del self._data[key]
            return True
        return False

    def __len__(self) -> int:
        """
        Return count of live (non-expired) entries.
        Reaps expired entries as part of computing length.
        """
        self._reap_expired()
        return len(self._data)

    def __contains__(self, key) -> bool:
        """
        Check if key is present and live.
        - Does not change recency order.
        - Does not refresh TTL.
        - Removes expired entry if found.
        """
        if key not in self._data:
            return False
        
        # Check expiration
        if self._is_expired(key):
            del self._data[key]
            return False
            
        return True
