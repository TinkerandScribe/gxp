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

## Notes — Phase 0.5

Prefer tool-backed verification of capability (what connectors exist) over assuming models. Re-evaluate engine choice at the Phase 4 anti-loop gate.

## Notes — Phase 1

When writing verification plans, name the **tools** you will use to make each check deterministic.

## Notes — Phase 2

Be strict on Verification and Approval gates. If a criterion cannot be checked mechanically, say so and propose how you will handle uncertainty.

## Notes — Phase 3

Explore the codebase with tools while implementing. Prefer reading source over relying on memory.

## Notes — Phase 5

1. Deterministic checks first (type/lint/test/build) via tools with real output.
2. Behavioral checks using execution/REPL tools when available.
3. Subjective review only after the above.

## Notes — Phase 6

Be honest. Low ratings on difficult tasks are valuable data.

## Notes — Phase 7

When capturing failures, note whether better tool use or context loading could have prevented the issue.

## Closing

**Remember:** This is an optimized *adaptation*, not a replacement. The source of truth remains in `core/`. Use `../sync/check-core.sh` frequently, especially before important work.
