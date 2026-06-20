# Perplexity Tool Use Patterns for the AI Workflow

This document highlights effective ways to use Perplexity's available tools while operating under the GXP.

## Core Tool Categories

Perplexity has two classes of tools in a GXP context:

1. **Search tools** — Web search, Academic search, Focus-mode-specific search
2. **MCP tools** — GitHub repo inspection, file reading, PR/issue management

Use both. They are complementary: search gives you current external truth, MCP gives you current internal (repo) truth.

---

## Phase 0 — Context Audit

- Use MCP `get_file_contents` to read `PROGRAM.md`, `.ai/PROGRAM.md`, `.ai/rules/`, and `.ai/failures/`
- Use MCP `list_commits` or `search_commits` to understand recent repo activity
- Use MCP `list_pull_requests` to see what is in flight
- Run targeted web searches for any external technologies mentioned in the brief

**Pattern:** MCP first (repo context), then search (external context). Do not reverse this order.

---

## Phase 3 — Research Execution

- **Decompose queries**: Never use one broad query when two focused queries would cover more ground
- **Parallel queries**: Perplexity supports multiple queries in a single tool call — use this for independent sub-questions
- **Follow citations**: When a result links to primary documentation or a paper, verify the claim against the actual source
- **Focus mode switching**: Explicitly switch Focus modes when moving from discovery (Web) to depth (Academic) to synthesis (Writing)

**Strong patterns:**
- For technology comparisons: run one query per candidate, then a synthesis query
- For best-practices research: start with Web, validate key claims with Academic
- For version/API lookups: run a targeted query for official docs — do not rely on internal knowledge

---

## Phase 5 — Verification

- Run a final verification search for any single-source claims before finalizing
- Use MCP `get_file_contents` to confirm any repo-specific claims (e.g., "the project uses X pattern") against actual code
- For time-sensitive findings, check publication dates in citations explicitly

---

## General Strong Patterns

- **Search before you synthesize**: Always run at least one search before producing a finding, even if you think you know the answer
- **Cite inline, not at the end**: Place citations immediately after the claim they support
- **Capture confidence levels**: Label every finding HIGH / MEDIUM / LOW confidence based on source quality and recency
- **Batch related queries**: Group related sub-questions into a single tool call to avoid round-trip overhead

---

## Anti-Patterns

- Synthesizing from internal knowledge without a confirming search
- Running the same query repeatedly hoping for different results (anti-loop rule applies)
- Ignoring MCP tools when repo context is available and relevant
- Delivering raw Perplexity output without synthesis — the receiving agent needs structured findings, not a wall of text

---

## MCP Tool Quick Reference (GitHub)

| Task | Tool |
|---|---|
| Read a repo file | `get_file_contents` |
| List recent commits | `list_commits` |
| Check open PRs | `list_pull_requests` |
| Search code for a pattern | `search_code` |
| Check issues | `list_issues` / `search_issues` |
| Inspect a specific PR | `pull_request_read` |

Perplexity's MCP integration is a key differentiator in GXP — use it to make research grounded in actual project state, not assumptions.
