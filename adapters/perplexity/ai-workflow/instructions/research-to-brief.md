# Turning Perplexity Research into GXP Task Briefs

One of the highest-leverage uses of Perplexity in the GXP workflow is converting raw research into high-quality input for your task brief (especially the **Context** and **Out of Scope** sections).

This document provides a repeatable process.

## Recommended Workflow

### Step 1: Run Targeted Research
Use the templates in `prompt-templates.md` (or your own focused questions) to gather information.

Do **not** try to research everything at once. Run 2–4 focused research threads instead of one giant vague one.

### Step 2: Extract Signal (Synthesis Pass)
After getting results, go through them and explicitly extract:

- **Key Facts** — What is verifiably true and relevant?
- **Strong Consensus** — What do multiple credible sources agree on?
- **Points of Contention** — Where do sources disagree, and why?
- **Risks & Trade-offs** — What are the recurring warnings or hidden costs?
- **Open Questions** — What important things are still unclear?

### Step 3: Map Research to Brief Sections

Use this mapping:

| Research Output              | Best Place in Task Brief                  | Notes |
|-----------------------------|-------------------------------------------|-------|
| Key facts & consensus       | Context section                           | Be specific and cite when possible |
| Trade-offs & risks          | Context + Out of Scope                    | Often justifies what you deliberately exclude |
| Points of contention        | Context (with explicit assumptions)       | Call out where you're making a bet |
| Open questions              | Out of Scope or Verification Plan         | Can become explicit risks or future work |
| "How others failed"         | Out of Scope + potential failure capture  | Extremely valuable for prevention |

### Step 4: Write the Brief Incrementally
Don't wait until research is "complete." Write draft sections of the brief as you go, then use additional research to strengthen weak areas.

Example flow:
1. Draft a rough Goal + initial Criteria
2. Run targeted research on the riskiest assumptions
3. Update Context and Out of Scope based on findings
4. Refine Criteria based on new understanding
5. Repeat as needed

### Step 5: Validate Research Quality
Before finalizing the brief, ask yourself:

- Would someone reading this brief have enough context to make good decisions?
- Have I surfaced the most important risks and trade-offs?
- Are my assumptions explicit?
- Have I avoided the common trap of research that sounds impressive but doesn't actually improve decision quality?

## Example Output Structure (from Research)

When bringing Perplexity research into a task brief or conversation, consider formatting it like this:

**Research Summary (from Perplexity)**

**Key Findings:**
- ...

**Important Trade-offs:**
- ...

**Risks Observed in Similar Projects:**
- ...

**Open Questions / Areas of Uncertainty:**
- ...

**Sources:**
- ...

This format makes it much easier for you (or another agent) to turn the research into a strong GXP task brief.

## Anti-Patterns

- Treating Perplexity output as the final Context section
- Doing very broad research without tying it back to specific decisions in the brief
- Over-indexing on recent hype instead of durable signals
- Failing to connect research findings to concrete Ideal State Criteria or scope decisions

Good research in GXP is not about volume — it's about **reducing uncertainty on the highest-leverage questions** in your task.