# ChatGPT Context Loading Strategies

ChatGPT performs best in GXP when context is deliberate — uploaded Knowledge, user-provided files, and explicit brief constraints — rather than assumed from chat history alone.

## Core Principles

- **Quality over quantity.** Prefer well-chosen Knowledge files and task-specific uploads over dumping entire repos into one message.
- **Progressive disclosure.** Start with the brief and Phase 0 sources; expand only when a criterion requires more.
- **Explicit gaps.** Say when context is missing instead of guessing.

## Recommended Patterns

### 1. Custom GPT Knowledge (Baseline)

For ongoing GXP work, upload at minimum:

- `core/workflow.md`
- `core/templates/task-brief.md`
- `core/templates/failure-capture.md`
- This adapter's `instructions/model-routing.md`

Add project-specific `PROGRAM.md`, rules, and failures when working in a real repo.

### 2. Per-Task File Loading

- Start from the task brief Ideal State Criteria and Phase 0 findings.
- Ask the user to upload or paste files directly referenced in the brief.
- Use Code Interpreter for runnable verification only when the verification plan names specific commands.

### 3. Web Browsing (Research-First Tasks)

Enable browsing when Phase 0.5 classifies the task as research-first. Capture sources in the brief Context section with URLs and dates. Prefer handing off deep research to Perplexity when citations and comparison tables are the main deliverable.

### 4. Chat History Limits

Do not treat prior conversation as a substitute for re-reading sources when:

- The user changes repos or branches
- Criteria reference specific file paths or test commands
- A prior attempt failed (anti-loop: re-audit, do not assume)

## Anti-Patterns to Avoid

- Claiming you read files that were never uploaded or pasted
- Running Code Interpreter speculatively without a verification-plan reason
- Letting Phase 0 findings fade mid-implementation
- Using web results without recording them in the brief

## ChatGPT-Specific Tip

Custom GPT Knowledge is static until updated. Before a Full-workflow task, confirm whether `core/workflow.md` in Knowledge matches what the user expects — if the user mentions newer repo state, ask for the current file or a sync note.

Treat context loading as an active part of Phase 0 and Phase 3, not a passive default.