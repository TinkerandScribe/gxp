Goal: Implement `safe_join` that securely joins paths under a root directory.
Criteria:
1. Returns normalized absolute path.
2. Result must be strictly under or equal to the normalized absolute root.
3. Raises ValueError with "escape" in message if traversal attempts occur.
4. Handles empty parts by returning normalized root.
5. Uses only stdlib (`os.path`).

Out of scope: Symlink resolution beyond `os.path` defaults, non-stdlib dependencies.
Verify: Unit tests for valid joins, escape attempts via `..`, absolute paths in parts, and empty parts.

```python
"""Starter — unsafe join (no abspath, no escape check)."""

import os


def safe_join(root: str, *parts: str) -> str:
    """
    Join root with parts, ensuring the result stays under root.
    
    Args:
        root: The base directory.
        *parts: Path components to join.
        
    Returns:
        The normalized absolute path if it remains under root.
        
    Raises:
        ValueError: If the resulting path escapes the root directory.
    """
    # Normalize root to an absolute path
    abs_root = os.path.normpath(os.path.abspath(root))
    
    # Join and normalize the full path
    joined_path = os.path.join(abs_root, *parts)
    normalized_path = os.path.normpath(os.path.abspath(joined_path))
    
    # Check if the normalized path is under the root
    # It must start with abs_root + separator or be exactly abs_root
    if not (normalized_path == abs_root or 
            normalized_path.startswith(abs_root + os.sep)):
        raise ValueError("Attempted path traversal detected: escape from root")
        
    return normalized_path
```