# Task brief

**Date:** 2026-07-24
**Task slug:** cowork-plugin-version-track-package
**Workflow:** lightweight (phases 1, 2, 3, 5 + ratings append)

## Goal

`adapters/cowork/plugin-src/.claude-plugin/plugin.json` declares version `1.3.1`, matching
the current package tag, so an installed Cowork plugin can be compared against a release by
version string instead of by content hash.

## Context

- Related files: `adapters/cowork/plugin-src/.claude-plugin/plugin.json` (only file changed)
- Background: the manifest has read `0.1.0` since the adapter was introduced, across every
  release through `v1.3.1`. A staleness check therefore cannot use the version field — it
  requires unzipping the installed `.plugin` and hashing 15 files against a fresh build.
  This was hit in practice: an installed copy was 12/15 files behind and the version string
  reported no difference.
- `CHANGELOG.md` states SemVer covers "the methodology package as a whole (core + adapters +
  install/verify scripts)", so the adapter tracking the package version is the documented
  intent, not a new policy.
- **Non-issue, investigated and dismissed:** `adapters/cowork/dist/gxp.plugin` was initially
  suspected of being a stale checked-in artifact. `.gitignore:24` ignores
  `adapters/cowork/dist/` and `git ls-files` confirms it is untracked. It is a local build
  output, correctly excluded. No change needed.
- Relevant `core/rules/` entries: `02-local-context-never-committed.md` — `dist/`,
  `_grok_fill/`, `gxp-release-asset/`, `.ai/tmp/` stay untracked; diff must not add them.
- Relevant `core/failures/` entries:
  - `jsonl-append-via-shell-heredoc-corrupts-escapes.md` — the `core/ratings.jsonl` append
    must go through Python, never a shell heredoc.
  - `verification-wrapper-swallows-exit-codes.md` — check `scripts/verify.sh` exit status
    directly; do not infer pass from stdout text.

**Strategy/Model:** current session model (Claude, Cowork) — a one-line JSON edit plus two
existing verify scripts; the binding constraint is honoring the ratings hash-chain and exit-code
discipline, not reasoning difficulty. No stronger engine would clear these criteria by a wider
margin.

## Routing

Not applicable — local repo edit, public methodology repo, no external dispatch.

## Ideal State Criteria

- [ ] 1. `adapters/cowork/plugin-src/.claude-plugin/plugin.json` has `"version": "1.3.1"`.
- [ ] 2. That file still parses as JSON: `python3 -c "import json;json.load(open(...))"` exits 0.
- [ ] 3. `bash adapters/cowork/sync/check-core.sh` exits 0.
- [ ] 4. `bash scripts/verify.sh` exits 0 (exit code read directly, not inferred from output).
- [ ] 5. `git diff --stat 6c26071 -- adapters/ core/workflow.md core/rules/` shows exactly 1
  file changed, 1 insertion, 1 deletion (the manifest). The only other paths added by this
  run are `core/tasks/cowork-plugin-version-track-package.md` (this brief) and one appended
  line in `core/ratings.jsonl` — both GXP bookkeeping, neither a methodology or adapter edit.
- [ ] 6. A freshly built `.plugin` contains the same 15 file paths as the pre-change build,
  and `plugin.json` is the only member whose content hash changed.
- [ ] 7. One JSON object is appended to `core/ratings.jsonl` chaining from `prev_hash`
  `5a2e1fef…`, and `python3 scripts/validate-ratings-chain.py core/ratings.jsonl` exits 0.
- [ ] 8. The change is committed to local `main`; `git status --porcelain` is empty
  afterwards; nothing is pushed.

## Out of scope

- Adding a `CHANGELOG.md` entry. `1.3.1` is already tagged and shipped; editing a released
  section to describe a retroactive alignment would misrepresent what that release contained.
  Parked as a follow-up for the next version's notes.
- Adding a CI guard that asserts `plugin.json` version equals the current git tag. Real
  improvement, but it is new tooling, not this fix.
- Rebuilding or deleting the local `adapters/cowork/dist/gxp.plugin`. Gitignored, user-local.
- The stray root directory literally named `\C:\Users\...\.ai\tmp\gxp-blind` (a Windows path
  bug artifact). Untracked and invisible to `git status`; flagged, not touched.
- Bumping any other adapter's version or introducing version fields where none exist.
- Pushing, tagging, or cutting a release.

## Verification plan

Deterministic, in order:

1. Criterion 1 — `grep '"version"' plugin.json`.
2. Criterion 2 — `python3 -c "import json,sys;json.load(open(sys.argv[1]))"`, read `$?`.
3. Criterion 3 — `bash adapters/cowork/sync/check-core.sh; echo $?`.
4. Criterion 4 — `bash scripts/verify.sh; echo $?` — capture the code in a variable before
   any pipe, per `verification-wrapper-swallows-exit-codes.md`.
