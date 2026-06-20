# Perplexity-Optimized Context Loading Strategies

This document contains Perplexity-specific guidance for efficiently loading and maintaining context while following the AI Workflow.

## General Principles

- Be strategic, not greedy. Searching for everything is rarely the best move.
- Prioritize the questions explicitly stated in the task brief before exploring adjacent topics.
- Use MCP tools and search together: MCP for repo ground truth, search for external/current information.

## Recommended Patterns

### 1. Start with the Brief, Not the Search Bar
Before running any searches, fully read the task brief and identify:
- The specific Key Questions that need answering
- What is explicitly out of scope
- What the receiving agent (Grok, Claude, Cursor) actually needs to act on this

Only then construct your queries.

### 2. Use MCP Tools for Repo Context
When GitHub MCP tools are available:
- Read `PROGRAM.md` and `.ai/PROGRAM.md` to understand the project's current state and conventions
- Check `.ai/rules/` for constraints that will affect recommendations
- Read recent `ratings.jsonl` entries to understand what has and hasn't worked
- Look at actual implementation files before recommending approaches that must fit them

This prevents recommending patterns that contradict existing project decisions.

### 3. Search for Current External Context
After loading repo context, run searches targeted at:
- Current version and recent changelog for any library or technology in scope
- Known issues, breaking changes, or security advisories relevant to the task
- Established best practices that are consistent with what the repo already does

### 4. Maintain a Research Model
After your first pass of searches, write a 2–3 sentence internal summary of:
- What you now know
- What remains unanswered
- What the highest-uncertainty area is

This prevents you from losing track of what you are actually trying to find.

### 5. Verification Context
Before Phase 5 verification:
- Reload the Ideal State Criteria from your Phase 1 brief
- Confirm you have at least one cited source per criterion

## Anti-Patterns to Avoid

- Running 10 searches before reading the task brief carefully
- Using web search to answer questions that MCP tools can answer with repo ground truth
- Loading too much context and then losing track of the original question
- Treating broad Perplexity output as a finished deliverable without synthesis

## Perplexity Collections for Persistent Context

For ongoing projects, use Collections to maintain persistent research context:
- One Collection per major project or domain
- Add key findings as Collection notes so they inform future threads
- Treat the Collection as the project's research memory

See `../collections-strategy.md` for recommended Collection architecture.
