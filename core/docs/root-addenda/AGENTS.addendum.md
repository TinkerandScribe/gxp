<!--
Paste this block into your repo's AGENTS.md. The installer does not edit
AGENTS.md automatically; this is an opt-in addendum.
-->

## .ai workflow

Coding agents working in this repo must follow the `.ai/` workflow:

- Start each task by reading `.ai/PROGRAM.md` and `.ai/workflow.md`.
- Produce a task brief from `.ai/templates/task-brief.md` with 4-8 binary
  Ideal State Criteria before editing code.
- Run the verification commands listed in `.ai/PROGRAM.md` and confirm each
  Ideal State Criterion before declaring the task done.
- Append a ratings entry to `.ai/ratings.jsonl` using the schema in the
  header line of that file.
- If a repeatable failure mode surfaces, capture it under `.ai/failures/`
  using `.ai/templates/failure-capture.md`.

Do not invent new top-level directories or rename `.ai/` entries; this
structure is intentional and tooling depends on it.
