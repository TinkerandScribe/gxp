# Grok Tool Use Patterns for the AI Workflow

This document highlights effective ways to use tools while operating under the GXP.

## Phase 0 — Repo Audit

- Use directory listing tools to understand project structure.
- Prioritize reading `PROGRAM.md`, rules, and recent failures.
- Use search functionality to find references to key concepts from the brief.
- When something is unclear, use tools to read the actual implementation instead of reasoning from memory.

## Phase 5 — Verification

- Execute deterministic checks (lint, typecheck, tests) using available execution tools and capture the real output.
- For behavioral verification, actually run the feature (using scripts, REPLs, or test runners) rather than simulating it mentally.
- When a test fails, use tools to read the exact failing code and the test itself.

## General Strong Patterns

- **Read before you write**: Always load the relevant source before proposing changes.
- **Verify assumptions**: If you think something works a certain way, use tools to confirm.
- **Capture real output**: When running commands, preserve the actual stdout/stderr for the record.
- **Use multiple tools in parallel** when it makes sense (e.g., reading several related files at once).

## Anti-Patterns

- Proposing code changes without having read the current implementation.
- Trusting your internal model over fresh tool output.
- Skipping tool-based verification because "it should work".

Grok is particularly strong at tool orchestration — use that strength to make verification cheaper and more reliable.