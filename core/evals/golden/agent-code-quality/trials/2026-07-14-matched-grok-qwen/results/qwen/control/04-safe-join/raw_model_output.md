```python
"""Safe path join that prevents directory traversal escapes."""

import os


def safe_join(root: str, *parts: str) -> str:
    """Join root with parts, ensuring the result stays under root.

    Args:
        root: The base directory.
        *parts: Path components to join under root.

    Returns:
        The normalized absolute path, guaranteed to be under root.

    Raises:
        ValueError: If any part would cause the result to escape root.
    """
    # Normalize and resolve root to an absolute path
    root_abs = os.path.abspath(os.path.normpath(root))

    # Join with parts and normalize the result
    joined = os.path.join(root_abs, *parts)
    result = os.path.abspath(os.path.normpath(joined))

    # Determine the prefix that valid children must start with.
    # If root_abs already ends with a separator (e.g. "/" on Unix or "C:\\" on Windows),
    # use it as-is; otherwise append the separator to avoid false negatives.
    if root_abs.endswith(os.sep):
        prefix = root_abs
    else:
        prefix = root_abs + os.sep

    # The result must either equal root exactly or be a proper child of root
    if result != root_abs and not result.startswith(prefix):
        raise ValueError("Attempted path escape detected")

    return result
```