# Task: deep_merge

## Deliverable

Implement `deep_merge(base: dict, override: dict, *, list_mode: str = "replace") -> dict`
in `deep_merge.py`.

## Spec

Return a **new** dict that is `base` deeply updated by `override`.

### Mutation

- **Never** mutate `base` or `override` (or any nested containers found in them).
- Always return a newly constructed tree (new dicts/lists as needed).

### Mapping rules (per key in the union of keys)

Let `b = base.get(key, missing)`, `o = override.get(key, missing)`.

1. Key only in `base` → deep-copy that value into the result.  
2. Key only in `override` → deep-copy that value into the result.  
3. Key in both:
   - If `o is None` → **delete** the key (omit from result). This is the only
     way to remove a key present in `base`.  
   - Else if both `b` and `o` are `dict` (plain `dict` only — not mappings of
     other types) → recursively `deep_merge(b, o, list_mode=list_mode)`.  
   - Else if both are `list` → combine by `list_mode` (below).  
   - Else → override wins: deep-copy `o` (scalar, list over dict, dict over
     list, mismatched types, etc.).

### `list_mode` (only when both values are lists)

| Mode | Behavior |
|------|----------|
| `"replace"` | result list is a deep-copy of override list |
| `"extend"` | deep-copy base list items, then deep-copy append all override items |
| `"unique"` | like extend, but skip an override item if it is already present under
  `==` equality in the result so far (base items first). Only top-level list
  element equality — no deep unique of nested structures beyond `==`. |

- Unknown `list_mode` → raise `ValueError` whose message contains `list_mode`.

### Deep-copy

- Nested `dict` / `list` values must be copied so later mutation of inputs or
  outputs does not cross-contaminate (shallow container copy is insufficient
  when nested).
- Non-container values may be shared (immutables).

### Constraints

- Stdlib only (`copy` module allowed).
- Edit only the starter tree; no hidden-test edits.
- `base` / `override` roots are always plain `dict` in tests.

## Done means

Hidden tests pass.
