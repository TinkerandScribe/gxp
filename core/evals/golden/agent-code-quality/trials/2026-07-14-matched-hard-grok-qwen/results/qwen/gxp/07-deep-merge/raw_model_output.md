### Brief

**Goal**: Implement a robust `deep_merge` function that merges two dictionaries deeply without mutating inputs, supporting specific list merging strategies and key deletion via `None`.

**Binary Criteria**:
1. **Immutability**: Inputs (`base`, `override`) and their nested structures are never mutated; a completely new tree is returned.
2. **Key Deletion**: If `override` has a key with value `None`, that key is excluded from the result (even if present in `base`).
3. **Recursive Dict Merge**: If both values for a key are plain `dict`s, they are merged recursively using the same logic.
4. **List Mode "replace"**: If both values are lists and mode is "replace", the result is a deep copy of the override list.
5. **List Mode "extend"**: If both values are lists and mode is "extend", the result is base items (deep copied) followed by override items (deep copied).
6. **List Mode "unique"**: If both values are lists and mode is "unique", it behaves like "extend" but skips override items already present in the accumulated list (using `==`).
7. **Type Mismatch/Scalar Override**: If types differ or one is not a dict/list, the override value wins (deep copied if container).
8. **Error Handling**: Invalid `list_mode` raises `ValueError` containing the string "list_mode".

**Out of Scope**:
- Merging non-dict mapping types (e.g., `OrderedDict`, `Counter`) as dicts; they are treated as scalars/overrides.
- Deep uniqueness checks for nested structures within list items (only top-level item equality matters).

**Verification**:
- Unit tests covering all merge scenarios, mutation isolation, and error handling.
- Manual inspection of the recursive logic to ensure deep copying at every step.

### Implementation

```python
from __future__ import annotations
import copy
from typing import Any


def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    """
    Deeply merges `override` into `base`, returning a new dict.
    
    Args:
        base: The base dictionary.
        override: The dictionary to merge on top of base.
        list_mode: Strategy for merging lists. Options: "replace", "extend", "unique".
        
    Returns:
        A new dictionary containing the merged result.
        
    Raises:
        ValueError: If `list_mode` is not one of the supported modes.
    """
    valid_modes = {"replace", "extend", "unique"}
    if list_mode not in valid_modes:
        raise ValueError(f"Invalid list_mode: '{list_mode}'. Must be one of {valid_modes}")

    def _deep_copy(value: Any) -> Any:
        """Deep copy a value. Handles dicts, lists, and scalars."""
        if isinstance(value, dict):
            return {k: _deep_copy(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_deep_copy(item) for item in value]
        else:
            # Scalars are immutable, so sharing is safe. 
            # However, to be strictly "new tree" compliant for containers, 
            # we only copy containers. For scalars, identity is fine.
            return value

    def _merge_dicts(b: dict, o: dict) -> dict:
        """Recursively merge two dicts."""
        result = {}
        
        # Get all unique keys from both dicts
        all_keys = set(b.keys()) | set(o.keys())
        
        for key in all_keys:
            in_base = key in b
            in_override = key in o
            
            if in_base and not in_override:
                # Key only in base -> deep copy
                result[key] = _deep_copy(b[key])
            elif in_override and not in_base:
                # Key only in override -> deep copy
                val_o = o[key]
                if val_o is None:
                    # Explicitly skip None values from override to "delete" keys
                    continue
                result[key] = _deep_copy(val_o)
            else:
                # Key in both
                val_b = b[key]
                val_o = o[key]
                
                if val_o is None:
                    # Delete key if override value is None
                    continue
                
                if isinstance(val_b, dict) and isinstance(val_o, dict):
                    # Both are dicts -> recursive merge
                    result[key] = _merge_dicts(val_b, val_o)
                elif isinstance(val_b, list) and isinstance(val_o, list):
                    # Both are lists -> handle based on list_mode
                    if list_mode == "replace":
                        result[key] = _deep_copy(val_o)
                    elif list_mode == "extend":
                        merged_list = [_deep_copy(item) for item in val_b]
                        merged_list.extend(_deep_copy(item) for item in val_o)
                        result[key] = merged_list
                    elif list_mode == "unique":
                        merged_list = [_deep_copy(item) for item in val_b]
                        for item in val_o:
                            deep_copied_item = _deep_copy(item)
                            # Check if already present using == equality
                            if deep_copied_item not in merged_list:
                                merged_list.append(deep_copied_item)
                        result[key] = merged_list
                else:
                    # Type mismatch or scalars -> override wins
                    result[key] = _deep_copy(val_o)
                    
        return result

    return _merge_dicts(base, override)
```