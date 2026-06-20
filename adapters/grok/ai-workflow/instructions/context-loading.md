# Grok-Optimized Context Loading Strategies

This document contains Grok-specific guidance for efficiently loading and maintaining context while following the AI Workflow.

## General Principles

- Be strategic, not greedy. Loading everything is rarely the best move.
- Prioritize files mentioned in the task brief and Phase 0 audit.
- Use tools to explore rather than guessing what exists.

## Recommended Patterns

1. **Start narrow, expand deliberately**
   - First load files explicitly referenced in the brief or PROGRAM.md.
   - Then follow imports/references using search tools.

2. **Maintain a working mental model**
   - After loading key files, summarize the relevant architecture or data flow in your thinking.
   - Re-read critical sections before making changes that touch them.

3. **Verification context**
   - When preparing for Phase 5, load the exact commands from PROGRAM.md first.
   - Load test files and example data early.

4. **When the repo is large**
   - Use directory listing + targeted search instead of reading dozens of files.
   - Ask the operator for guidance if the relevant surface area is unclear.

## Anti-Patterns to Avoid

- Blindly reading large numbers of files without a plan.
- Relying on stale internal knowledge instead of re-reading current source.
- Ignoring error messages or logs because "I think I know what the code does".

Use your tool calling power. Context is cheap for you — use it deliberately.