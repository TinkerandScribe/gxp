# Severity Mapping & Fix-vs-Rebuild Decision Gate

## Severity Levels

- **Critical** — Structural debt that actively blocks safe change, creates high defect risk, or makes the system extremely expensive to evolve (pervasive God objects, widespread cycles, Big Ball of Mud signals across core modules, many files far past 1k lines with tangled logic).
- **High** — Clear design problems that will compound (localized God objects, spaghetti growth in important paths, significant boundary leaks, multiple modules that are hard to reason about).
- **Medium** — Real maintainability issues that should be scheduled (over-abstraction, moderate size/complexity, some Feature Envy or duplication).
- **Low** — Nits, style, or minor cleanup that does not change the structural recommendation.

Prefer fewer Critical/High findings with strong evidence over long lists of Lows.

## Decision Gate (primary recommendation)

Map the overall gap to one primary path. Adjust thresholds to codebase size and criticality; the categories are illustrative.

| Overall gap | Typical signals | Recommended path |
|-------------|-----------------|------------------|
| Small | Mostly Medium/Low; few structural issues; localized problems | **Incremental fix roadmap** |
| Medium | Several High findings; spaghetti or God objects in named modules; recoverable with focused work | **Targeted rewrite** of specific modules/subsystems + supporting roadmap |
| Large | Multiple Critical signals; pervasive structural problems across core; high cost/risk of incremental change | **Clean rebuild / fork** recommended |

Always justify the choice with the highest-severity findings. Do not recommend rebuild lightly; do not recommend endless incremental fixes when the structure is fundamentally hostile to change.

## GXP Handoff Rules

Every run **must** end with a GXP Handoff package containing (in this order):

1. **Recommended Path** + short rationale tied to the highest-severity findings.
2. **4–8 candidate binary Ideal State Criteria** derived from the Critical/High findings.  
   Criteria must be checkable (e.g. “No file in `src/core/` exceeds 800 lines”, “No circular dependencies among modules A, B, C”, “Module X has a single clear responsibility and <N public methods”).
3. **Verification ideas** — concrete commands, inspections, or tool checks that would prove each criterion.
4. **Out of scope** for the immediate brief (so GXP anti-scope-creep is respected).

These candidates become the Ideal State Criteria of the subsequent GXP task (fix brief or rebuild brief). The healthcheck itself does not expand scope; it only proposes.

After the package is emitted, the skill run stops.
