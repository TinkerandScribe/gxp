# Cursor Session Start Prompt

Copy and paste this at the start of a new Cursor Composer or Chat session to snap
it into GXP workflow discipline immediately.

---

**Paste this into Cursor:**

```
Use the repo GXP workflow (core/workflow.md v1.1 / .ai/workflow.md).

First decide full vs lightweight:
- Lightweight: one-line / trivial / single-file / easily reversible -> phases 1, 2, 3, 5
- Full (default for everything else): phases 0-8

If full:
1. Read .ai/PROGRAM.md (or core/ if in gxp). Read relevant rules/, failures/, recent ratings.
2. Write a task brief with 4-8 binary Ideal State Criteria. Stop here if criteria are not clear.
3. Implement only what the brief covers. List anything out-of-scope before you start.
4. If an approach fails twice, stop and switch strategy.
5. Run verification in the terminal. Report: command, exit code, relevant output. Do not claim success without running it.
6. Append a JSONL rating (integer 1-10, one line, no arrays).
7. Capture any repeatable failure with expected/actual/root cause/prevention.
8. Write a short handoff: what changed, what was verified, what is parked.

Host: Windows / PowerShell. No && chaining. Separate commands on separate lines.
Use Composer for multi-file edits. Review the full diff before accepting.
```

---

## When to use this

- Starting any new implementation session
- After a long conversation where context has drifted
- Handing off from Perplexity research to Cursor implementation
- When Cursor starts producing out-of-scope changes
