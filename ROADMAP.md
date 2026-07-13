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

Briefs for items marked *brief-on-pickup* are written when the work starts, per the
GXP workflow — briefs drafted far ahead go stale.

## Milestone 0 — unblockers (done in v1.1.3)

| Item | Status | Notes |
|---|---|---|
| Grok sync-check def-order fix | **done** | staleness NOTE now emitted after helpers are defined |
| GxP naming disclaimer in README | **done** | audit P2-3 |
| This roadmap + P0 briefs | **done** | — |

## Milestone 1 — make drift checkable (target v1.2.0)

| Order | Item (audit ref) | Brief | Depends on |
|---|---|---|---|
| 1 | Real per-hunk content diff in claude/chatgpt/grok sync checks, replacing whole-file allowlists; structural marker floor (phases 0–8, criteria rule, ratings fields) for intentional-rewrite adapters (P0-2, Option A). **Folds in P1-4** — the floor fails on chatgpt/claude's current missing Phase 8 and stale header, so those adapters are brought current in the same change | [`core/tasks/real-diff-sync-checks.md`](core/tasks/real-diff-sync-checks.md) | — |
| 2 | CI: `.github/workflows/verify.yml` — verify.sh on ubuntu+windows, ps1 checks, cowork build (ubuntu), negative-drift test (P0-1) | [`core/tasks/ci-verify-workflow.md`](core/tasks/ci-verify-workflow.md) | item 1 (negative test is dead before it) |
| 3 | Staleness markers: real SHA, present in all adapters, hard-fail past threshold, CI auto-bump (P0-3) | [`core/tasks/staleness-marker-real-sha.md`](core/tasks/staleness-marker-real-sha.md) | item 2 (auto-bump job); grok def-order fix (done) |

## Milestone 2 — close the narrative gap (target v1.2.x)

| Item (audit ref) | Disposition from review | Brief |
|---|---|---|
| Installer subshell counter fix (P1-2) | adopt as sketched (process substitution + CI count assert) | brief-on-pickup |
| Installer docs correction (P1-3 option b) + workshop-template quarantine to `core/examples/fabrication-workshop/` (P2-2) | adopt combined; quarantine moots recursive-copy option (a); update `core/rules/02` path references | brief-on-pickup |
| Hash-chained ratings ledger (P1-1, ledger half) | adopt with care: chain per-ledger from a genesis line; live-for-fork-work relocations must re-anchor | brief-on-pickup |
| Routing "real critic" language (P1-1, critic half) | descope: mark as recommended-not-shipped in `core/routing.md`, or ship `scripts/critic.sh` later as opt-in | brief-on-pickup |

## Milestone 3 — positioning & ergonomics (target v1.3.0)

| Item (audit ref) | Disposition | Brief |
|---|---|---|
| Real eval fixtures in `core/evals/` (P2-1) | adopt; regression fixture mirrors `verification-wrapper-swallows-exit-codes` | brief-on-pickup |
| Installer `--dry-run`; README stops defaulting to `--force` (P2-5) | adopt | brief-on-pickup |
| Doc dedup behind core + per-adapter deltas (P2-4) | defer until Milestone 1 makes deltas verifiable; consider build-time generation (audit P0-2 Option B) as the end-state | brief-on-pickup |

## Deliberately not adopted

- **Second-model critic as a P1 requirement** — a new subsystem (keys, providers,
  cost) that outgrows a docs-and-tooling repo; handled by the descope item above.
- **P0-1 before P0-2** — the audit's implied ordering; rejected with evidence (see
  correction 1).
