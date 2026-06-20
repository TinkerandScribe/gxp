# Research Handoff Template

One of the most valuable uses of Perplexity in the GXP workflow is producing high-quality research that can be handed off to a coding/research agent (Grok, Claude, Cursor, etc.).

This template helps you turn scattered Perplexity threads into clean, high-signal context that another agent can use effectively.

## Recommended Handoff Structure

When moving research from Perplexity into another agent, use this format:

```markdown
## Research Summary: [Topic]

**Research Goal:**
[What decision or part of the brief this research was meant to inform]

**Key Findings:**
- [Finding 1] (Source: [link or citation])
- [Finding 2] (Source: ...)
- ...

**Important Trade-offs:**
- ...

**Risks & Failure Modes Observed Elsewhere:**
- ...

**Open Questions / Areas of Uncertainty:**
- ...

**Sources:**
- [Link 1] - [brief note on why it's relevant]
- [Link 2] - ...

**Recommended Constraints for the Brief:**
- [Suggestion 1]
- [Suggestion 2]

**Suggested Out of Scope Items (based on research):**
- ...
```

## How to Use This Template

1. After doing research in Perplexity, copy the most important threads.
2. Fill out the template above (you can do this in Perplexity itself using the Writing focus, or manually).
3. Paste the completed handoff into your main agent along with your draft task brief.
4. Ask the agent to incorporate the research into the Context and Out of Scope sections.

## Pro Tips

- **Be selective.** Better to hand off 3–5 high-signal findings with good sources than 20 scattered ones.
- **Include "so what".** Don't just list facts — briefly note why each finding matters to the decision at hand.
- **Note contradictions.** If sources disagree, call it out explicitly. This is very useful for the receiving agent.
- **Use Perplexity's Writing focus** as a final synthesis step before handing off. It often produces much cleaner output than raw research threads.

## Example Prompt to Generate a Handoff

You can paste this into Perplexity (ideally in Writing focus) after doing research:

```
Using the research we've done in this thread, create a clean Research Handoff document in the following format:

## Research Summary: [Topic]

**Research Goal:**
[What decision or part of the brief this research was meant to inform]

**Key Findings:**
- [Finding 1] (Source: [link or citation])
- ...

**Important Trade-offs:**
- ...

**Risks & Failure Modes Observed Elsewhere:**
- ...

**Open Questions / Areas of Uncertainty:**
- ...

**Sources:**
- ...

**Recommended Constraints for the Brief:**
- ...

**Suggested Out of Scope Items (based on research):**
- ...
```

This pattern turns Perplexity from a "chat with search" into a powerful **research engine** that feeds directly into high-quality GXP task briefs.