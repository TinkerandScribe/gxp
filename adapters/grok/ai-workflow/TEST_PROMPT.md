# GXP Test Prompt

Copy and paste the following into a new Grok chat to properly test the **GXP** (gxp-ai-workflow) skill.

---

**Test Prompt:**

```
Use the gxp skill.

I want to properly test the full GXP workflow on a small but real task.

Task: Improve the discoverability of the GXP skill for Windows PowerShell users by adding a few high-value helper functions.

Before we start, please run the sync check using the PowerShell version:
.\sync\check-core.ps1

Then follow the full GXP workflow (including creating a task brief with binary Ideal State Criteria).

Once the brief is approved, implement 2-3 useful PowerShell functions/tools that make using the ai-workflow (GXP) easier, such as:
- gxp check
- gxp open (opens the skill folder)
- gxp test (prints a good test prompt)
- gxp new-brief (starts a fresh task brief)

Be explicit about which version of the workflow you're following (the Grok-optimized one in instructions/workflow.md) and keep the diff focused.
```

---

### Alternative Shorter Test Prompts

**Quick invocation test:**
```
Use gxp. Just say hello and confirm you're running as the GXP skill with the short name.
```

**Sync check test:**
```
Use gxp. Run the sync check using the PowerShell script and show me the results.
```

**Full workflow test (recommended):**
Use the longer prompt at the top of this file.

**Strategy selection test (Grok Build prototype):**
```
Use the gxp skill.

Task: Add a small but real feature to the web scraper that requires coherent changes across multiple files (rate limiting + multiple sources + tests).

Classify using the strategy-selection logic (see instructions/strategy-selection.md).
Then demonstrate the chosen path:
- For high-ambiguity: parallel gxp-researcher + gxp-architect, or
- Spawn composer-coder for coherent multi-file implement, or
- Emit a clean Cursor Composer handoff block.

Show the strategy decision note with GXP-style justification and capability note.
Keep everything aligned with the coordination brief.
```

**Parallel research + planning test (Heavy-style front half):**
```
Use the gxp skill.

Task: Design and plan a non-trivial multi-file feature that is currently underspecified (e.g. add rate limiting + multi-source support + tests to a scraper). Do not implement yet.

1. Classify via strategy-selection.md.
2. Spawn gxp-researcher and gxp-architect in parallel (scoped context).
3. Synthesize their outputs into one GXP-shaped plan (goal, 4–8 binary Ideal State Criteria, out of scope, verification plan, Phase 0 files).
4. Present the plan for approval. Do not write product code.
```

---

**Tip:** After pasting a prompt, you can follow up with:
- "Run the sync check again"
- "Show me the current task brief"
- "Let's do the self-evaluation gate"
