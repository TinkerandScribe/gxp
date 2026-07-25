# Research Handoff Template

One of the most valuable uses of Perplexity in the GXP workflow is producing
high-quality research that can be handed off to a coding/research agent
(Grok, Claude, Cursor, etc.).

This template turns scattered Perplexity threads into clean, high-signal
context with explicit **trust boundaries** so the receiving agent never
confuses external research with repo ground truth or local verification.

## Trust boundaries (non-negotiable)

1. **Research-stage only.** This handoff does **not** claim that files were
   edited, tests/lint/build were run, or ratings/failures ledgers were updated.
   Local verification belongs to the coding agent (or host) after handoff.
2. **Separate provenance.** Label every load-bearing fact as either
   **repository-sourced** (from MCP/repo tools or operator-pasted tree state)
   or **externally researched** (Perplexity search / web / academic sources).
3. **Separate epistemic status.** Use three buckets below — do not merge
   verified findings, inferences, and open questions into one undifferentiated
   bullet list.
4. **No false local-verify.** Never write language such as “tests pass,”
   “build is green,” or “verified in the repo” unless the **host** actually
   ran those checks and the handoff quotes that evidence. If asked to run
   local commands you cannot run, refuse explicitly and park the check for
   the receiving agent.

## Recommended Handoff Structure

When moving research from Perplexity into another agent, use this format:

```markdown
## Research Summary: [Topic]

**Research Goal:**
[What decision or part of the brief this research was meant to inform]

**Handoff Target:**
[Which coding agent / GXP phase consumes this — e.g. Cursor Phase 1 brief]

### Provenance legend
- **Repo:** fact observed via repo tools or operator-supplied tree state
- **External:** fact from Perplexity/web/academic sources (cite URL or title)

### Verified findings
Facts with clear support. Prefer primary sources. Each bullet must carry
provenance and a citation when External.

- [Repo|External] [Finding] (Source: …) — confidence: HIGH|MEDIUM|LOW

### Inferences
Conclusions that go beyond a single source: synthesis, likely implications,
recommended approaches. Label as inference so the receiver can re-check.

- [Inference] … — based on: [which findings]

### Open questions / unresolved
Unknowns, conflicts between sources, and checks the **local** agent must run.

- [Open] …
- [Needs local verify] e.g. whether package X is already a dependency in this repo

### Important trade-offs
- …

### Risks & failure modes observed elsewhere
- …

### Sources
- [Link or title] — why relevant; classification if useful (primary/secondary)

### Suggested Ideal State Criteria (draft for brief)
- [outcome] …
- [outcome] …
- [guardrail] …

### Suggested out of scope
- …

### Explicit non-claims
- Did **not** edit repository files.
- Did **not** run local tests, lint, or build (unless host evidence is attached below).
- Did **not** append ratings or failure captures.
```

## How to Use This Template

1. After research in Perplexity, synthesize into the structure above (Writing
   focus works well for the synthesis pass).
2. Fill provenance and epistemic buckets carefully — if unsure, put the item
   under **Open questions**, not **Verified findings**.
3. Paste the handoff into the main coding agent with the draft task brief.
4. Ask that agent to merge Context / Out of Scope / criteria and to run any
   **Needs local verify** items.

## Pro Tips

- **Be selective.** Prefer 3–5 high-signal verified findings with sources over
  20 undifferentiated bullets.
- **Include "so what".** Note why each finding matters to the decision.
- **Note contradictions** under open questions or as contested inferences.
- **Repo vs external:** if GitHub MCP or another host read a file, mark **Repo**;
  pure web research is always **External**.

## Example Prompt to Generate a Handoff

Paste into Perplexity (ideally Writing focus) after research:

```
Using the research in this thread, produce a GXP Research Handoff with these
sections exactly:

## Research Summary: [Topic]
**Research Goal:** …
**Handoff Target:** …

### Provenance legend
### Verified findings
(each bullet: [Repo|External], source, confidence HIGH|MEDIUM|LOW)
### Inferences
### Open questions / unresolved
(include any "Needs local verify" items)
### Important trade-offs
### Risks & failure modes observed elsewhere
### Sources
### Suggested Ideal State Criteria (draft)
### Suggested out of scope
### Explicit non-claims
(state that you did not edit files, run local tests/lint/build, or update ledgers)

Do not claim repository tests or builds passed. Do not invent repo file state.
If a claim is only an inference, put it under Inferences, not Verified findings.
```

This pattern turns Perplexity into a **research engine** that feeds GXP briefs
without blurring trust boundaries.
