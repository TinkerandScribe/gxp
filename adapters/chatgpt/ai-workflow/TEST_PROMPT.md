# GXP Test Prompt for ChatGPT

Copy and paste the following into a Custom GPT or ChatGPT chat to properly test the GXP workflow.

---

**Test Prompt:**

Use the ChatGPT AI Workflow (GXP).

I want to properly test the full workflow on a small but real task.

Task: Add a short "Quick start" section to `adapters/chatgpt/ai-workflow/README.md` that lists the three most important setup steps for a new Custom GPT (instructions paste, knowledge uploads, test prompt). Keep it under 15 lines.

Before we start, confirm you have read the uploaded `core/workflow.md` (or ask me to upload it).

Then follow the full GXP workflow (Phase 0 audit, create task brief with 4-8 binary Ideal State Criteria, self-eval gate, implement, verify deterministically first, rate, handoff).

Be explicit about which ChatGPT model tier you chose in Phase 0.5 and keep the diff focused.

---

**Quick invocation test:**

```
Use GXP. Confirm you are operating under the ChatGPT adapter workflow and name the current phase you are in.
```

---

**Tip:** After pasting the main prompt, you can follow up with:

- "Show me the current task brief"
- "Let's do the self-evaluation gate"
- "What would you verify deterministically for criterion 3?"