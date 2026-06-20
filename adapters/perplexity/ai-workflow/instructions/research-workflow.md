# Perplexity Research Workflow (GXP Optimized)

This guide explains how to use Perplexity effectively as part of the GXP (Guided eXecution Protocol) methodology.

## Core Mindset

Perplexity is a **research acceleration tool**, not a replacement for thinking or coding agents.

Its job in GXP is to rapidly produce high-quality, cited information that feeds into Phase 0 (Context Gathering) and helps create stronger task briefs.

## Recommended Research Process

### 1. Define the Research Question(s) First
Before opening Perplexity, clearly articulate what you need to know.

Good examples:
- "What are the current best practices and trade-offs for implementing real-time collaboration in web apps in 2025?"
- "What are the main technical and business risks when adopting [specific technology] in a small team?"

Bad examples:
- "Tell me about real-time apps"
- "What should I build?"

### 2. Use Focused, Iterative Queries
- Start with 1–3 high-signal questions.
- Review the results and citations.
- Follow up with more targeted questions based on what you learned.
- Stop when you have enough signal to inform your task brief.

### 3. Capture Research Outputs Deliberately
For every meaningful research thread, capture:
- Key findings
- Most relevant sources/citations
- Open questions or risks
- How this research affects your task brief or scope

Bring these findings into your main agent (Grok, Claude, Cursor, etc.) when writing the actual task brief.

## Perplexity Strengths to Leverage

- Fast synthesis of current information
- Good citation quality (better than most models for research)
- Ability to quickly explore adjacent topics

## Common Pitfalls to Avoid

- **Endless exploration**: Perplexity makes rabbit holes very easy. Set time or question limits.
- **Treating Perplexity as your only source**: Always cross-reference important claims.
- **Vague queries**: The quality of output is highly dependent on query quality.
- **Skipping synthesis**: Raw Perplexity output is rarely ready to go straight into a task brief. You must do the work of turning it into structured context.

## Suggested Prompt Starters

Use these as starting points when beginning research inside Perplexity:

**For technology evaluation:**
"Compare [Technology A] vs [Technology B] for [specific use case] in 2025. Focus on maturity, ecosystem, performance characteristics, and team size suitability. Include recent developments."

**For competitive / domain research:**
"What are the current leading approaches and key challenges in [domain] as of 2025? Summarize the top 3–5 approaches with their main trade-offs."

**For best practices:**
"What are the current recommended patterns and anti-patterns for [specific technical problem] in production systems?"

## Integration with GXP Workflow

Research done in Perplexity should primarily feed into:
- Phase 0 (deeper context)
- Phase 1 (better briefs — especially Context and Out of Scope sections)
- Phase 2 (identifying risks and approval gates early)

Strong research early in the workflow dramatically improves the quality of everything that follows.