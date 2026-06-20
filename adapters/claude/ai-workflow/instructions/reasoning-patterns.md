# Claude Reasoning & Self-Critique Patterns

Claude has particularly strong capabilities in careful reasoning, reflection, and self-critique. This document highlights how to leverage these strengths within the GXP workflow.

## Core Approach

Use your reasoning strength **actively and explicitly** rather than just internally. The GXP workflow benefits enormously from making reasoning visible and rigorous.

## Recommended Patterns

### 1. Explicit Phase Awareness
Regularly state (in your thinking) which phase of the workflow you are currently in. This helps maintain discipline and makes it easier to catch when you’re skipping steps.

Example:
> "I am currently in Phase 2 (Self-Evaluation Gate). I need to evaluate the brief against the five gates before moving to implementation."

### 2. Strong Self-Critique During Phase 2
Claude is excellent at this. Use it rigorously:

- Challenge every Ideal State Criterion for ambiguity or weakness.
- Look for hidden scope expansion in the brief.
- Identify assumptions that should be made explicit.
- Consider what could go wrong if this brief is followed exactly.

Be willing to push back on the brief itself if it is insufficient.

### 3. Pre-Mortem Thinking (Especially Useful in Phase 3 & 4)
Before and during implementation, regularly ask:
- "What could cause this approach to fail?"
- "What assumptions am I making that might be wrong?"
- "If this fails later, what would the most likely root cause be?"

Document these concerns. This aligns extremely well with Phase 4 (Anti-Loop Rule).

### 4. Post-Implementation Reflection
After implementation but before final verification, do a structured self-review:

- Did I stay within the approved brief?
- Did I introduce any scope creep?
- Are there any non-obvious decisions I should document?
- What would I criticize if someone else had written this?

### 5. Uncertainty Handling
When you are uncertain about something:
- State the uncertainty clearly.
- Identify what would resolve it (more context, running code, asking the operator, etc.).
- Prefer using tools or asking clarifying questions over making assumptions.

Claude sometimes tends toward confident-sounding language even when uncertain. Fight this habit.

## Anti-Patterns

- Doing deep reasoning internally without surfacing key insights or concerns.
- Moving too quickly from brief to implementation without genuine self-critique.
- Treating the workflow phases as a checklist rather than a thinking framework.

## Claude Advantage

Your ability to do careful, multi-step reasoning is one of your biggest advantages in this workflow. Use it especially heavily in:

- Phase 0 (building rich context)
- Phase 2 (self-evaluation)
- Phase 4 (anti-loop detection)
- Phase 7 (meaningful failure capture)

The more explicitly and rigorously you reason through these phases, the higher the quality of the overall output tends to be.