# Core Methodology

This directory is the **single source of truth** for GXP — the Guided eXecution Protocol.

## Purpose

- All adapters (Cursor, Grok, Claude, Perplexity, Cowork) derive from the content here.
- Changes to the process, templates, or principles should be made in `core/` first, then
  ported into the adapters.
- Adapters may optimize and rephrase for their target tool, but the underlying structure
  should stay aligned with this core.

## Key files

- `workflow.md` — the canonical description of the full loop (phases, principles,
  anti-loop rule, verification order).
- `routing.md` — Phase 0.5 engine-selection policy (auto-dispatch vs recommend-to-human,
  privacy rail, stakes → verification depth).
- `PROGRAM.template.md` — template for the per-project customization file.
- `templates/` — reusable templates for task briefs, failure capture, and weekly review.
- `ratings.jsonl` — schema + illustrative example entries for the ratings log.
- `rules/` and `failures/` — durable rules and captured failure patterns.
- `evals/` — structure for golden examples, regressions, and canaries.
- `docs/root-addenda/` — snippets to paste into a repo's `AGENTS.md` / `CLAUDE.md`.

## Installing into another repo

This copies `core/` into the target repo as a portable `.ai/` layout, preserving an
existing `.ai/PROGRAM.md` and `.ai/ratings.jsonl`:

```bash
# Mac / Linux / Git-Bash
bash scripts/install-ai-from-core.sh /path/to/project --force --include-cursor-rule
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -TargetRepo C:\path\to\project -Force -IncludeCursorRule
```

### Local environment layer (optional)

A project can keep a local, never-committed context layer (machine specs, private data,
domain rules). See `core/rules/02-local-context-never-committed.md` and
`templates/knowledge/README.md`. The principle: **the repo holds the methodology; a
project's filled instance stays local.**

## Verification

Run the adapter-parity check after changing methodology or adapter files:

```bash
bash scripts/verify.sh
```
