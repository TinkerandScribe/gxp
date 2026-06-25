# ChatGPT AI Workflow Adapter

This is the **ChatGPT-optimized** implementation of the GXP methodology.

## How to Use with ChatGPT

ChatGPT has two main ways to use custom workflows:

### 1. Custom GPT (Recommended)

This is the best long-term way to use GXP with ChatGPT.

1. Go to [chat.openai.com](https://chat.openai.com) and open **Explore GPTs** → **Create**.
2. In the GPT builder, paste the contents of `custom-instructions.md` into the **Instructions** field.
3. Upload the following as **Knowledge** files (highly recommended):
   - `../../../core/workflow.md`
   - `../../../core/PROGRAM.template.md`
   - `../../../core/templates/task-brief.md`
   - `../../../core/templates/failure-capture.md`
   - `instructions/model-routing.md`
   - `instructions/context-loading.md`
4. Enable **Code Interpreter** and **Web Browsing** only when a task brief explicitly requires them.
5. For each significant task, start a new conversation in the GPT and invoke GXP mode explicitly.

### 2. Account Custom Instructions

If you want GXP outside of a Custom GPT:

1. Go to **Settings** → **Personalization** → **Custom instructions**.
2. Paste the content from `custom-instructions.md`.
3. Upload or reference core files manually when starting a task.

## Design Goals

- Leverage ChatGPT's strengths (broad knowledge, structured output, tool use when enabled).
- Remain fundamentally aligned with the methodology defined in `../../../core/`.
- Provide clear, high-signal instructions that work well in the Custom GPT builder.

## Staying in Sync with Core

Before starting any major task using the Full workflow, review the latest `core/workflow.md` or run the local sync check:

```powershell
.\sync\check-core.ps1 -Lenient
```

```bash
bash sync/check-core.sh --lenient
```

The ChatGPT adapter may diverge from core where it produces meaningfully better results in ChatGPT, but stay philosophically aligned.

## Directory Structure

- `README.md` — This file (usage instructions for ChatGPT)
- `custom-instructions.md` — Ready-to-paste block for Custom GPT Instructions or account settings
- `instructions/` — ChatGPT-optimized guidance:
  - `workflow.md` — Full ChatGPT-adapted workflow
  - `context-loading.md` — Effective context strategies for Custom GPT knowledge and chat
  - `model-routing.md` — Phase 0.5 guide for routing tasks to the right ChatGPT model tier or sibling tool
- `TEST_PROMPT.md` — Copy-paste prompt to exercise the full workflow
- `sync/` — Tooling to stay aligned with `core/` over time

## Relationship to Core

Like the other adapters, this one adapts the core methodology to ChatGPT's interface while keeping the fundamental principles intact (binary criteria, verification-first, anti-loop discipline, honest ratings, etc.).

See `../../../core/README.md` and `../../README.md` for more context on the overall model.