5. Criterion 5 — `git diff --stat 6c26071 -- adapters/ core/workflow.md core/rules/`, then
   `git show --stat HEAD` to confirm the commit contains only the manifest, this brief, and
   the ratings line.
6. Criterion 6 — build into a throwaway tree, hash all zip members, diff the hash map against
   the pre-change build captured earlier this session.
7. Criterion 7 — `python3 scripts/validate-ratings-chain.py core/ratings.jsonl; echo $?`.
8. Criterion 8 — `git log --oneline -1` and `git status --porcelain` (must be empty);
   `git log origin/main..main` shows the commit is local only.

No behavioral or subjective checks — a version string has no runtime behavior in this repo.

## Self-evaluation gate

- [x] **Completeness** — the real goal is "make staleness detectable by version"; criterion 6
  guards the thing that actually matters (no collateral content change), which a bare "the
  field says 1.3.1" check would miss.
- [x] **Ambiguity** — all eight are exit codes, exact strings, or file counts.
- [x] **Scope trap** — CHANGELOG entry and CI guard both explicitly parked, not smuggled in.
- [x] **Verification** — every criterion has a command. None require judgment.
- [x] **Approval gates** — version target and commit-to-main both approved by the operator
  before Phase 3 (see below).

## Approval gates

- Version target `1.3.1` (vs. leaving `0.1.0` or an independent `0.2.0`) — **approved by
  operator, 2026-07-24**, on the basis that CHANGELOG already scopes SemVer to the whole
  package including adapters.
- Commit directly to local `main` rather than a branch — **approved by operator, 2026-07-24**.
  Not pushed.

## Dead ends

- **Stale `.git/index.lock` blocked the commit (resolved, not abandoned).** First `git commit`
  died with `Unable to create '.git/index.lock': File exists`. Not retried blindly. Inspection
  showed a 0-byte lock timestamped 20:39:22 — the exact moment of this session's first
  `git status -sb`, which had also emitted `warning: unable to unlink .git/index.lock:
  Operation not permitted`. Root cause: the Cowork folder mount denies `unlink` by default, so
  any git command that takes the index lock leaves it stranded and wedges every later write.
  Resolved by granting delete permission for the folder, then `rm -f .git/index.lock`.
  Belief now: on a Cowork-mounted repo, enable file deletion *before* the first git command
  that writes, not after one fails.

## Handoff notes

- **What changed:** one line — `adapters/cowork/plugin-src/.claude-plugin/plugin.json`
  `version` `0.1.0` → `1.3.1`. Plus GXP bookkeeping: this brief, one `core/ratings.jsonl`
  line. Committed as `60c3b1b` on local `main`, not pushed.
- **What was verified (and how):** all deterministic. C1 grep; C2 `json.load` exit 0;
  C3 `adapters/cowork/sync/check-core.sh` exit 0; C4 `scripts/verify.sh` exit 0 (code captured
  in a variable before any pipe, per `verification-wrapper-swallows-exit-codes.md`);
  C5 scoped `git diff --stat` = 1 file / 1 insertion / 1 deletion; C6 rebuilt the `.plugin`
  and hashed all members — 15/15 paths stable, `plugin.json` the only changed member;
  C7 `validate-ratings-chain.py` exit 0, 15 chained entries; C8 `git status --porcelain`
  empty, commit local-only. **8/8 met.** No behavioral or subjective checks — a version
  string has no runtime behavior in this repo.
- **Explicitly not done / parked / follow-ups:**
  1. CI guard asserting manifest version == current git tag. Recommended; it would have
     caught this drift at release time instead of by hand.
  2. CHANGELOG entry — belongs in the next version's notes, not retroactively inside the
     already-shipped `1.3.1` section.
  3. Proposed `core/failures/` entry for the Cowork-mount unlink issue (drafted in Dead ends
     above, **not** written as a file — adding one was outside this brief's scope).
  4. Stray untracked root directory literally named `\C:\Users\...\.ai\tmp\gxp-blind`
     (Windows path-bug artifact). Invisible to `git status`, harmless, left alone.
- **Approval gates hit and outcomes:** version target `1.3.1` — approved. Commit to local
  `main` — approved. Both cleared before Phase 3; no new gate hit mid-implementation.
- **New `failures/` entries or rules:** none written. One candidate proposed (item 3 above).
- **Rating entry reference:** `core/ratings.jsonl`, last line, `entry_hash`
  `a9bdf75894c83787894ddb09a8529743e8a935e1a896786bd74ed6e145d6e953`, rating **7/10**.
  Held below 8 deliberately: half the originally stated scope was a false diagnosis (a
  gitignored build artifact called a stale checked-in file, because tracked-ness was never
  checked), and Phase 2 had to reject a non-binary criterion I had written myself.
