# Task: safe_join under a root

## Deliverable

Implement `safe_join(root: str, *parts: str) -> str` in `safe_join.py`.

## Spec

- Join `root` with zero or more path `parts` using `os.path` semantics, then
  return the **normalized absolute** path.
- The result **must** stay under the normalized absolute `root` (as a path
  prefix with a path separator, or equal to root).
- If any part would escape the root via `..` or absolute segments, raise
  `ValueError` whose message contains `escape` (case-insensitive).
- Empty `parts` → normalized absolute root.
- Do not follow symlinks beyond what `os.path.abspath` / `normpath` do (no
  extra symlink policy required).
- Stdlib only.

## Constraints

- Edit only the starter tree; no hidden-test edits.

## Done means

All hidden tests pass.
