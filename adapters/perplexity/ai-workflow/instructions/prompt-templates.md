# Perplexity Prompt Templates for GXP

This file contains ready-to-use, high-signal prompt templates optimized for Perplexity when conducting research as part of the GXP workflow.

## Technology Evaluation

```
Compare [Technology A] vs [Technology B] for [specific use case] in a [team size / context] environment as of 2025.

Focus on:
- Maturity and production readiness
- Ecosystem health and long-term viability
- Performance characteristics relevant to our use case
- Learning curve and team fit
- Major risks or common failure modes reported in real usage
- Recent developments (2024–2025)

Prioritize practical considerations over marketing claims. Include sources.
```

## Architecture & Trade-off Research

```
For a [team size] team building [type of system], what are the main architectural approaches to [problem] in 2025?

For each major approach, cover:
- Core idea and when it makes sense
- Key advantages
- Major drawbacks and operational costs
- Real-world examples of success and failure
- When to avoid this approach

Rank them by relevance to the following constraints: [paste relevant constraints from your brief].
```

## Competitive / Market Landscape

```
What are the current leading companies and approaches in [market / problem space] as of 2025?

For the top 4–6 players/approaches, summarize:
- Core positioning and differentiation
- Strengths and weaknesses
- Recent strategic moves (last 18 months)
- Notable risks or controversies

Focus on information relevant to a small-to-medium team making build vs partner vs buy decisions.
```

## Risk and Failure Mode Research

```
What are the most common ways teams have failed or struggled when adopting [technology/approach]?

Structure the answer by:
- Most frequent failure modes
- Early warning signs
- Hidden or underestimated costs
- What successful teams did differently

Include specific examples and sources where possible.
```

## Build vs Buy / Build vs Partner Analysis

```
For a [team size] team with [relevant constraints], what are the main options for solving [problem]?

Compare:
- Building in-house
- Using open source + self-hosting
- Using managed SaaS / third-party services
- Partnering with another company

For each option, cover realistic total cost of ownership, time-to-value, lock-in risks, and operational burden.
```

## Recent Developments & "What's New"

```
What are the most significant developments in [technology/domain] from the last 12–18 months (as of 2025) that a working software engineer should be aware of?

Focus on changes that materially affect architectural decisions, rather than hype. Include sources.
```

## Operational & Cost Considerations

```
What are the real-world operational and cost implications of running [technology/approach] at [scale / team size]?

Cover:
- Typical infrastructure and staffing requirements
- Common hidden costs
- Operational complexity and toil
- Scaling characteristics

Base the answer on real reports and case studies rather than vendor claims.
```

## Security, Compliance, and Risk Posture

```
What are the current security and compliance considerations when using [technology/approach] in a [regulated / high-trust] environment?

Focus on:
- Known vulnerabilities or attack surfaces
- Compliance certifications and gaps
- Common misconfigurations that cause issues
- How mature teams are handling these risks in 2025
```

## Tips for Using These Templates in GXP

- Replace bracketed sections with details from your current task brief or Phase 0 findings.
- Add explicit constraints (team size, timeline, risk tolerance, existing tech stack, etc.).
- After running research, **synthesize** the output into your task brief instead of pasting raw results.
- Use multiple templates in sequence when the topic is complex (e.g., Technology Evaluation → Risk and Failure Mode Research → Operational Considerations).

These templates are designed to produce research that translates cleanly into strong **Context**, **Out of Scope**, and **Verification Plan** sections in a GXP task brief.