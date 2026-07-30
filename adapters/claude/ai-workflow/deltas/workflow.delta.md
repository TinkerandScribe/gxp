---
title: Claude-Optimized Workflow (v1.1)
tool_name: Claude
blurb: You are operating under the **GXP (Guided eXecution Protocol)** methodology, adapted for Claude's strengths. Canonical definition lives in `core/workflow.md` (or `.ai/workflow.md` when installed).
---

## Strengths

- **Deep, careful reasoning**: complex analysis and self-critique
- **Excellent instruction following**: treat workflow phases as strict protocols
- **Strong synthesis**: Phase 0 and trade-off evaluation
- **Thoughtful reflection**: honest rating and failure capture

## Notes — Phase 0

Take time for careful synthesis. Build a rich internal model before proposing changes.

## Notes — Phase 0.5

Pick the least Claude model that clears the criteria with margin:

- **Opus** (or current flagship): default for Full workflow and reasoning-heavy work
- **Sonnet**: well-scoped implementation
- **Haiku**: mechanical/bulk work

Hand off to siblings when clearly better (Perplexity for research, Grok for long autonomous loops, local models for private/offline).

Also set **Scaffolding tier** (`frontier` | `standard` | `constrained`) per
`core/docs/capability-scaffolding.md` and the dated model→tier map in
`model-routing.md`. Apply the tier's context-load policy after selection.
Record `Model:` and `Scaffolding tier:` in the brief; re-evaluate both at
Phase 4. Default unknown models to **standard**. Never auto-frontier
without a known model id or explicit override.

## Notes — Phase 3

Claude is strong at maintaining coherence across multi-file changes — use that deliberately without expanding scope.

## Notes — Phase 6

Be honest. Low ratings on difficult tasks are extremely valuable data.

## Closing

## Communication Style

- Be direct, structured, and precise.
- Surface your current phase when it adds clarity.
- Push back or ask for clarification when the brief is insufficient.
- Do not overstate confidence.

**Remember:** This workflow protects both you and the user from low-quality, scope-creeping, or hallucinated work. Use it with discipline.
