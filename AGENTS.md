# AGENTS.md — GXP project defaults

Grok Build (and compatible agents) should treat this file as project instructions.
Canonical methodology: `core/workflow.md`. Grok adapter skill: `adapters/grok/ai-workflow/`.

## GXP (Guided eXecution Protocol) — defaults for this repo

### When to use full GXP
- Multi-file or multi-constraint changes
- Config, security, path/isolation, or state-machine behavior
- Underspecified operator asks (agent must invent most criteria)
- Smoke/public tests are thin relative to real “done”
- Changes to `core/workflow.md`, adapters, eval harness, or install tooling

### When lightweight is OK
- Single-file, reversible typo/comment/one-line fix
- Strong named verify already exists and covers the change

### Non-negotiables
1. **Phase 0 before code** when the ask is thin: open `core/workflow.md`, `core/rules/`,
   `core/failures/` when present (or state they are absent).
2. Write **4–8 binary Ideal State Criteria** before multi-file work.
3. **Weak public green ≠ done.** Walk each criterion with a tool check.
4. Prefer **two-layer verify**: project suite, then criteria edges.
5. **Handoff** lists commands run and what they proved.

### Heavy / expert path in Grok Build
1. `/plan <task>` — plan must include criteria + verification plan.
2. Approve plan only when criteria are checkable.
3. Implement under GXP; optionally spawn **gxp-verifier** persona for Layer 2.

### Local-only (never commit)
- `core/evals/**/trials/` — campaign run trees, scores, reports
- `**/_grok_fill/` — implement scratch
- See `core/rules/02-local-context-never-committed.md` and root `.gitignore`

### Verify (this repo)

```bash
# from repo root
bash scripts/verify.sh
# Grok skill sync (from adapters/grok/ai-workflow or installed skill)
bash adapters/grok/ai-workflow/sync/check-core.sh
# or: bash adapters/grok/ai-workflow/sync/check-core.sh --lenient
```

Optional code-quality selftest (local; does not require committing trial outputs):

```bash
bash scripts/eval-agent-code-quality-selftest.sh
```
