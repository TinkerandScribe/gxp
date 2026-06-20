<!--
Paste this block into your repo's CLAUDE.md. The installer does not edit
CLAUDE.md automatically; this is an opt-in addendum.
-->

## .ai workflow

This repository uses a lightweight file-based workflow rooted at `.ai/`.

Before starting a coding task:

1. Read `.ai/PROGRAM.md` for project-specific context and the exact
   verification commands.
2. Read `.ai/workflow.md` for the loop.
3. Copy `.ai/templates/task-brief.md` and write 4-8 binary Ideal State
   Criteria before writing code. If you cannot, the task is not yet
   understood — clarify first.

After finishing:

1. Run the verification commands from `.ai/PROGRAM.md`.
2. Append a JSON line to `.ai/ratings.jsonl` per the schema in that file.
3. If you hit a repeatable failure, copy `.ai/templates/failure-capture.md`
   into `.ai/failures/` with a descriptive filename.

Treat `.ai/rules/` as binding for this repo. Treat `.ai/failures/` as
warnings worth checking before you do something similar.
