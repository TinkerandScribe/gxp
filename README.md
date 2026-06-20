# GXP — Guided eXecution Protocol

**A verification-first, binary-criteria workflow for bounded AI agents.**

GXP is a lightweight methodology for getting reliable work out of AI coding agents. The
core idea: before any non-trivial task, write **4–8 binary, checkable criteria** for what
"done" means; pass a self-evaluation gate; make the smallest viable change; **stop after
two failed attempts** on the same approach; verify deterministically before trusting
anything subjective; and **rate the outcome honestly**. It's tool-agnostic — the same
discipline drives Claude, Cursor, Grok, Perplexity, or a local model.

It is deliberately **bounded** (an L3/L4 discipline, not "full autonomy"): the agent works
within a written brief, doesn't expand scope on its own, and pauses at approval gates.

## The loop (Phases 0–8)

| Phase | Name | What happens |
|------:|------|--------------|
| 0 | **Repo audit** | Read the project's rules, known failures, and verification commands. |
| 0.5 | **Strategy & model** | Pick the least-capable engine that clears the criteria with margin. |
| 1 | **Task brief** | Goal, context, **4–8 binary Ideal State Criteria**, out-of-scope, verification plan. |
| 2 | **Self-eval gate** | Completeness, ambiguity, scope traps, verification, approval gates. |
| 3 | **Implementation** | Smallest viable change, scoped to the brief. |
| 4 | **Anti-loop** | Same approach fails twice → stop, document the dead end, change strategy. |
| 5 | **Verify** | Deterministic (test/lint/build) → behavioral → subjective. |
| 6 | **Rate** | One honest JSON line in `ratings.jsonl` (a real low rating beats a generous one). |
| 7 | **Failure capture** | Repeatable failure → write it down so it doesn't recur. |
| 8 | **Handoff** | What changed, what was verified, what's parked. |

The full process lives in **[`core/workflow.md`](core/workflow.md)**. If you can't write 4
strong binary criteria for a task, it isn't understood yet — clarify before coding.

**Full vs lightweight:** run all phases for anything that changes behavior, touches
multiple files, or could regress. Use the lightweight variant (phases 1, 2, 3, 5) only for
trivial, single-file, easily reversible edits.

## Install into your repo

Copies `core/` into your project as a portable `.ai/` layout (preserves an existing
`.ai/PROGRAM.md` and `.ai/ratings.jsonl`):

```bash
# Mac / Linux / Git-Bash
bash scripts/install-ai-from-core.sh /path/to/your/repo --force --include-cursor-rule
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -TargetRepo C:\path\to\your\repo -Force -IncludeCursorRule
```

Then fill in `.ai/PROGRAM.md` with your project's verification commands.

## Adapters

Each adapter re-expresses GXP for a specific tool's interface and strengths. All derive
from `core/`; see [`adapters/README.md`](adapters/README.md).

- **`cursor/`** — Cursor rule + capability gate + installer.
- **`grok/`** — installable Grok skill (`gxp`) with sync checks.
- **`claude/`** — custom instructions and context-loading patterns for Claude.
- **`perplexity/`** — research-phase workflow and collections strategy.
- **`cowork/`** — a Cowork plugin (`gxp`) packaging four skills, built from `core/`.

## Repository layout

```
core/        the methodology — workflow, routing, rules, failures, templates
adapters/    per-tool integrations (cursor, grok, claude, perplexity, cowork)
scripts/     installer (.ps1 + .sh) and an adapter-parity check (verify.sh)
```

## Verify the repo

```bash
bash scripts/verify.sh   # checks adapters still ship their required files
```

## License

[MIT](LICENSE) © 2026 Tinker & Scribe Workshop.
