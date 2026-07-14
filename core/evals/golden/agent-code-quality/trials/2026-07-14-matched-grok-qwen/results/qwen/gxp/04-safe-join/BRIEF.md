Goal: Implement `safe_join` that securely joins paths under a root directory.
Criteria:
1. Returns normalized absolute path.
2. Result must be strictly under or equal to the normalized absolute root.
3. Raises ValueError with "escape" in message if traversal attempts occur.
4. Handles empty parts by returning normalized root.
5. Uses only stdlib (`os.path`).

Out of scope: Symlink resolution beyond `os.path` defaults, non-stdlib dependencies.
Verify: Unit tests for valid joins, escape attempts via `..`, absolute paths in parts, and empty parts.
