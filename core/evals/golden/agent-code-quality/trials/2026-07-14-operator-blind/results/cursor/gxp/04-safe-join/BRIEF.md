# BRIEF — safe_join (trial 10)

## Goal

Implement `safe_join(root, *parts)` in `safe_join.py` so joined paths stay under a
normalized absolute root, using stdlib `os.path` only.

## Ideal State Criteria

1. **ISC-1:** `safe_join(root)` with no parts returns `os.path.abspath(os.path.normpath(root))`.
2. **ISC-2:** `safe_join(root, "a", "b")` returns the normalized absolute path of joining root with parts.
3. **ISC-3:** Joining parts that normalize inside root (e.g. `"sub", "..", "file"`) succeeds and stays under root.
4. **ISC-4:** Joining `..` segments or absolute path parts that leave root raises `ValueError`.
5. **ISC-5:** Every escape `ValueError` message contains the substring `escape` (case-insensitive).
6. **ISC-6:** A result equal to root is allowed; a result that merely shares a string prefix but is not under root (e.g. `/tmp/root` vs `/tmp/root2`) is rejected.
7. **ISC-7:** Implementation uses only the Python stdlib (no third-party imports).

## Out of scope

- Custom symlink resolution beyond `os.path.abspath` / `normpath`.
- Files other than `safe_join.py`, `BRIEF.md`, and `HANDOFF.md` in DEST.
- Running official hidden tests or `score_trial.py`.

## Verification plan

1. Import `safe_join` from DEST and run a small inline Python script covering:
   - empty parts → absolute root
   - benign nested join
   - in-root `..` normalization
   - escape via `..` above root
   - escape via absolute segment
   - `ValueError` message contains `escape`
2. Confirm no extra files created in DEST.

## Strategy/Model

Cursor agent (current session); single-file stdlib task with clear spec — full GXP workflow, minimal implementation.
