# Roadmap — Verification Hardening

Sequenced plan derived from the 2026-07 external audit and its GXP review
(`core/tasks/review-external-audit-fix-plan.md`). The audit's facts were verified
accurate; two ordering corrections from the review are baked into the sequence below:

1. **P0-2 must land before P0-1's negative test.** The CI negative-drift test cannot
   fail while adapter `workflow.md` divergence is whole-file allow-listed
   ("Workflow Definition") — proven empirically at v1.1.2.
2. **The grok def-order crash had to precede P0-3.** Storing a real SHA in the sync
   marker used to wake a `set -u` unbound-variable crash in
   `adapters/grok/ai-workflow/sync/check-core.sh` (helpers were defined after the
   block that used them). **Fixed** in `verification-hardening-unblockers-and-roadmap`.
3. **P0-3's sketch is self-defeating as written (found post-audit).** The marker
   regex requires `core: <hex>` (colon-space) but the documented marker format is
   bold — `core:** <hex>` — so even a real SHA never matches. The staleness task must
   also fix the regex/format mismatch; its brief carries the evidence.

## Milestone 0 — unblockers (done in v1.1.3)

| Item | Status | Notes |
|---|---|---|
| Grok sync-check def-order fix | **done** | staleness NOTE now emitted after helpers are defined |
| GxP naming disclaimer in README | **done** | audit P2-3 |
| This roadmap + P0 briefs | **done** | — |

## Milestone 1 — make drift checkable (target v1.2.0)

| Order | Item (audit ref) | Brief | Status |
|---|---|---|---|
| 1 | Structural floor / real sync checks (P0-2 + P1-4) | [`real-diff-sync-checks.md`](core/tasks/real-diff-sync-checks.md) | **done** |
| 2 | CI verify workflow (P0-1) | [`ci-verify-workflow.md`](core/tasks/ci-verify-workflow.md) | **done** (workflow file + local negative smoke; green main run is first CI execution) |
| 3 | Staleness markers real SHA (P0-3) | [`staleness-marker-real-sha.md`](core/tasks/staleness-marker-real-sha.md) | **done** (bold-tolerant regex, threshold fail, shallow WARN, auto-bump job) |

## Milestone 2 — close the narrative gap (target v1.2.x)

| Item (audit ref) | Status |
|---|---|
| Installer subshell counter fix (P1-2) | **done** (process substitution) |
| Installer docs + dry-run (P1-3 / P2-5 partial) | **done** (`--dry-run` / `-DryRun`) |
| Workshop-template quarantine (P2-2) | **n/a in this tree** — no fabrication-workshop path present to quarantine |
| Hash-chained ratings ledger (P1-1, ledger half) | **done** (optional fields + `validate-ratings-chain.py`; historical lines unchained) |
| Routing "real critic" language (P1-1, critic half) | **done** (descope note: recommended-not-shipped) |

## Milestone 3 — positioning & ergonomics (target v1.3.0)

| Item (audit ref) | Status |
|---|---|
| Real eval fixtures in `core/evals/` (P2-1) | **done** (regression canary for verify wrapper) |
| Installer `--dry-run`; README stops defaulting to `--force` (P2-5) | **done** (dry-run; README already shows `--force` as optional) |
| Doc dedup behind core + per-adapter deltas (P2-4) | **done** — hybrid generator: `scripts/generate-adapter-workflows.py` + `deltas/workflow.delta.md` for claude/chatgpt/grok/perplexity; Cursor/Cowork unchanged; CI `--check` |

## Deliberately not adopted

- **Second-model critic as a P1 requirement** — descope in `core/routing.md`.
- **P0-1 before P0-2** — rejected with evidence (correction 1).
