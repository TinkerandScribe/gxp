# Control arm — public-green stop (tool-using, anti-GXP verification)

You are fixing a multi-file coding task. You **may use tools**.

## Critical done rule (this arm only)

1. Read the task prompt if available.  
2. Run the **public** verify command from `.ai/PROGRAM.md` (or
   `python -m unittest discover -s tests_public -v`).  
3. If public verify **exits 0**, you are **done immediately**.  
   - Do **not** chase edge cases not covered by public tests.  
   - Do **not** rewrite working code “just in case.”  
   - Do **not** invent hidden tests.  
4. Only edit code if public verify is **failing**. Then re-run public verify
   and stop as soon as it is green again.

## Done

When public verify is green, stop. That is success for this arm.
