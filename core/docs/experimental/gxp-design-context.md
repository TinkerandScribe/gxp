---
name: gxp-design-context
aliases: [design-context, program-design-context, contextual-design]
description: >
  Experimental GXP skill that produces light Program Design artifacts 
  (file-tree diffs, call-stack trees, types + signatures, least-confident decisions)
  for code-related work. Opt-in only. Feeds higher-quality Ideal State Criteria.
  Incorporates design-time ambition (code-judo), boundary clarity, and pattern justification.
---

# gxp-design-context

**Experimental. Operator-activated only (or via Experimental-Skill Advisor).**

## Purpose

When working on multi-file or design-sensitive code, produce five light Program Design artifacts so that Ideal State Criteria and verification plans are grounded in the actual shape of the code *before* implementation begins.

The goal is a design that feels inevitable in hindsight — one that deletes complexity rather than rearranges it.

## When to use

- Multi-file changes
- New interfaces, types, or call flows
- Hierarchy / selection / orchestration logic
- Any task where maintainability or interface clarity is a known risk
- Modules that `gxp-code-healthcheck` has flagged for **Targeted rewrite**

Prefer this skill for *new or changing design work*. Prefer `gxp-code-healthcheck` when the task is grading existing structural debt, spaghetti, or fix-vs-rebuild decisions.

## Hard constraints

- Never write implementation bodies
- Keep artifacts short and scannable
- Prefer light pseudocode over heavy diagrams
- All decisions must be challengeable by the operator before the self-evaluation gate
- Any larger structural suggestions beyond the five artifacts are *candidates only* until accepted into a GXP brief
- Any new pattern or abstraction must be justified in the least-confident decisions

## What this skill does NOT do

- Full architecture or code-quality reviews (use `gxp-code-healthcheck`)
- Implementation of any code
- Heavy diagrams or exhaustive documentation
- Unbounded cleanup or scope expansion
- Auto-activation

## Artifacts to produce (in order)

1. **File-tree diff**  
   Show new and modified files with one-line justifications.  
   Make ownership and layer placement obvious.

2. **Call-stack tree(s)**  
   Use diff syntax (`+` / `-`) for the main flows being changed.  
   Make dependency direction and layer crossings visible. Prefer designs that keep dependencies pointing inward.

3. **Types + method signatures**  
   Only signatures and type definitions — no bodies.  
   Prefer explicit models over optionality, casts, or ad-hoc shapes. Ask whether each type earns its complexity.

4. **Least-confident decisions**  
   Numbered list of the places that most need operator challenge.  
   Tag each with relevant risk dimensions when useful:
   - **Boundary** — layer or module ownership risk
   - **Abstraction** — does this abstraction earn its keep today?
   - **Pattern** — introduces a new pattern; is it justified?
   - **Ambition** — is there a simpler framing that deletes complexity?
   - Confidence: High / Medium

5. **GXP Handoff (mandatory)**  
   Convert the key design decisions into a short package (see below).

### Design Ambition check (required before handoff)

Before emitting the handoff, explicitly answer:

- Is there a code-judo / design-judo move that would make this dramatically simpler (fewer concepts, fewer branches, fewer helpers, cleaner boundaries)?
- Does every new abstraction or pattern earn its complexity *today*?
- Would this design feel inevitable in hindsight, or merely workable?

If a simpler framing exists, either adopt it in the artifacts or list it as a High-ambition candidate in the least-confident decisions / Out of Scope section.

While producing the artifacts, briefly note any obvious God-object growth, boundary leaks, or speculative generality that the new design should avoid. Do not turn this skill into a full healthcheck.

## Output location

Write artifacts under:

```
docs/plans/<feature-slug>/03-program-design.md
```

(or the project’s equivalent design location)

## GXP Handoff (mandatory)

End every run with this short package:

```markdown
## GXP Handoff (Design Context)

### Suggested Ideal State Criteria (binary, checkable)
1. ...
2. ...
(4–8 max)

### Verification Ideas
- Concrete checks that would prove each criterion

### Least-confident decisions still needing operator challenge
- [Boundary / Abstraction / Pattern / Ambition] ...

### Out of Scope / Candidates
- Any larger structural suggestions or alternative framings that remain candidates only
```

**After emitting the Handoff Package, stop.** Do not expand into implementation, additional analysis, or free-form cleanup.

## Integration with GXP

- Activated only when the operator says yes to the Experimental-Skill Advisor or explicitly invokes this skill.
- Strongly recommended after a `gxp-code-healthcheck` **Targeted rewrite** recommendation, before implementation begins.
- Output feeds directly into Phase 1 (Task Brief) Ideal State Criteria and the Phase 2 self-evaluation gate.
- After the artifacts and least-confident decisions are approved, normal GXP Full workflow continues.

## Example invocation

Operator: `use gxp-design-context`  
or  
Advisor suggestion → operator replies `y`

Then produce the five artifacts + Design Ambition check + GXP Handoff and stop for operator review.
