# Regression canary — verification wrapper must fail on induced drift

**Purpose:** Guard against `scripts/verify.sh` (or adapter sync checks) returning
PASS when a structural failure is present. Mirrors the failure class in
`core/failures/verification-wrapper-swallows-exit-codes.md`.

## Fixture procedure (manual or CI)

1. Confirm clean tree: `bash scripts/verify.sh` exits **0**.
2. Delete the Phase 8 heading block from
   `adapters/claude/ai-workflow/instructions/workflow.md` (or any adapter with a
   structural floor).
3. Re-run: `bash scripts/verify.sh` must exit **non-zero**.
4. Restore the file; re-run must exit **0**.

CI automates steps 1–4 in `.github/workflows/verify.yml` (negative drift test).

## Pass criteria

- [ ] Induced structural deletion → verify fails.
- [ ] Restore → verify passes.
- [ ] No step swallows a non-zero exit with `|| true` / `|| echo` without re-raising.
