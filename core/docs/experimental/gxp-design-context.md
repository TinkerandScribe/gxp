# gxp-design-context

**Experimental. Operator-activated only (or via Experimental-Skill Advisor).**

## Purpose

When working on multi-file or design-sensitive code, produce the three light Program Design artifacts preferred by Dex Horthy’s approach so that Ideal State Criteria and verification plans are grounded in the actual shape of the code *before* implementation begins.

## When to use

- Multi-file changes
- New interfaces, types, or call flows
- Hierarchy / selection / orchestration logic
- Any task where maintainability or interface clarity is a known risk

## Hard constraints

- Never write implementation bodies
- Keep artifacts short and scannable
- Prefer light pseudocode over heavy diagrams
- All decisions must be challengeable by the operator before the self-evaluation gate

## Artifacts to produce (in order)

1. **File-tree diff**  
   Show new and modified files with one-line justifications.

2. **Call-stack tree(s)**  
   Use diff syntax (`+` / `-`) for the main flows being changed.

3. **Types + method signatures**  
   Only signatures and type definitions — no bodies.

4. **Least-confident decisions**  
   Numbered list of the places that most need operator challenge.

5. **Suggested Ideal State Criteria**  
   Convert the key design decisions into 4–8 binary, checkable criteria that can be dropped into the normal GXP task brief.

## Output location

Write artifacts under:

```
docs/plans/<feature-slug>/03-program-design.md
```

(or the project’s equivalent design location)

## Integration with GXP

- Activated only when the operator says yes to the Experimental-Skill Advisor or explicitly invokes this skill.
- Output feeds directly into Phase 1 (Task Brief) Ideal State Criteria and the Phase 2 self-evaluation gate.
- After the artifacts are approved, normal GXP Full workflow continues (implementation → two-layer verification → rating).

## Example invocation

Operator: `use gxp-design-context`  
or  
Advisor suggestion → operator replies `y`

Then produce the four artifacts listed above and stop for operator review of the least-confident decisions before proceeding.
