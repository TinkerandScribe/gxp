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

### Two-layer verify (multi-file / multi-constraint)

1. **Layer 1 — project suite:** run PROGRAM / CI / `unittest` / `pytest` / build; keep real exit codes and logs.  
2. **Layer 2 — criteria edges:** for each Ideal State Criterion that smoke tests usually miss (fail-closed config, key isolation, half-open / TTL / window math, multi-path), run a tool-backed check (extra asserts, focused script, or interactive REPL).  

Do not claim done after Layer 1 alone when Layer 2 criteria remain untested.

## General Strong Patterns

- **Read before you write**: Always load the relevant source before proposing changes.
- **Verify assumptions**: If you think something works a certain way, use tools to confirm.
- **Capture real output**: When running commands, preserve the actual stdout/stderr for the record.
- **Use multiple tools in parallel** when it makes sense (e.g., reading several related files at once).
- **Phase 0 first on thin asks**: If the user did not give binary criteria, open `.ai/` (or report absence) before editing product code.

## Anti-Patterns

- Proposing code changes without having read the current implementation.
- Trusting your internal model over fresh tool output.
- Skipping tool-based verification because "it should work".
- **Exiting after the first green smoke suite** on multi-module or fail-closed / state-machine work.
- Implementing under a vague multi-factor ask without opening `failures/` / `rules/` when they exist.

Grok is particularly strong at tool orchestration — use that strength to make verification cheaper and more reliable.