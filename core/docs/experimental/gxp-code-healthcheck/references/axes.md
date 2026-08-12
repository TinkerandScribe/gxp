# Expanded Axis Checks

Weight order (highest first):

1. Architecture & Boundaries  
2. Maintainability & Complexity  
3. Correctness & Robustness (lightweight structural view)  
4. Readability & Simplicity  
5. Security & Tool Evidence (light)

## 1. Architecture & Boundaries

- Clear module / layer ownership?
- Dependencies point in the right direction?
- Business/domain logic free of framework/UI/ORM leakage?
- Canonical homes for shared behavior exist and are used?
- Any “code judo” opportunity that would make entire layers, branches, or helpers disappear while preserving behavior?

## 2. Maintainability & Complexity

- Files approaching or past ~1000 lines without strong justification?
- God objects / classes with too many responsibilities?
- Spaghetti growth: new ad-hoc conditionals or feature checks in shared paths?
- Cognitive load of the main flows — can a reader hold the model?
- Complexity that can be *deleted* rather than rearranged?

## 3. Correctness & Robustness (structural signals)

- High-risk paths lacking obvious error / edge handling?
- State or invariant risks made likely by the current structure?
- Test coverage signals around critical modules (presence, not just count)?

## 4. Readability & Simplicity

- Straightforward control flow?
- Names that reveal intent?
- Unnecessary wrappers, identity abstractions, casts, or optionality?
- Dead or zombie code?

## 5. Security & Tool Evidence (light)

- Clear, high-confidence issues only.
- Prefer real-tool signals when available (complexity metrics, cycle detectors, dead-code finders, project linters).
- Record what was measured and what could not be measured.

When in doubt, elevate Architecture & Maintainability findings and treat ambitious simplification candidates as the highest-value output (subject to GXP scope rules).
