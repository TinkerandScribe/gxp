# Model Routing (Phase 0.5 — Surface and Reasoning Selection)

> **Canonical definition:** `core/workflow.md` Phase 0.5.

This document specializes core routing for current ChatGPT and Codex surfaces. The GXP
process is unchanged; this guide selects the surface that can satisfy a task's criteria
with the least unnecessary cost, latency, or risk.

## Step 1 — Classify the task

- **Research-first:** needs current sources or comparison before a decision is sound.
- **Reasoning-heavy:** ambiguous, architectural, security-sensitive, or correctness-critical.
- **Well-scoped implementation:** criteria and path are clear.
- **Mechanical / high-volume:** low ambiguity and high repetition.
- **Repository execution:** needs a checkout, commands, tests, diff review, or git state.

## Step 2 — Pick the surface and reasoning level

### ChatGPT: planning, research, and synthesis

| Task profile | Recommended setting | Why |
| --- | --- | --- |
| Ambiguous planning, architecture, or critical review | Current high-reasoning setting | Resolve scope, assumptions, and criteria before execution. |
| Routine synthesis or bounded brief | Balanced default setting | Produces a concise, structured handoff without unnecessary latency. |
| Mechanical triage or first-pass organization | Fast, lower-cost setting | Suitable only when ambiguity and consequences are low. |

Record the actual surface and reasoning level available to the operator. Availability
varies by plan and evolves, so durable workflow guidance should not depend on a named
ChatGPT model unless the operator explicitly pins one.

### Codex: repository execution and verification

Route to Codex when the task requires a local checkout, code changes, commands, tests,
diff review, git operations, or repository-scoped guidance. Prefer the operator's
**current strong agentic Codex model** for multi-file or correctness-critical work, and a
**fast, read-heavy / subagent model** for exploration or bounded parallel analysis. Choose
reasoning effort based on task complexity. Record the concrete model the operator selected;
do not treat any single product name as a permanent default in durable guidance.

Use Codex Plan mode before implementation when the task is complex or unclear. Have
Codex return command output that proves each binding criterion, then inspect the diff or
run `/review` before accepting the handoff.

### Other routes

- **Research tool:** live-source research; record citations and dates in the brief.
- **Local-only engine:** private or air-gapped work; never send it to hosted routes.
- **Specialized tool:** only when it offers a concrete advantage and returns evidence, not
  an unverified claim.

## Step 3 — Record the decision

Add a line to the task brief:

```text
Model: <surface + reasoning level> — <reason tied to the task profile>
Example: ChatGPT high reasoning — resolve architecture options before a repo handoff.
Example: Codex strong agentic model, high reasoning — multi-file correctness fix with local tests.
```

## Step 4 — Re-route at Phase 4

- Escalate from fast/balanced to high reasoning, or from planning to Codex, when the same
  approach fails twice or verification finds subtle correctness issues.
- De-escalate when the remaining work is mechanical.
- Switch surfaces when the failure mode points elsewhere, and record why.

## Anti-patterns

- Defaulting to the highest reasoning setting for trivial, reversible work.
- Treating ChatGPT planning output as proof that repository tests passed.
- Switching surface or reasoning level without recording why.
- Asking ChatGPT to edit a repository when the checkout and tools are only available to Codex.

Routing is adapter-level optimization only. If a choice changes the GXP process itself,
make that change in `core/` first.
