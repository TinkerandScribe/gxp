# Failure capture

**Date:** 2026-07-13
**Task / context:** Appending a rating line to `core/ratings.jsonl` via a bash
heredoc during the `review-external-audit-fix-plan` run.

## Expected

The appended line is valid JSON (schema line's contract: one JSON object per line).

## Actual

The line contained `\$` — written in the heredoc to protect `$YELLOW` from shell
expansion — which is an **invalid JSON escape**. `json.loads` failed:
`Invalid \escape: line 1 column 825`.

## Root cause

Two escaping layers with different rules: a quoted heredoc (`<<'EOF'`) already
suppresses shell expansion, so the `\` before `$` was unnecessary and landed
literally in the file; JSON accepts `\"`, `\\`, `\n`… but not `\$`. Writing JSON
through a shell quoting layer invites exactly this class of corruption.

## Detection

Validate every ratings append immediately: parse the last line (or whole file) with
a real JSON parser right after writing. The corruption was caught this way within
seconds — the check is the reason the ledger stayed clean.

## Resolution

Repaired the one byte; validated all lines parse. Subsequent appends use the
editor/Write tooling (no shell quoting layer) instead of heredocs.

## Prevention

- Append JSONL entries with a file-editing tool or a JSON-emitting program
  (`jq -c`, `json.dump`), never through shell heredocs/echo with hand-escaped
  content.
- Keep the post-append parse check as a standing habit (a future
  `verify.sh` JSONL-validation step would make it automatic — see ROADMAP
  Milestone 2 hash-chain item, which subsumes it).

## Follow-up

- [ ] When the hash-chained ledger lands (ROADMAP Milestone 2), include a
  parse-all-lines step in `verify.sh` so malformed appends fail verification.

## Repeatable?

Yes — any agent or contributor appending ledger lines through a shell is one
mis-escaped `$` away from a corrupt ledger.
