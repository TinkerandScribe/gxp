# HANDOFF — safe_join (trial 10)

## What changed

- **`safe_join.py`:** Replaced the unsafe `os.path.join` stub with a full implementation:
  - Normalizes `root` to `os.path.abspath(os.path.normpath(root))`.
  - With no `parts`, returns that absolute root.
  - Joins `parts`, then `normpath` + `abspath`.
  - Uses `os.path.commonpath` to ensure the result stays under `abs_root`; raises `ValueError("path would escape root")` on escape (different drives on Windows also raise).

## What was verified

Inline Python checks (run from shell, not committed):

- Empty `parts` returns normalized absolute root.
- Benign multi-segment join matches expected absolute path.
- In-root `..` normalization (`sub/../sub/file`) succeeds.
- `..` above root raises `ValueError` with `escape` in message.
- Absolute path segment outside root raises `ValueError` with `escape` in message.
- Sibling-directory escape (`root` → `root2`) is rejected.

## What is not done

- Official hidden test suite not run (per trial protocol).
- No symlink-specific behavior beyond stdlib `abspath`/`normpath`.

## Files in DEST

| File | Role |
|------|------|
| `BRIEF.md` | Task brief and ISC |
| `safe_join.py` | Implementation |
| `HANDOFF.md` | This file |
