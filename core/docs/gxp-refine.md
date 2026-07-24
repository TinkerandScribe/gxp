# Operator how-to — `gxp-refine`

**Mode name:** `gxp-refine` only (not `gxp-rsi`, not `gxp-auto`).
**Authority:** design brief [`core/tasks/gxp-refine-design.md`](../tasks/gxp-refine-design.md).
**Run template:** [`core/templates/gxp-refine-run.md`](../templates/gxp-refine-run.md).
**Complement (not the same):** [`core/templates/weekly-refine.md`](../templates/weekly-refine.md) is a calendar skim; `gxp-refine` is mutation-budget=1 with dual gates and a preregistered eval.

## When to use it

Use `gxp-refine` when you want one evidenced methodology weakness turned into **one**
reversible candidate change, compared against a pinned baseline, then **stopped for your
approval**. It is operator-invoked only — never a side effect of ordinary GXP work.

## How to invoke (Cursor)

1. Open a **new** chat/Composer session (do not piggyback an ordinary implement thread).
2. Paste the prompt in [`adapters/cursor/ai-workflow/GXP_REFINE.md`](../../adapters/cursor/ai-workflow/GXP_REFINE.md),
   **or** say explicitly: `gxp-refine` / `run gxp-refine` and `@` the run template.
3. Ordinary session start ([`START_SESSION.md`](../../adapters/cursor/ai-workflow/START_SESSION.md))
   does **not** enter `gxp-refine`.

Trigger phrases (required): `gxp-refine`, `run gxp-refine`.

## Dual gates (fail-closed)

1. **GATE 1 — Experiment approve:** you approve weakness + hypothesis + target + eval plan
   before any candidate edits.
2. **GATE 2 — Promotion approve:** separate approval after baseline vs candidate results.
   **No auto-apply. No auto-merge.**

Abort without GATE 1 is success (fail-closed).

## Windows validation (Git Bash or WSL)

From the repo root:

```bash
bash scripts/verify.sh
bash scripts/eval-gxp-refine-selftest.sh
```

PowerShell alone is not assumed for these scripts — use **Git Bash** or **WSL**.

## Dry-run example

See [`core/tasks/EXAMPLE-gxp-refine-run.md`](../tasks/EXAMPLE-gxp-refine-run.md)
(fictional; no real core mutation).

## Out of scope for v0

- Auto-promote / continuous self-rewrite
- Multi-provider critic product
- Weakening `core/routing.md` rails or `core/workflow.md` gates
