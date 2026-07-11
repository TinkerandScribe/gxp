# Task brief

**Date:** 2026-07-10
**Task slug:** review-uncommitted-jlens-artifacts
**Workflow:** full

## Goal

Give the operator a per-file disposition recommendation (commit as-is / commit after
scrub-edit / relocate / drop) for every uncommitted change in gxp-public, backed by a leak
sweep and verification evidence, and stop at the approval gate before touching git history.

## Context

- Uncommitted set: `M core/ratings.jsonl`, `?? jlens-research-findings.md`,
  `?? core/tasks/jlens-research-verification.md`,
  `?? core/failures/webfetch-summarizer-invents-plausible-details.md`,
  `?? gxp-release-asset/gxp-skill.zip`
- Rules: `core/rules/01-no-secrets-in-git.md`, `core/rules/02-local-context-never-committed.md`
  (principle: project-/deployment-specific content is local-only regardless of path).
- Repo scrub standard: zero PII, zero insider project references (launch commits 6686878, 7811900).
- Canonical findings copy already committed in the private source repo.
- README §"Use it as a Claude skill" points at a **GitHub Release asset**
  (`releases/latest/download/gxp-skill.zip`), not an in-tree file.
- ratings.jsonl history: schema line invites real runs ("replace them with your own runs");
  08b9110 dogfooded a real line — evidence for the ledger-policy call.

**Strategy/Model:** current Claude Code session; read-only + scratchpad until the approval
gate. No routing.

## Ideal State Criteria

- [x] 1. Every path in `git status --short` has exactly one explicit disposition in the
      final table, with the exact scrub/move spelled out where applicable.
- [x] 2. Leak sweep (`git grep -iE` over tracked files + `rg` with the same pattern over all
      untracked files and the unpacked zip) returns **0 unjustified hits in everything
      proposed for commit**; every hit anywhere is listed and judged in context.
- [x] 3. The pending `core/ratings.jsonl` line parses mechanically as one JSON object with
      the v1.1 schema fields (no array, no trailing junk).
- [x] 4. Every file proposed for commit is pure LF (mechanical byte check, no CR).
- [x] 5. `bash scripts/verify.sh` exits 0 on the working tree as proposed.
- [x] 6. The ratings-ledger contradiction is named with git-history evidence and exactly ONE
      policy (curated-examples-only vs live-for-fork-work) is recommended and applied to the
      pending line's disposition.
- [x] 7. `gxp-skill.zip` is unpacked and its full file list + contents swept for PII/insider
      terms before any recommendation that places it anywhere public.
- [x] 8. Zero git-mutating commands (add/commit/tag/push/release) before Gate 1 approval;
      after approval, local commit only — no tag, no push.

## Out of scope

- Pushing, tagging, or creating releases (separately operator-gated).
- Rewriting already-committed history (e.g. the 08b9110 ratings line).
- Building or rebuilding the skill zip.

## Verification plan

1. Deterministic: leak-sweep commands (2), JSON parse (3), CR-byte scan (4), verify.sh (5),
   zip listing + sha256 vs published release asset (7), shell history shows no mutating git
   commands pre-gate (8).
2. Behavioral: cross-check README release-link expectation vs in-tree zip; cross-check the
   private canonical copy is byte-identical (diff); walk ratings history for the policy
   evidence (6).
3. Subjective: disposition reasoning per file (1), judged hits in context (2).

## Self-evaluation gate

- [x] Completeness — covers all five paths + policy question + verification gates from the operator spec.
- [x] Ambiguity — each criterion is mechanically checkable or has a named judgment step.
- [x] Scope trap — no scrubbing/moving applied before approval; proposed diffs only.
- [x] Verification — every criterion has a concrete check above.
- [x] Approval gates — ONE hard gate: present recommendations, then STOP until operator sign-off.

## Approval gates

- **Gate 1 (hard):** after presenting the per-file table, diffs, policy recommendation, and
  verification evidence — stop. No git mutation until the operator approves.
  **Outcome: held, then approved by the operator ("proceed", 2026-07-10).**

## Dead ends

-

## Handoff notes

- **Dispositions applied:** findings doc dropped (byte-identical canonical copy lives in the
  private source repo; public copy leaked a local user path); jlens task brief + rating line
  relocated to the private repo's GXP layer; failure capture
  `webfetch-summarizer-invents-plausible-details.md` committed after template-conformance
  edits (Task/context header, Repeatable? section, no dangling brief reference);
  `gxp-release-asset/` dropped (sha256-identical to the asset already published on the
  v1.1.1 GitHub release) and the path gitignored.
- **Ledger policy adopted:** live-for-fork-work — a run's rating lives where its artifacts
  live; `core/ratings.jsonl` accepts real runs whose subject is this repo (brief in
  `core/tasks/`), and keeps the labeled example entries.
- **Verified:** leak sweep clean on the committed set; verify.sh exit 0; LF-only; ratings
  lines valid single JSON objects. Push/tag NOT performed (separately gated).
