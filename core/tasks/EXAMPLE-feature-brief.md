# Task brief

**Date:** 2026-01-15
**Task slug:** add-csv-export
**Workflow:** full

> Example brief. Shows what a filled-in GXP task brief looks like for a small feature.
> Replace with your own; delete the example briefs once you have real ones.

## Goal

Add a `GET /reports/export.csv` endpoint that streams the current report as CSV.

## Context

- Related files: `api/reports.py`, `api/serializers.py`, `tests/test_reports.py`
- Related PRs / tickets: #482 (report JSON endpoint this builds on)
- Relevant `.ai/rules/` entries: none new
- Relevant `.ai/failures/` entries: none
- Background: the JSON report endpoint already exists; this adds a CSV view over the same
  query. Large reports must stream, not buffer the whole result set in memory.

**Strategy/Model:** mid-tier coding model — well-scoped, one endpoint + tests, no
architectural decisions.

## Routing

- **privacy_class:** public
- **stakes:** low
- **engine_candidates:** [claude-code | cursor]
- **forbidden_engines:** []
- **exec_mode:** auto
- **output_contract:** new endpoint + passing tests, no schema change

## Ideal State Criteria

- [ ] `GET /reports/export.csv` returns HTTP 200 with `Content-Type: text/csv`.
- [ ] The CSV header row matches the JSON field order from `/reports`.
- [ ] A 50k-row report streams (peak memory stays under the existing request cap; verified
      by the streaming test asserting the response is chunked, not buffered).
- [ ] An unauthenticated request returns 401 (same auth as the JSON endpoint).
- [ ] `pytest tests/test_reports.py -q` exits 0.
- [ ] `ruff check api/` reports no new warnings.

## Out of scope

- XLSX / other export formats (separate ticket).
- Column selection / filtering query params.

## Verification plan

1. **Deterministic:** `pytest tests/test_reports.py -q`; `ruff check api/`.
2. **Behavioral:** hit the endpoint authenticated (200, correct header row) and
   unauthenticated (401); run the streaming test with a 50k-row fixture.
3. **Subjective:** confirm field order reads naturally and matches the JSON.

## Self-evaluation gate

- [x] **Completeness** — covers endpoint, auth, streaming, tests, lint.
- [x] **Ambiguity** — each criterion is binary.
- [x] **Scope trap** — XLSX and filtering explicitly parked.
- [x] **Verification** — every criterion has a concrete check.
- [x] **Approval gates** — none (additive, public, low-stakes).

## Approval gates

- (none)

## Dead ends

- (none)

## Handoff notes

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Rating entry reference:
