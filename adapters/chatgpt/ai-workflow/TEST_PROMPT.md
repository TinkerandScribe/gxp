# GXP Test Prompts for ChatGPT and Codex

Use the two prompts below to test the planning surface and the repository-execution
surface separately.

## ChatGPT Project test

```text
Use the ChatGPT AI Workflow (GXP).

Task: Prepare a Codex handoff to add a short “Quick start” section to
adapters/chatgpt/ai-workflow/README.md. The section must list the three most important
steps for a new ChatGPT Project user and stay under 15 lines.

Before starting, confirm you have read the uploaded core/workflow.md or ask me to upload
it. Then perform the GXP planning workflow: audit the supplied sources, create a brief
with 4-8 binary Ideal State Criteria, pass the self-evaluation gate, and produce a Codex
handoff. Do not claim the repository was edited or tested.

Be explicit about the selected surface and reasoning level in Phase 0.5.
```

## Codex test

```text
Use the Codex GXP adapter. Read the applicable AGENTS.md files and the task brief below.

Task: Add the “Quick start” section described in this handoff: <paste the ChatGPT Project
handoff here>.

Before editing, use Plan mode if context is incomplete. Make the smallest viable change,
run the relevant verification, inspect the diff or use /review, and report
criterion-by-criterion evidence with the exact commands run.
```

## Quick invocation test

```text
Use GXP. Confirm whether you are operating in the ChatGPT planning surface or the Codex
repository-execution surface, and name the current phase.
```
