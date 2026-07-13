# Task: robust KEY=VALUE parser

## Deliverable

Implement `parse_kv(text: str) -> dict[str, str]` in `parse_kv.py`.

## Spec

- Input is a multi-line string of config text.
- Each **effective** line has the form `KEY=VALUE`.
- Keys: non-empty, trimmed; composed of letters, digits, underscore (`[A-Za-z0-9_]+`).
- Values: rest of the line after the first `=`; do **not** strip interior spaces;
  strip only a single optional pair of matching double quotes wrapping the whole value
  (`"hello world"` → `hello world`). Nested/unmatched quotes are left as-is.
- Blank lines are ignored.
- Lines whose first non-whitespace character is `#` are comments and ignored.
- Lines that are not blank, not comments, and do not match `KEY=VALUE` with a valid
  key are **errors**: collect them; after parsing, if any errors exist, raise
  `ValueError` with a message that includes how many invalid lines were found
  (e.g. contains the substring `invalid` and the count).
- If the same key appears more than once, **last wins**.
- Return a plain `dict` (insertion order may follow first-seen or last-seen; not graded).

## Constraints

- Edit only files under this package directory you were given (the starter tree).
- Do not add network calls or non-stdlib dependencies.
- Do not modify any `hidden_tests` directory if one appears in the tree.

## Done means

`parse_kv` meets the spec. Prefer writing a short note of what you verified.
