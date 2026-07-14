# Brief — parse_kv

**Strategy/Model:** Cursor agent in DEST only; single-file stdlib parser (comfortable margin for this L3 task).

**Routing:** Stay in current tool; no handoff.

## Goal

Implement `parse_kv(text: str) -> dict[str, str]` in `parse_kv.py` so multi-line `KEY=VALUE` config parses per the task spec (comments, blanks, quote unwrap, last-wins, invalid-line `ValueError`).

## Context

- Task prompt: `core/evals/golden/agent-code-quality/tasks/01-parse-kv/prompt.md`
- Editable root: this DEST (starter `parse_kv.py` is intentionally wrong)
- Phase 0: DEST has no local PROGRAM/rules; constraints come from the task prompt and arm `gxp.md` (no ratings/helpers in DEST)

## Ideal State Criteria

1. `parse_kv("a=1\nb=2")` returns `{"a": "1", "b": "2"}` (type `dict`).
2. Blank lines and lines whose first non-whitespace char is `#` are ignored (no error).
3. Keys are trimmed and accepted only if non-empty and match `[A-Za-z0-9_]+`; values are the substring after the first `=` with no interior stripping except optional matching outer `"..."` when the whole value is wrapped and interior has no `"`.
4. Duplicate keys: last assignment wins.
5. Any non-blank, non-comment line that is not valid `KEY=VALUE` is counted; after the full parse, `ValueError` is raised and `str(exc)` contains both `invalid` and the decimal count of such lines.
6. No network calls and no non-stdlib imports in `parse_kv.py`.

## Out of scope

- Official hidden tests / scorer
- Helper scripts (`verify_adhoc.py`), `ratings.jsonl`, extra packages
- Changing files outside DEST

## Verification plan

1–5: Run deterministic inline Python assertions in-shell against the criteria (happy path, comments/blanks, quotes/spaces, duplicates, invalid lines + message).
6: Inspect imports in `parse_kv.py`.
