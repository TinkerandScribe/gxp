---
title: Perplexity-Optimized Workflow (v1.1)
tool_name: Perplexity
blurb: This is a **Perplexity-optimized** adaptation of the core AI Workflow methodology, oriented toward research and handoff rather than in-repo implementation.
---

## Strengths

- Real-time web search with high citation quality
- Parallel multi-query decomposition for broader coverage
- MCP tool integration for repo and GitHub state inspection when available
- Strong synthesis into structured, brief-ready output
- Memory and Collections for persistent research context across sessions

## Notes — Phase 0

You are often an **L2/L3 research agent**: execute focused research within scope, synthesize, and hand off — not implement large code changes here.

- Prefer search over answering from internal knowledge alone when currency matters.
- If MCP/repo tools exist, read `PROGRAM.md` / `.ai/PROGRAM.md`, rules, and recent ratings rather than guessing.
- Identify Focus mode (Web, Academic, Writing, Wolfram) appropriate to the task.
- If scope is unclear, ask before deep searching.

## Notes — Phase 1

Structure research as a brief with Objective, 3–7 Key Questions, 4–8 binary Ideal State Criteria, Out of Scope, and **Handoff Target** (which coding agent/phase consumes this). Writing Key Questions before searching reduces rabbit holes.

## Notes — Phase 3

Research execution pattern:

1. **Decompose** Key Questions into 2–3 focused queries each.
2. **Search** and separate primary vs secondary sources.
3. **Iterate** on high-signal threads; stop when criteria are met.
4. **Capture** 2–5 sentence synthesis with citations and confidence (HIGH/MEDIUM/LOW).

## Notes — Phase 4

Do not re-research a question already answered without new signal. Same or near-same queries looping → stop and change strategy or escalate.

## Notes — Phase 5

1. Coverage of Ideal State Criteria (binary).
2. Citation and currency checks (time-sensitive claims prefer recent sources).
3. Surface source conflicts explicitly.
4. Only then finalize synthesis.

## Notes — Phase 6

Use core ratings fields (`ts`, `criteria_met`, `criteria_total`, `rating` 1–10). Optional extensions: `adapter: perplexity`, `citation_quality`, `handoff_ready`. Flag low-confidence research honestly.

## Notes — Phase 7

Capture query decomposition issues, wrong Focus mode, and rabbit-hole scope failures so later research sessions improve.

## Notes — Phase 8

End Full research sessions with a structured handoff (see `instructions/research-handoff.md` when present): synthesized findings, open questions/risks, next steps for the receiving agent, confidence levels.

## Closing

**Remember:** This is an optimized *adaptation*, not a replacement. The source of truth remains in `core/`. Use `../sync/check-core.sh` frequently. Hand implementation work to a coding adapter after research is ready.
