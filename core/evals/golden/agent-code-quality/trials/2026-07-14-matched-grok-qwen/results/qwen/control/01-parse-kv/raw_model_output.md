```python
"""Robust KEY=VALUE parser implementation."""

import re


def parse_kv(text: str) -> dict[str, str]:
    """Parse a multi-line string of config text into a dictionary.
    
    Args:
        text: A multi-line string containing KEY=VALUE pairs, comments, and blank lines.
        
    Returns:
        A dictionary mapping keys to values. If duplicate keys exist, the last value wins.
        
    Raises:
        ValueError: If there are any invalid lines (non-blank, non-comment lines that don't
                    match the KEY=VALUE format with a valid key). The error message includes
                    the count of invalid lines found.
    """
    result = {}
    errors = []
    
    # Regex for valid keys: letters, digits, underscores only, non-empty
    key_pattern = re.compile(r'^[A-Za-z0-9_]+$')
    
    for line_num, raw_line in enumerate(text.splitlines(), start=1):
        # Strip leading/trailing whitespace for processing
        stripped = raw_line.strip()
        
        # Skip blank lines
        if not stripped:
            continue
            
        # Skip comment lines (first non-whitespace char is #)
        if stripped.startswith('#'):
            continue
        
        # Check if line contains '='
        if '=' not in stripped:
            errors.append((line_num, raw_line))
            continue
        
        # Split on first '=' only
        key_part, value_part = stripped.split('=', 1)
        
        # Trim the key
        key = key_part.strip()
        
        # Validate key is non-empty and matches allowed characters
        if not key or not key_pattern.match(key):
            errors.append((line_num, raw_line))
            continue
        
        # Process value: strip only a single optional pair of matching double quotes
        # wrapping the whole value. Do not strip interior spaces.
        value = value_part
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            # Remove the surrounding quotes
            value = value[1:-1]
        
        result[key] = value
    
    # If there were any errors, raise ValueError with count
    if errors:
        error_lines = [f"line {num}: {content}" for num, content in errors]
        raise ValueError(
            f"Found {len(errors)} invalid line(s):\n" + "\n".join(error_lines)
        )
    
    return result
```