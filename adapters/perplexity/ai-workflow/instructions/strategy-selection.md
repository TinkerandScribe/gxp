# Perplexity Research Strategy Selection

This document provides guidance on selecting the right research strategy when operating under the GXP methodology.

The Perplexity adapter is a **research-only role** in GXP. Strategy selection here is about choosing the right research approach — not about delegating to subagents.

---

## Quick Decision Matrix

Apply this before beginning any non-trivial research session:

| Situation | Recommended Strategy |
|---|---|
| Broad technology evaluation, no time constraint | Full workflow — Web focus, iterative |
| Specific library/API, current docs needed | Targeted web search + official docs via MCP or direct URL |
| Architecture or design pattern comparison | Full workflow — Web → Academic → Writing |
| Performance, cost, or math-heavy question | Wolfram focus |
| Synthesizing prior research into a brief | Writing focus, use `research-to-brief.md` template |
| Quick single fact or version number | Lightweight workflow — single focused query |
| Repo-specific question (what does this codebase do?) | MCP tools first, search only for external context |

---

## Research Depth Levels

### Level 1 — Quick Lookup
- Single focused query
- No synthesis required
- Use when: verifying a version number, checking if a feature exists, single-answer facts
- Output: One sentence answer with citation

### Level 2 — Focused Research
- 3–7 queries across 1–2 Focus modes
- Brief synthesis paragraph per Key Question
- Use when: evaluating a single technology, answering a specific architectural question
- Output: Structured findings with citations and confidence levels

### Level 3 — Full Research Sprint
- 10+ queries, multiple Focus modes, MCP repo inspection
- Full brief structure with Ideal State Criteria
- Use when: major architectural decisions, technology migrations, significant new feature research
- Output: Full handoff document using `research-handoff.md` template

---

## Focus Mode Selection Guide

| Research Need | Best Focus Mode |
|---|---|
| Current ecosystem state, news, recent releases | Web |
| Deep technical papers, algorithms, formal methods | Academic |
| Synthesizing findings into a coherent narrative | Writing |
| Calculations, performance modeling, math | Wolfram |
| Combination (broad → deep → synthesized) | Web → Academic → Writing in sequence |

**Always note which Focus mode produced each finding.** This affects how much weight downstream agents should give the source.

---

## When to Escalate Out of Perplexity

Perplexity is the research layer. If the task requires any of the following, produce a handoff artifact and route to the appropriate agent:

- **Writing code**: Route to Cursor or Grok
- **Multi-file implementation**: Route to Grok (Composer 2.5) or Cursor
- **Interactive debugging**: Route to Cursor
- **Long-running agentic execution**: Route to Grok Build or Claude

The output of any escalation should be a GXP handoff document following `instructions/research-handoff.md`.

---

## Decision Logging

For Level 2 and Level 3 research, log your strategy decision at the start:

```
Research Strategy Decision:
- Level: [1 / 2 / 3]
- Focus mode(s): [Web / Academic / Writing / Wolfram]
- MCP tools needed: [yes / no — which ones]
- Estimated queries: [N]
- Justification: [one sentence]
- Handoff target: [agent and phase]
```

This log entry goes at the top of your research notes and feeds into Phase 6 rating.
