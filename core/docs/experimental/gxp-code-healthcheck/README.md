# gxp-code-healthcheck (Experimental)

**Status:** Experimental / Operator-gated only  
**Does not alter the stable GXP core path.**

## Purpose

GXP-native code health sensor. Grades a codebase or change for design quality, maintainability, architecture smells, and AI-slop patterns. Produces a severity scorecard, an explicit Fix-roadmap / Targeted-rewrite / Clean-rebuild recommendation, and a GXP Handoff Package of 4–8 binary Ideal State Criteria that can be consumed directly by a subsequent GXP brief or verifier.

## When to use

- Full codebase grading before a rework decision
- Deciding between incremental fix, targeted rewrite, or clean rebuild
- Feeding GXP Phase 0 / researcher with high-signal structural findings
- Reviewing a branch or module for spaghetti, God objects, boundary leaks, or AI-generated structural debt

## Hard constraints

- Opt-in only (or via Experimental-Skill Advisor)
- Never auto-activates
- Ambitious “code judo” ideas are recorded as *candidates* only — they do not expand the current task scope
- After the GXP Handoff Package is emitted, the skill stops
- Not a pure security, performance, or style tool

## How it feeds GXP

Every run ends with a mandatory **GXP Handoff Package**:

1. Recommended Path (Incremental fix / Targeted rewrite / Clean rebuild) + rationale
2. 4–8 candidate binary Ideal State Criteria
3. Verification ideas
4. Out of scope for the immediate brief

These criteria become the Ideal State Criteria of the next GXP task.

## Files

- `SKILL.md` — full executable skill
- `references/` — anti-patterns, axes, severity & decision gate

## Activation

Operator request, or Experimental-Skill Advisor suggestion after Phase 0 signals.
