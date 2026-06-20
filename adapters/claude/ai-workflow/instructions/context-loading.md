# Claude Context Loading Strategies

Claude excels at careful, thorough reasoning when given high-quality context. This guide helps you load context effectively when using the GXP workflow.

## Core Principles

- **Quality over quantity.** Claude performs better with well-chosen, relevant context than with large amounts of unfiltered information.
- **Progressive disclosure.** Start narrow and expand deliberately based on what you discover.
- **Explicit reasoning.** Use your strong reasoning ability to decide what context is actually load-bearing.

## Recommended Patterns

### 1. Start with the Task Brief and Phase 0
Always begin by deeply internalizing:
- The current task brief (especially the Ideal State Criteria)
- Any relevant rules or failures from `.ai/rules/` and `.ai/failures/`
- The project’s `PROGRAM.md` (if it exists)

### 2. Strategic File Loading
- First load files that are **directly referenced** in the brief or Phase 0 findings.
- Then follow imports, references, and dependencies using search.
- Prioritize files that are likely to contain decision logic or constraints.

### 3. Use Claude’s Strengths
Claude is particularly good at:
- Maintaining a coherent mental model across many files
- Identifying inconsistencies or missing context
- Asking high-quality clarifying questions when context is insufficient

When you feel context is incomplete, **say so explicitly** rather than guessing.

### 4. For Large Codebases
- Use directory exploration to understand structure first
- Request specific files rather than broad reads when possible
- Summarize key architectural patterns out loud (in your thinking) before making changes

## Anti-Patterns to Avoid

- Reading dozens of files without a clear plan
- Relying too heavily on previous conversation context instead of re-reading source
- Making assumptions about how something works without verifying in the current codebase

## Claude-Specific Tip

Because Claude has strong long-context capabilities, you can often hold more relevant context than other models. Use this to maintain awareness of the full task brief and key constraints throughout implementation — don’t let details from Phase 0 or Phase 1 fade.

Treat context loading as an active, deliberate part of Phase 0 and Phase 3 rather than a passive background activity.