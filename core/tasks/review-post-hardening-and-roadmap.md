# Task brief — review post-hardening work + next roadmap

**Date:** 2026-07-13  
**Slug:** review-post-hardening-and-roadmap  
**Workflow:** full (review + docs; no feature migration)  

## Goal

Review shipped verification-hardening / eval / P2-4 work against evidence on disk,
then update `ROADMAP.md` with the best next sequence and write pickup briefs for
each open item (binary criteria, no implementation of those items in this task).

## Context

- Verification-hardening M0–M3: **done** (see prior ROADMAP section).  
- P2-4 hybrid generator + multi-seed eval campaign + v1.3.0 released earlier.  
- Operator rule: **do not push tags/releases unless asked**.  
- Residual items (not on old roadmap): shared Python probe, core `4–8` prose,
  grow eval tasks, blind multi-model campaign, external dogfood, optional Cursor
  generator.

## Ideal State Criteria

- [x] 1. Written review verdict: what is solid vs what claims overreach.  
- [x] 2. `ROADMAP.md` keeps completed hardening as archive and adds sequenced **next**
  milestones with dependencies and status `brief-ready` / deferred.  
- [x] 3. One brief per actionable next item under `core/tasks/` with 4–8 ISC,
  out-of-scope, verification plan, Depends-on.  
- [x] 4. `verify.sh` exit 0 after docs; no secrets; no release/tag.  
- [x] 5. Honest rating in `core/ratings.jsonl`.

## Out of scope

- Implementing polish, eval growth, multi-model runs, or dogfood.  
- Creating GitHub releases/tags.

## Review verdict (evidence-based)

### Solid

| Area | Evidence |
|---|---|
| Drift is checkable | Structural floor; CI negative Phase-8 test; no whole-file workflow allowlist |
| Markers / CI / install polish | Live SHA markers, auto-bump, verify matrix, dry-run, subshell fix |
| Doc dedup hybrid | Generator + deltas + CI `--check`; Cursor/Cowork intentionally separate |
| Harness reliability | Selftest green on Grok, Cursor, Claude; starter &lt; reference on 3 tasks |
| Process enforcement story | Multi-seed: GXP verify-to-green 9/9 vs incomplete one-shots |

### Overreach / limits

| Claim | Reality |
|---|---|
| “Agents write better code under GXP” | **Not proven** for blind multi-model agents; multi-seed fixtures are in-repo |
| Hash-chained ledger | Optional fields + validator; historical lines unchained |
| Workshop quarantine | N/A — artifact never in public tree |

### Best way to proceed (sequencing rationale)

1. **Small tooling polish first** — shared Python probe + core `4–8` prose remove
   known footguns and generator inject; low risk; make later work smoother.  
2. **Grow eval task set next** — reduce ceiling effects and task narrowness before
   spending operator time on multi-model runs.  
3. **Blind multi-model campaign** — only after (2); uses independent agents; highest
   value for the open scientific question.  
4. **External dogfood** — parallel product track; does not block (1)–(3) but should
   not preempt evidence work if the goal is “prove GXP.”  
5. **Cursor on generator** — defer until text-adapter generator is stable in the wild;
   Cursor’s `rule.mdc` + Phase -1 are a different shape (high risk, low urgency).

## Verification plan

Read ROADMAP + briefs exist; `bash scripts/verify.sh`; no tag/push release.
