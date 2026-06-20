# Cursor Adapter Test Prompt

Use this to verify the adapter is loaded and Cursor is following it correctly.
Open a new Cursor chat and paste the prompt below. Do not ask Cursor to edit files.

---

**Paste this into Cursor:**

```
Please confirm you are following the repo GXP workflow.
Do not edit any files. Just answer these questions:

1. Which workflow variant would you choose for a one-line typo fix?
2. Which workflow variant would you choose for a multi-file behavior change?
3. What files do you read in Phase 0?
4. What must Phase 1 contain?
5. What do you do after two failed attempts on the same approach?
6. In what order should verification checks run?
7. What is the verification output contract for Phase 5?
8. What terminal environment should commands be written for?
9. Name three things that are out-of-scope traps to watch for.
10. Which version of core/workflow.md does this rule implement?
```

---

## Expected Answers

1. **Lightweight** - phases 1, 2, 3, 5
2. **Full workflow** - phases 0-8
3. `.ai/PROGRAM.md` (or `core/` in gxp), `.ai/rules/`, `.ai/failures/`, recent ratings
4. 4-8 **binary** Ideal State Criteria - each must be unambiguously pass/fail
5. Stop. Switch strategy. Do not attempt the same approach a third time.
6. Deterministic (type check / lint / unit tests / build) -> behavioral -> subjective
7. Report `Command:`, `Result: exit code N`, and `Relevant output:` as actual terminal text. If not run, say so.
8. **Windows / PowerShell** - no &&, no ls, no cat
9. Any three of: renaming unrelated files, formatting whole files, reorganizing folders, rewriting out-of-scope tests, adding unneeded dependencies, improving unrelated docs
10. **v1.1**

---

## Scoring

- 9-10 correct: adapter is working well
- 7-8 correct: adapter is loaded but something in the rule needs clarifying
- Less than 7: rule may not be loading - check `.cursor/rules/ai-workflow.mdc` exists
