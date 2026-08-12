# Curated High-Signal Anti-Patterns & Smells

Use these as first-class detection targets. Always attach concrete evidence (file, symbol, structural pattern). Prefer a few high-conviction findings over exhaustive lists.

## Architecture

- **Big Ball of Mud / Missing Architecture**  
  No clear module or layer boundaries; any code can call almost anything.  
  Evidence: tangled import graph, shared “utils” that know too much, no ownership.

- **Violated Layer Boundaries**  
  Domain/business logic depends on UI, HTTP, ORM, or infrastructure types (or the reverse in the wrong direction).  
  Remedy: push dependencies inward; keep domain pure.

- **Over-abstraction / Speculative Generality**  
  Abstractions, interfaces, or configurability added for imagined future needs.  
  Thermo-nuclear test: does this abstraction earn its complexity *today*?

- **Anemic Domain or Logic in Wrong Layer**  
  Data holders with no behavior; all logic lives in services/controllers/handlers.

## Coupling & Cohesion

- **God Object / God Class**  
  One type or file owns too many responsibilities or grows past ~500–1000 lines.  
  Evidence: method count, responsibility list, size.

- **Circular Dependencies**  
  A → B → A (or longer cycles). Detect via import graph or build errors.

- **Feature Envy**  
  A method uses another type’s data/methods more than its own.

- **Shotgun Surgery**  
  A single conceptual change requires edits across many unrelated files.

## Design & Complexity

- **Spaghetti / Conditional Complexity Growth**  
  Ad-hoc conditionals, feature flags, or special cases bolted onto shared flows.  
  New branches that make an existing path harder to reason about = design smell.

- **Files Crossing ~1000 Lines**  
  Strong default smell. Prefer decomposition before further growth.

- **Leaky or Thin Abstractions**  
  Wrappers that add indirection without real value; identity abstractions; excessive casts/optionality that obscure the real design.

- **Duplicated or Near-Duplicate Helpers**  
  Especially common in AI-generated code. Prefer canonical home + reuse.

## AI-Slop Specific Signals

- Over-generated abstraction layers that could be collapsed
- Hollow or low-value tests that assert almost nothing
- Inconsistent patterns across successive agent edits
- Weak or missing module boundaries after multi-file generation
- Dead code left from iterative LLM attempts

## Usage Rule

When a finding matches one of the above, name the pattern, cite evidence, and propose a concrete structural remedy. Ambitious “code judo” restructurings that *delete* complexity are preferred, but always record them as candidates until a GXP brief accepts the scope.
