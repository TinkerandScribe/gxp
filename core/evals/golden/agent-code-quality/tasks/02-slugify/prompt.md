# Task: URL slugify

## Deliverable

Implement `slugify(text: str) -> str` in `slugify.py`.

## Spec

- Lowercase the string.
- Replace any run of characters that are **not** ASCII letters or digits with a single `-`.
- Strip leading/trailing `-`.
- Collapse multiple `-` to one (already implied by “run”).
- Empty / all-separator input → `""`.
- Unicode letters: strip them (not kept). Only `[a-z0-9]` remain after processing.
- Do not depend on third-party packages.

## Constraints

- Edit only the starter tree you were given.
- Do not modify hidden tests.

## Done means

`slugify` meets the spec; note how you verified.
