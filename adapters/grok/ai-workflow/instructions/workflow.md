# Grok-Optimized Workflow (v1.1)

> **Last synced from core:** post-strategy-prototype-implementation (2026-06-09)
> This file is intentionally allowed to diverge from `../../../core/workflow.md`
> for Grok-specific strengths. Run `../sync/check-core.sh` regularly.

This is a **Grok-optimized** adaptation of the core AI Workflow methodology.

## Grok Strengths We Leverage

- Excellent tool use and function calling
- Strong long-context reasoning
- Good at explicit uncertainty handling
- Capable of complex multi-step planning when given clear structure

## Autonomy calibration

This is an **L3/L4 bounded agent workflow**. The agent operates within a
defined task brief with explicit Ideal State Criteria, runs verification
itself, and pauses at approval gates. It is **not** L5 self-directed
research.

**Grok note:** Use your tool-calling capabilities aggressively during
repo audit and verification. Do not rely only on reasoning when tools
can give you ground truth.

## Full vs lightweight workflow

Same rules as core. When in doubt, run the full workflow.

## Phase 0 — Repo audit (Grok enhanced)

Before writing or proposing anything, scan the repo for context:

- Read `.ai/PROGRAM.md`
- Read `.ai/rules/`
- Read `.ai/failures/`
- Skim recent `ratings.jsonl`

**Grok-specific guidance:**
- Use the `read_file` and directory listing tools heavily here.
- When the repo is large, be strategic: start with key files mentioned
  in the brief, then expand using search.
- Explicitly call out any rules or past failures that are relevant.
- If you are uncertain about something, use tools to resolve it rather
  than guessing.

## Grok Build Strategy Selection (Prototype — see instructions/strategy-selection.md)

**For sessions running in Grok Build (with access to Composer 2.5 and subagents):**

After (or as part of) Phase 0, perform lightweight strategy classification using GXP language before committing to a model or delegation style.

See the full guidance in `instructions/strategy-selection.md` (coordinated with `core/tasks/EXAMPLE-feature-brief.md`).

Quick decision matrix (binary criteria style):
- Genuine ambiguity / architecture / research / planning heavy → Use native Grok + plan mode (or grok-native-planner persona).
- Coherent multi-file agentic coding, long sustained implementation, "make the whole thing work" → Composer 2.5 (via persona "composer-coder" or `/model composer-2.5` + subagent).
- Requires visual side-by-side editing, IDE context, or Cursor ecosystem → Emit Cursor Composer handoff artifact (GXP brief + ready-to-paste prompt that follows the Cursor adapter rule.mdc).
- Small, reversible, terminal/debug focused → Fast native Grok model.

**Always:**
- Log the decision with justification tied to Ideal State Criteria.
- Note capability (external_apis availability).
- Plan scoped context for any subagent/handoff.
- Ensure the choice can be scored later in critic / Phase 6 (gxp_alignment_score style).

This is prototype only — it advances the coordination brief without touching upstream orchestrator internals. Use `spawn_subagent` with persona for automatic switching inside one session.

## Phase 1 — Task brief

Same structure as core. Binary Ideal State Criteria remain the heart
of the system.

**Grok tip:** When writing verification plans, think about what tools
you can use to make verification deterministic.

## Phase 2 — Self-evaluation gate

Same gates as core.

**Grok note:** Be particularly strict on "Verification" and "Approval
gates". If a criterion cannot be checked mechanically, say so clearly
and propose how you will handle the uncertainty.

## Phase 3 — Implementation

- Keep the diff focused on the brief.
- Prefer the smallest viable change.
- Follow conventions from phase 0.
- Do not introduce new dependencies unless the brief calls for them.
- Write one-line notes for non-obvious decisions.

**Grok optimization:** Use your tool calling to explore the codebase
while implementing. Prefer reading actual source over relying on
memory.

## Phase 4 — Anti-loop rule

Identical to core. This rule is extremely high value.

## Phase 5 — Verification (Grok enhanced)

Run verification commands from `PROGRAM.md`.

**Strongly recommended order for Grok:**

1. **Deterministic checks first** (type/lint/test/build)
2. Use tools to execute tests and capture real output.
3. Behavioral checks — actually run the feature using whatever
   execution or REPL tools are available.
4. Only then do subjective review.

If a criterion cannot be checked mechanically, clearly state your
confidence level and the method used.

## Phase 6 — Rate

Append one JSON object per line to `ratings.jsonl`.

**Grok note:** Be honest. Low ratings on difficult tasks are extremely
valuable data.

## Phase 7 — Failure capture

Same as core, but with one Grok addition:

When capturing failures, consider whether better tool use or better
context loading could have prevented the issue. Document that.

## Phase 8 — Handoff (from core v1.1)

Explicit handoff section in the task brief when relevant.

---

**Remember:** This is an optimized *adaptation*, not a replacement.
The source of truth remains in `core/`. Use `../sync/check-core.sh`
frequently, especially before important work.