# Dogfood M7 retrospective — external host (2026-07-24)

**Status:** complete (usefulness test, not code-quality science)  
**Host class:** private single-user Flask + SQLite business-management app (operator-named; details stay on host)  
**Public artifacts only:** this note + closed brief under `core/tasks/`. No customer data, no secrets, no absolute user paths.

## What was already true on the host

- `.ai/` installed with a filled `PROGRAM.md` (north-star constraints: money/tax/dates first, single-user offline, no JS framework, route-file line budget).
- Canonical loop in host `.ai/workflow.md` plus Cursor rule; task briefs under host `.ai/tasks/`.
- Deterministic verify floor: syntax/`ast.parse` of app + routes, `from app import app`, host smoke script (key GET 200s), unit tests.
- **Eleven** host rating lines (May 2026 campaign + 2026-07-24 launcher): mix of full and lightweight; several full runs recorded 8/8 Ideal State Criteria met.

Representative cycles (host-private briefs/ratings; summarized only):

| Cycle type | Outcome (host ledger) | Usefulness signal |
|---|---|---|
| Product feature (quote presets + tax math) | 8/8 full | Binary criteria forced cent-level HST probes before "done" |
| Security hardening (CSRF) | 8/8 full | Gate held until tests green; no drive-by scope |
| Ops polish (dotenv, desktop launcher) | 4/4 lightweight | Lightweight variant matched trivial surface area |
| Weekly refine | pass | Host already flagged self-grading / small-N soft spots |

## What GXP helped

1. **PROGRAM.md as a hard constraint surface** — agents optimized for money/tax correctness and "no auth / no SPA / offline" instead of inventing platform work.
2. **Binary Ideal State Criteria** — especially on money paths (explicit HST arithmetic checks), reduced "looks fine" completions.
3. **Full vs lightweight** — trivial launcher/dotenv work stayed small; multi-file product work used the full loop.
4. **Deterministic verify first** — AST/import/smoke/unit tests before subjective review matched the methodology's Phase 5 order.
5. **Ratings + refine** — host weekly refine already proposed mandatory eval probes and design-criterion checks (pressure that later shows up in core Verification ladder thinking).

## What hurt / friction

1. **Schema drift on the host ledger** — early host ratings used legacy field names (`task_id`, `date`, `ideal_state_met`) rather than core `ts` / `task` / `criteria_met`. Still useful locally; harder to share tooling with `validate-ratings-chain.py`.
2. **One-shot install, weak refresh habit** — host workflow did not automatically pick up later core improvements (e.g. named Verification ladder, gxp-refine surfaces). `PROGRAM.md` and ratings correctly preserved; **workflow freshness** was operator-driven and easy to skip.
3. **Self-graded ratings** — honest intent, but no independent review; host refine already called this out.
4. **Private host** — correct for secrets, but means public gxp can only publish sanitized retrospectives (this file), not raw host briefs.

## One change proposal for gxp core/adapters

**Document and script a "refresh workflow only" host upgrade path:** preserve `.ai/PROGRAM.md` and `.ai/ratings.jsonl`, update `.ai/workflow.md` (and optional Cursor rule) from a pinned gxp version, and record `Last synced from gxp: vX.Y.Z` in `PROGRAM.md`. Pair with a short "legacy ratings fields → core schema" note so long-lived hosts can dual-write or migrate without breaking history.

(Installer already preserves user files; the gap is operator-facing recipe + version stamp, not a new subsystem.)

## M7 criteria checklist

- [x] 1. Host `.ai/workflow.md` + real `PROGRAM.md` verify commands  
- [x] 2. Task briefs with 4–8 binary ISC on host  
- [x] 3. Implementations on host main; deterministic verify first  
- [x] 4. Rating lines on host `.ai/ratings.jsonl`  
- [x] 5. This retrospective (helped / hurt / one proposal; no secrets)  
- [x] 6. Public path under `core/evals/`; no host secrets  

## Explicit non-claims

- Does **not** reopen the M6 marketing claim gate.  
- Does **not** assert multi-model code-quality lift.  
- Usefulness evidence only: GXP was runnable and valuable on a real private product host over multiple cycles.
