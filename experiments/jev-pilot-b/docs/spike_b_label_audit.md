# Spike B — holdout label audit (gold `needs_review` → prior Jev `fail`)

Prior live Jev run (parent) scored these **holdout** rows `fail` while gold is
`needs_review`. This note reviews `data/labels.jsonl` only. Gold is **not**
rewritten: none of the eight are clearly wrong under the sheet’s own
convention (complete, evaluable absence → `fail`; partial / promised /
redacted / unreadable packet → `needs_review`).

**Patched labels file:** none. Inverse of this note: delete this file.

**Holdout re-score:** parent’s job with live Jev after merge. This spike does
not replay MCP. Offline structured-path scoring is `scripts/apply_rules_policy.py`.

## Summary

| id | gold (sheet) | prior Jev | recommendation | flip? |
|---|---|---|---|---|
| 042 | needs_review | fail | keep gold `needs_review` | no |
| 048 | needs_review | fail | keep gold `needs_review` | no |
| 083 | needs_review | fail | keep gold `needs_review` | no |
| 104 | needs_review | fail | keep gold `needs_review` | no |
| 105 | needs_review | fail | keep gold `needs_review` | no |
| 106 | needs_review | fail | keep gold `needs_review` | no |
| 107 | needs_review | fail | keep gold `needs_review` | no |
| 108 | needs_review | fail | keep gold `needs_review` | no |

**Counts:** keep 8 / flip 0.

Jev’s `fail` on these rows is the incomplete-evidence collapse this spike
addresses (`incomplete_evidence` path before Jev disposition), not a gold
error.

## Per-id review

### 042 — keep gold `needs_review`

- **source_tag / split:** `gxp` / holdout
- **criterion:** Two-layer verify ran: project suite then criterion-edge checks.
- **artifact:** Handoff claims Layer 2 “spot-checked a few rows” without naming
  which ISC or which commands.
- **rationale:** Claim is present but unnamed; cannot confirm the suite+edge
  walk ran or that it did not — same shape as calibrate 038/041 (thin handoff
  → `needs_review`), not a demonstrated skip.
- **Jev fail:** treats missing command names as criterion false.

### 048 — keep gold `needs_review`

- **source_tag / split:** `gxp` / holdout
- **criterion:** The filled label sheet has exactly 120 unique ids.
- **artifact:** PR text says N is “about 120”; attach is a spreadsheet
  screenshot, not a JSONL parse log.
- **rationale:** Approximate language plus an unparsed screenshot does not
  prove 120 unique ids and does not prove a different N — count is unread,
  not refuted.
- **Jev fail:** collapses “about 120” / screenshot into not-exactly-120.

### 083 — keep gold `needs_review`

- **source_tag / split:** `shop` / holdout
- **criterion:** `keep_alive` is set on the local model server session.
- **artifact:** Chat guess “keep_alive is probably 10 minutes”; no config key
  and no runtime ACK.
- **rationale:** Guess is not a config or ACK; session TTL is unknown. Matches
  calibrate 069 (`# keep_alive TBD`, no startup log → `needs_review`).
- **Jev fail:** reads “probably” as evidence the setting is absent.

### 104 — keep gold `needs_review`

- **source_tag / split:** `idea_gate` / holdout
- **criterion:** Evidence names at least one measured conversion count with
  identifiers.
- **artifact:** “~8-ish signups”, no window, no unique ids; author correctly
  refuses emails and provides no substitutes.
- **rationale:** Partial count plus a PII-safe gap is the 093 shape
  (`orders happened`, export declined → `needs_review`), not the empty-slogan
  fail class (088/090). Identifiers are missing *because* substitutes were
  not supplied yet — human, not automatic fail.
- **Jev fail:** treats missing identifiers as a completed negative.

### 105 — keep gold `needs_review`

- **source_tag / split:** `idea_gate` / holdout
- **criterion:** The packet includes a countable proof-of-product with N and a
  dated window.
- **artifact:** Window `2026-09-10..2026-09-16` present; N field blank; chart
  file is 0 bytes.
- **rationale:** Half-filled POP (window without N) matches 097 (count
  without window → `needs_review`). Packet is incomplete, not an explicit
  POP skip (103).
- **Jev fail:** missing N ⇒ criterion false instead of unread.

### 106 — keep gold `needs_review`

- **source_tag / split:** `idea_gate` / holdout
- **criterion:** Evidence names at least one measured conversion count with
  identifiers.
- **artifact:** Points at `metrics.json`; attach is `metrics.json.example`
  with all zeros and a TODO.
- **rationale:** Placeholder export is promised evidence, not a measured
  count — same as 095 (header-only CSV “will fill after the weekend” →
  `needs_review`). Zeros+TODO are not a completed traction claim.
- **Jev fail:** reads example zeros as “no conversions.”

### 107 — keep gold `needs_review`

- **source_tag / split:** `idea_gate` / holdout
- **criterion:** The packet includes a countable proof-of-product with N and a
  dated window.
- **artifact:** Whole traction section redacted as “PII risk”; no synthetic
  counts or ids left in place.
- **rationale:** Redaction hides the field; POP is unreadable, not shown to
  be absent. Sheet convention for PII-safe refusal without substitutes is
  `needs_review` (093/104), not fail.
- **Jev fail:** empty visible traction ⇒ fail.

### 108 — keep gold `needs_review`

- **source_tag / split:** `idea_gate` / holdout
- **criterion:** Evidence names at least one measured conversion count with
  identifiers.
- **artifact:** Three bullet user stories; no measurement; role names only
  (operator, reviewer).
- **rationale:** Wrong artifact type / no count is closer to fail neighbors
  (101 slogan, 102 stock dashboard) than the others, but still matches 099
  (landing + Stripe screenshots, no completion count → `needs_review`): the
  packet is present and obviously non-numeric, so a human confirms it is not
  a misfiled POP rather than auto-fail. **Not clearly wrong** — no flip.
- **Jev fail:** user stories ⇒ no conversion count ⇒ fail.

## Decision for gold files

Leave `data/labels.jsonl` and `data/labels.csv` unchanged. A patched sheet
would be added only for a clearly wrong gold; this audit has none.
