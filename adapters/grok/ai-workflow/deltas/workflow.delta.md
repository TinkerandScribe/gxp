---
title: Grok-Optimized Workflow (v1.1)
tool_name: Grok
blurb: This is a **Grok-optimized** adaptation of the core AI Workflow methodology.
---

## Strengths

- Excellent tool use and function calling
- Strong long-context reasoning
- Good at explicit uncertainty handling
- Capable of complex multi-step planning when given clear structure

## Pre-phase

## Grok Build Strategy Selection (Prototype — see `instructions/strategy-selection.md`)

**For sessions running in Grok Build (with access to Composer 2.5 and subagents):**

After (or as part of) Phase 0, perform lightweight strategy classification using GXP language before committing to a model or delegation style.

See the full guidance in `instructions/strategy-selection.md`.

Quick decision matrix (binary criteria style):

- Genuine ambiguity / architecture / research / planning heavy → native Grok + plan mode (or grok-native-planner persona).
- Coherent multi-file agentic coding → Composer 2.5 (composer-coder persona / subagent).
- Visual IDE / Cursor ecosystem → Cursor Composer handoff artifact (GXP brief + paste prompt).
- Small reversible terminal/debug work → fast native Grok model.

**Always:** log the decision with justification tied to Ideal State Criteria; note capability; plan scoped context for any subagent/handoff.

## Notes — Phase 0

Use `read_file` and directory listing tools aggressively. On large repos, start from files named in the brief, then expand with search. Resolve uncertainty with tools rather than guessing.

**Thin / underspecified operator ask (evidence-backed):** If the request does not
already contain about 4+ binary criteria, or the goal is multi-factor and vague:

1. **Do not implement yet.**  
2. Open `.ai/PROGRAM.md`, `rules/`, and `failures/` when present (or state they are
   missing).  
3. Write Ideal State Criteria that name edges smoke tests often miss (fail-closed,
   isolation, state transitions, multi-key, etc.).  
4. Cite any applicable failure notes in the brief before coding.

Frontier models can code well without this; they still skip Phase 0 under short asks
and leave multi-factor bugs. Phase 0 is the fix for that failure mode.

## Notes — Phase 0.5

Prefer tool-backed verification of capability (what connectors exist) over assuming models. Re-evaluate engine choice at the Phase 4 anti-loop gate.

## Notes — Phase 1

When writing verification plans, name the **tools** you will use to make each check deterministic.

## Notes — Phase 2

Be strict on Verification and Approval gates. If a criterion cannot be checked mechanically, say so and propose how you will handle uncertainty.

**Lightweight vs full (Grok Build):** Use full workflow when the change is multi-file
or multi-constraint, or when project smoke/public verify is thin relative to the
criteria. Lightweight is OK for single-file trivial edits with a clear strong verify
path—evals show full GXP process adds little correctness when the prompt and tools
already force best-effort multi-factor work.

## Notes — Phase 3

Explore the codebase with tools while implementing. Prefer reading source over relying on memory.

## Notes — Phase 5

1. Deterministic checks first (type/lint/test/build) via tools with real output.
2. Behavioral checks using execution/REPL tools when available.
3. Subjective review only after the above.

**Weak green (do not stop early):** After any suite exits 0 (`unittest`, `pytest`,
build, etc.), re-walk Ideal State Criteria that thin smoke tests miss. On multi-file
or multi-constraint tasks, run a **second layer** (extra asserts, a focused script, or
criterion-by-criterion tool checks) before claiming done.

**Anti-pattern:** “Public tests passed” as the only done signal on multi-module or
fail-closed / state-machine work. That failure mode is exactly where GXP showed large
correctness lifts in evals.

## Notes — Phase 6

Be honest. Low ratings on difficult tasks are valuable data.

## Notes — Phase 7

When capturing failures, note whether better tool use or context loading could have prevented the issue.

## Closing

**Remember:** This is an optimized *adaptation*, not a replacement. The source of truth remains in `core/`. Use `../sync/check-core.sh` frequently, especially before important work.
