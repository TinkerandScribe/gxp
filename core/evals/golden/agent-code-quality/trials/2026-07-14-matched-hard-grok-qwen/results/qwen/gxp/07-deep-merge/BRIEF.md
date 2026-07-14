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
