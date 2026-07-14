from __future__ import annotations
import copy


def deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict:
    """
    Return a new dict that is base deeply updated by override.
    
    Args:
        base: The base dictionary.
        override: The override dictionary.
        list_mode: How to handle lists when both values are lists.
                  Options: "replace", "extend", "unique".
    
    Returns:
        A new merged dictionary.
    
    Raises:
        ValueError: If list_mode is not one of the supported modes.
    """
    # Validate list_mode early
    if list_mode not in ("replace", "extend", "unique"):
        raise ValueError(f"Invalid list_mode: {list_mode!r}. Must be 'replace', 'extend', or 'unique'.")
    
    result = {}
    
    # Get all keys from both dicts
    all_keys = set(base.keys()) | set(override.keys())
    
    for key in all_keys:
        in_base = key in base
        in_override = key in override
        
        if in_base and not in_override:
            # Key only in base -> deep copy
            result[key] = _deep_copy(base[key])
        elif in_override and not in_base:
            # Key only in override -> deep copy
            result[key] = _deep_copy(override[key])
        else:
            # Key in both
            b_val = base[key]
            o_val = override[key]
            
            if o_val is None:
                # Delete the key (omit from result)
                continue
            elif isinstance(b_val, dict) and isinstance(o_val, dict):
                # Both are dicts -> recursively merge
                result[key] = deep_merge(b_val, o_val, list_mode=list_mode)
            elif isinstance(b_val, list) and isinstance(o_val, list):
                # Both are lists -> combine by list_mode
                result[key] = _merge_lists(b_val, o_val, list_mode)
            else:
                # Override wins -> deep copy override value
                result[key] = _deep_copy(o_val)
    
    return result


def _deep_copy(obj):
    """Deep copy an object. Uses copy.deepcopy for containers."""
    if isinstance(obj, dict):
        return {k: _deep_copy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_deep_copy(item) for item in obj]
    else:
        # For non-container values (immutables), we can just return them as-is
        # since they are immutable and safe to share.
        return obj


def _merge_lists(base_list, override_list, list_mode):
    """Merge two lists according to the specified mode."""
    if list_mode == "replace":
        # Result is a deep copy of override list
        return [_deep_copy(item) for item in override_list]
    elif list_mode == "extend":
        # Deep copy base items, then deep copy append all override items
        result = [_deep_copy(item) for item in base_list]
        result.extend(_deep_copy(item) for item in override_list)
        return result
    elif list_mode == "unique":
        # Like extend, but skip override item if already present under == equality
        result = [_deep_copy(item) for item in base_list]
        for item in override_list:
            copied_item = _deep_copy(item)
            # Check if this item is already in result using == equality
            if not any(copied_item == existing for existing in result):
                result.append(copied_item)
        return result
    else:
        # This should never be reached due to early validation, but just in case
        raise ValueError(f"Invalid list_mode: {list_mode!r}")
