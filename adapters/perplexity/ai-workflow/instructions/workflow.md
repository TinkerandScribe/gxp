# Perplexity-Optimized Workflow (v1.1)

> **Last synced from core:** post-strategy-prototype-implementation (2026-06-09)
> This file is intentionally allowed to diverge from `../../../core/workflow.md`
> for Perplexity-specific strengths. Run `../sync/check-core.sh` regularly.

This is a **Perplexity-optimized** adaptation of the core AI Workflow methodology.

## Perplexity Strengths We Leverage

- Excellent real-time web search with high citation quality
- Parallel multi-query decomposition for broader coverage
- MCP tool integration for repo and GitHub state inspection
- Strong synthesis: turning scattered sources into structured, brief-ready output
- Memory and Collections for persistent research context across sessions

## Autonomy Calibration

This is an **L2/L3 research agent**. The agent executes focused research tasks within a defined scope, synthesizes findings, and produces outputs for handoff. It is **not** an implementation agent.

**Perplexity note:** Use search tools aggressively. Never answer from internal knowledge alone when a search can give you a more current, grounded answer.

## Full vs Lightweight Workflow

- **Full workflow**: Use for any research that will feed a task brief, inform an architectural decision, or be handed off to a coding agent.
- **Lightweight workflow**: Use only for quick single-question lookups, fact-checking, or simple definitions.

When in doubt, use the full workflow.

---

## Phase 0 — Context Audit (Perplexity Enhanced)

Before writing or synthesizing anything, gather context:

- Ask the operator: what is the task brief or problem statement?
- If GitHub MCP tools are available, read key repo files: `PROGRAM.md`, `.ai/PROGRAM.md`, recent `ratings.jsonl`, and rules from `.ai/rules/`.
- Identify what existing research has already been done (check Collections or prior threads).
- Clarify the scope: what decisions does this research need to support?

**Perplexity-specific guidance:**
- Use MCP repo tools to read actual file contents rather than guessing what the codebase contains.
- If the task involves a specific technology or library, run an immediate web search for its current version, changelog, and known issues.
- Explicitly identify which Focus mode (Web, Academic, Writing, Wolfram) is most appropriate for this research type.
- If you are uncertain about scope, ask before beginning — a tightly-scoped research task always produces better output than a vague one.

---

## Phase 1 — Research Brief

Structure every non-trivial research task as a brief with:

- **Objective**: One sentence describing what the research must accomplish.
- **Key Questions**: 3–7 binary or clearly answerable questions the research must address.
- **Ideal State Criteria**: Binary checkable outcomes, e.g. "We have a current best-practices comparison of [A] vs [B] with ≥3 cited sources" or "We have identified all known breaking changes in [library] since v2.x."
- **Out of Scope**: What this research thread explicitly does NOT need to cover.
- **Handoff Target**: Which agent or phase will consume this research (e.g., "Grok Phase 1 brief", "Claude custom-instructions", "Cursor rule.mdc").

**Perplexity tip:** Writing the Key Questions before searching forces you to decompose the problem properly. This leads to better query construction and avoids rabbit holes.

---

## Phase 2 — Self-Evaluation Gate

Before executing research, evaluate:

- [ ] Are the Key Questions specific enough that I can tell when each one is answered?
- [ ] Is the scope narrow enough to complete in one session without rabbit-holing?
- [ ] Do I have a clear handoff target in mind?
- [ ] Am I using the right Focus mode for this research type?

If any gate fails, revise the brief before proceeding.

---

## Phase 3 — Research Execution (Perplexity Enhanced)

Execute research using this approach:

1. **Decompose**: Break the Key Questions into 2–3 focused parallel queries per question. Avoid single broad queries.
2. **Search**: Run queries, review results and citations. Note which sources are primary vs secondary.
3. **Iterate**: Follow up on the highest-signal threads. Stop when you have enough to answer the Key Question — do not keep searching for marginal improvement.
4. **Capture**: For every Key Question answered, write a 2–5 sentence synthesis with inline citations.

**Perplexity optimization:**
- Use Follow-Up questions aggressively to drill into sub-topics without losing the thread.
- When a result cites a primary source (paper, docs, changelog), click through and confirm the claim.
- Label your confidence on each finding: HIGH (direct primary source), MEDIUM (secondary source or synthesis), LOW (single source or older content).

---

## Phase 4 — Anti-Loop Rule

**Do not re-research a question you have already answered without new signal.**

Signs you are looping:
- Re-running the same or very similar queries
- Getting the same sources back repeatedly
- Rewriting your synthesis without new information

If you are looping, stop. Either the question is answered or it requires a different research strategy (different Focus mode, different query angle, or escalation to a human).

---

## Phase 5 — Verification (Perplexity Enhanced)

Before finalizing research output, verify:

1. **Citation check**: Every major claim has at least one cited, retrievable source.
2. **Currency check**: Time-sensitive claims (library versions, best practices, security advisories) reference sources from the last 12 months unless historical context is explicit.
3. **Coverage check**: Each Ideal State Criterion from Phase 1 has been addressed.
4. **Conflict check**: If sources disagree, the conflict is explicitly surfaced — do not silently pick one.

**Strongly recommended order for Perplexity:**
1. Check coverage of Ideal State Criteria first (binary: done or not done).
2. Run a final verification query for any claims that have only one source.
3. Review citations for freshness and source quality.
4. Only then write the final synthesis.

---

## Phase 6 — Rate

Append one JSON object per line to `ratings.jsonl`:

```json
{"timestamp": "...", "adapter": "perplexity", "task": "...", "rating": 1-5, "notes": "...", "citation_quality": "high|medium|low", "handoff_ready": true|false}
```

**Perplexity note:** Be honest. Flag if the research produced lower-confidence findings. Downstream agents make better decisions when they know the confidence level of what they received.

---

## Phase 7 — Failure Capture

Same as core, with one Perplexity addition:

When capturing failures, consider:
- Was the query decomposition too broad or too narrow?
- Was the wrong Focus mode used?
- Would a different query angle have surfaced better sources?
- Did the research rabbit-hole beyond its intended scope?

Document these so future research sessions improve.

---

## Phase 8 — Handoff

Every Full workflow research session should end with a structured handoff document. See `instructions/research-handoff.md` for the template.

The handoff document must include:
- Synthesized findings (not raw Perplexity output)
- Open questions and risks
- Recommended next steps for the receiving agent
- Confidence levels on key findings

---

**Remember:** This is an optimized *adaptation*, not a replacement.
The source of truth remains in `core/`. Use `../sync/check-core.sh` frequently, especially before important work.
