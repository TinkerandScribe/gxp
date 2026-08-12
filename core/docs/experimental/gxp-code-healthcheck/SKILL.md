---
name: gxp-code-healthcheck
description: Performs structured code health audit for design quality, maintainability, architecture smells, and AI-slop patterns. Grades a codebase or change, produces severity scorecard, proposes binary Ideal State Criteria, and recommends fix-roadmap vs targeted rewrite vs clean rebuild. Use when reviewing codebases for spaghetti or design debt, grading quality before rework, deciding fix vs rebuild under GXP, or feeding Phase 0 / verifier with high-signal findings.
---

# GXP Code Healthcheck

You are running a **GXP-native code health audit**. Your job is to produce evidence-backed findings that map directly into binary Ideal State Criteria and a clear Fix-vs-Rebuild decision. Do not produce soft opinions or endless nit lists.

## When to Use

- Full codebase grading before a rework decision
- Review of a branch, PR, or set of changes for structural health
- Module or subsystem health check
- Feeding GXP Phase 0 or the verifier persona with high-signal design findings
- Deciding between incremental fix roadmap, targeted rewrite, or clean rebuild

Do **not** use for pure security audits, pure performance profiling, or trivial style nits. Point those to specialized skills.

### What this skill does NOT do
- Deep security or performance audits (light flags only)
- Exhaustive style or formatting reviews
- Unbounded “clean everything” recommendations that invite scope creep
- Auto-expanding the current task with ambitious rewrites (those stay candidates until a GXP brief accepts them)

## Modes

1. **Full codebase** — grade overall design health and recommend path
2. **Diff / branch / PR** — focus on regressions and missed opportunities in the change
3. **Module focus** — deep dive on one subsystem

Ask for mode and scope if not specified. Default for large unknown repos: recent changes + highest-risk modules.

## Core Process

### 1. Scope & Evidence Collection

- Confirm mode and boundaries.
- For **full-codebase** mode, follow this efficient order:
  1. Structure map + large-file inventory (>500 lines soft flag, >1000 lines strong)
  2. Dependency / cycle signals (if tools or simple import analysis available)
  3. God-object and layer-boundary heuristics
  4. Targeted deep reads on the highest-severity candidates
- Gather structural signals:
  - Large files / God candidates
  - Import / dependency cycles if detectable
  - Obvious layer boundary leaks
  - Test presence and quality signals around changed or critical paths
- Prefer tool evidence (complexity, cycles, dead code, linters) when available. Record what was and was not measurable.
- For AI-generated or heavily agent-touched code, note duplication, over-abstraction, weak boundaries, and hollow tests as first-class signals.

### 2. Multi-Axis Review (weighted)

Evaluate in this priority order:

1. **Architecture & Maintainability** (highest weight)
   - Layer / module boundaries and leaks
   - God objects / excessive responsibility
   - Circular or tangled dependencies
   - Spaghetti growth (ad-hoc conditionals, feature checks scattered across shared code)
   - File size and decomposition
   - Abstraction quality — do abstractions earn their complexity?
   - Code-judo opportunities: places where a restructuring would *delete* complexity while preserving behavior

2. **Readability & Simplicity**
   - Control flow clarity
   - Naming and local consistency
   - Unnecessary indirection, wrappers, casts, or optionality churn
   - Dead or zombie code

3. **Correctness signals** (lightweight)
   - Obvious edge-case or error-path gaps visible from structure
   - Test gaps that leave high-risk paths unguarded
   - State / invariant risks that structure makes likely

4. **Security & Performance** (light pass only)
   - Flag only clear, high-confidence issues or obvious hotspots. Defer deep dives.

### 3. Anti-Pattern Scan (curated)

Actively look for and evidence these high-signal smells (see `references/anti-patterns.md` for detail):

- God Object / Blob
- Big Ball of Mud / Missing Architecture
- Circular Dependencies
- Feature Envy / Shotgun Surgery
- Anemic Domain or Logic in Wrong Layer
- Spaghetti / Conditional Complexity Growth
- Premature or Leaky Abstraction
- AI-slop patterns (near-duplicate helpers, over-wrapping, hollow tests, inconsistent style across agent edits)

Record only findings with concrete evidence (file, symbol, or structural pattern).

### 4. Ambition Rule (Code Judo)

Be ambitious about structural simplification. Prefer findings that show how complexity can be *deleted* rather than rearranged. 

**Critical constraint:** Record ambitious restructuring ideas as *candidate improvements*. Do **not** expand the current task scope. Under GXP these become proposed Ideal State Criteria or items for a later brief.

### 5. Grading & Decision Gate

Produce:

- **Severity scorecard** per major finding or axis (Critical / High / Medium / Low)
- **Overall health judgment** in binary-friendly language
- **Path recommendation** (choose one primary):
  - **Incremental fix roadmap** — gap is manageable with targeted changes
  - **Targeted rewrite** of named modules/subsystems
  - **Clean rebuild / fork** recommended — structural debt is pervasive enough that incremental work is high-risk or low-leverage

Justify the recommendation with the highest-severity findings.

### 6. GXP Handoff Package (mandatory)

End every run with this package so a GXP brief or verifier can consume it directly:

```markdown
## GXP Handoff

### Recommended Path
[Incremental fix roadmap | Targeted rewrite of X/Y | Clean rebuild]
Rationale: [2–4 sentences tied to highest-severity findings]

### Proposed Ideal State Criteria (binary, checkable)
1. ...
2. ...
(4–8 max; prefer criteria that close Critical/High findings)

### Verification Ideas
- Commands / tools / checks that would prove each criterion
- Suggested Phase 0 files or modules to open first

### Out of Scope for Current Brief
- Items that would expand beyond the recommended path
```

## What This Skill Does NOT Do

- Pure security audits or deep vulnerability hunting (point to dedicated security skills)
- Pure performance profiling or optimization campaigns
- Style / formatting nits or exhaustive cosmetic lists
- Unbounded cleanup or automatic scope expansion
- Declaring a codebase “healthy” solely because tests pass or behavior appears correct

## Output Rules

- Prioritize structural and maintainability findings over nits.
- Prefer a smaller number of high-conviction findings with evidence.
- Never approve a change or declare a codebase “healthy enough” solely because behavior appears correct.
- Quantify when possible (file sizes, cycle counts, number of touch points for a change).
- Keep the main report scannable; move deep catalogs and examples to references.
- **After emitting the GXP Handoff Package, stop.** Do not append free-form cleanup lists or expand scope.

## Approval / Exit Bar for This Skill

The skill run is complete only when:

- Mode and scope are clear
- Highest-weight axes have been examined with evidence
- At least one explicit path recommendation is made and justified
- The GXP Handoff package is present, the path is explicit, and the proposed criteria are binary and checkable

## References

- `references/anti-patterns.md` — curated high-signal smells and remedies
- `references/axes.md` — expanded checks per axis
- `references/severity-and-decision.md` — how to map findings to severity and Fix-vs-Rebuild
