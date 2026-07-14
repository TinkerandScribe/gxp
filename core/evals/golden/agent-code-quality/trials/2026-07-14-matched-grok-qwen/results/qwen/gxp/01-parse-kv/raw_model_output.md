**Binary Criteria:**
1. **Goal**: Implement `parse_kv` to parse multi-line config strings into a dictionary, handling comments, blank lines, and specific quoting rules.
2. **Criteria**:
   - Keys must match `[A-Za-z0-9_]+`.
   - Values preserve interior spaces but strip outer matching double quotes if present.
   - Invalid lines (non-blank, non-comment, no valid key=value) trigger a `ValueError` with count.
   - Duplicate keys result in the last value winning.
3. **Out of Scope**: Network calls, external dependencies, modifying hidden tests.
4. **Verify**: The function raises `ValueError` on invalid syntax and correctly parses valid lines with quote stripping.

```python
import re

def parse_kv(text: str) -> dict[str, str]:
    """
    Parse a multi-line string of KEY=VALUE pairs into a dictionary.
    
    - Keys are trimmed and must match [A-Za-z0-9_]+.
    - Values are the rest of the line after the first '='.
    - Outer matching double quotes on values are stripped.
    - Blank lines and comments (starting with #) are ignored.
    - Invalid lines raise ValueError with a count of errors.
    - Duplicate keys: last value wins.
    """
    result = {}
    invalid_lines = []
    
    for line in text.splitlines():
        stripped_line = line.strip()
        
        # Ignore blank lines
        if not stripped_line:
            continue
            
        # Ignore comments
        if stripped_line.startswith('#'):
            continue
            
        # Check for '=' separator
        if '=' not in stripped_line:
            invalid_lines.append(stripped_line)
            continue
            
        key_part, value_part = stripped_line.split('=', 1)
        key = key_part.strip()
        
        # Validate key format: non-empty and only alphanumeric/underscore
        if not re.fullmatch(r'[A-Za-z0-9_]+', key):
            invalid_lines.append(stripped_line)
            continue
            
        # Process value: strip outer matching double quotes if present
        value = value_part
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            
        result[key] = value
        
    if invalid_lines:
        raise ValueError(f"Found {len(invalid_lines)} invalid lines")
        
    return result
```