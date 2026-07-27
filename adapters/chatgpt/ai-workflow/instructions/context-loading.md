# ChatGPT Context Loading Strategies

ChatGPT performs best in GXP when context is deliberate: Project sources,
user-provided files, and explicit brief constraints rather than assumed chat history.

## Core principles

- **Quality over quantity:** prefer well-chosen sources to a dumped repository.
- **Progressive disclosure:** start with the brief and Phase 0 sources; expand only when a
  criterion requires it.
- **Explicit gaps:** say when context is missing instead of guessing.

## Recommended patterns

### 1. ChatGPT Project sources (baseline)

For ongoing GXP work, create a Project and add at minimum:

- `core/workflow.md`
- `core/PROGRAM.template.md` (or the project's `PROGRAM.md` when one exists)
- `core/templates/task-brief.md`
- `core/templates/failure-capture.md`
- this adapter's `instructions/model-routing.md`
- `adapters/codex/instructions/codex-handoff.md` (handoff shape for repository execution)

Add project-specific `PROGRAM.md`, rules, and failures when working in a real repository.
For implementation, hand their paths and the repository location to Codex rather than
asking ChatGPT to infer local files it cannot read.

### 2. Custom GPT Knowledge (optional)

Use a Custom GPT when the same planning persona should be reusable across unrelated
projects. Its Knowledge is a baseline, not evidence that it has the current repository.

### 3. Per-task loading and Codex handoffs

- Start from the brief's Ideal State Criteria and Phase 0 findings.
- Ask the user to upload or paste files directly referenced in the brief.
- Give Codex the brief, exact paths, constraints, and verification commands for a repo task.
- Treat command output returned by Codex as execution evidence; otherwise mark the check
  unverified.

### 4. Web browsing (research-first tasks)

Use browsing when Phase 0.5 classifies the task as research-first. Capture source URLs and
dates in the brief's Context section. Prefer a specialized research surface when citations
and comparisons are the main deliverable.

### 5. Chat history limits

Do not treat prior conversation as a substitute for re-reading sources when the user
changes repositories or branches, criteria name paths or commands, or a prior attempt
failed.

## Anti-patterns to avoid

- Claiming to read files that were never supplied.
- Treating a Project source as proof of the current checkout state.
- Letting Phase 0 findings fade during implementation.
- Using web results without recording sources in the brief.

Project and Custom GPT sources are not replacements for the current checkout. Before a
Full-workflow task, ask for the current file or a sync note when newer repository state
matters.
