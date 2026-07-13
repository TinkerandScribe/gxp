# Changelog

All notable changes to the public [GXP](https://github.com/TinkerandScribe/gxp) repo are
documented here. Versioning follows [SemVer](https://semver.org/) for the methodology
package as a whole (core + adapters + install/verify scripts).

## [Unreleased]

### Changed

- **Doc dedup (P2-4 hybrid)** — `claude` / `chatgpt` / `grok` / `perplexity`
  `instructions/workflow.md` are generated from `core/workflow.md` +
  `adapters/<tool>/ai-workflow/deltas/workflow.delta.md` via
  `scripts/generate-adapter-workflows.py` (`--check` in CI). Cursor `rule.mdc` and
  Cowork build-time core copy unchanged. Edit core + deltas only; do not hand-edit
  generated workflow bodies.

## [1.2.0] - 2026-07-13

### Added

- **CI** — `.github/workflows/verify.yml` (ubuntu + windows, `fetch-depth: 0`,
  `verify.sh`, Windows PowerShell 5.1 sync checks, cowork build on Linux, negative
  structural-drift test, main-branch marker auto-bump).
- **Live sync markers** — real core tip SHA in claude/chatgpt/grok/perplexity
  workflows; bold-tolerant regex; hard-fail past threshold (default 3); shallow WARN;
  `scripts/update-sync-markers.sh`.
- **Installer `--dry-run` / `-DryRun`** and subshell counter fix (process substitution)
  in `install-ai-from-core.sh`.
- **Eval regression fixture** —
  `core/evals/regressions/verification-wrapper-must-fail-on-drift.md`.
- **Optional ratings hash-chain** schema fields + `scripts/validate-ratings-chain.py`.
- **Routing critic descope** — independent review recommended, not a shipped subsystem.
- **Structural floor (P0-2)** — claude/chatgpt/grok checks enforce Phases 0–8, 4–8
  criteria, anti-loop, deterministic-first verification, and ratings fields.

### Fixed

- Whole-file `workflow.md` allowlisting no longer masks drift; present-file content
  is not allowlist-exempt; allowlist readers strip CR for WSL/Windows.

### Changed

- **chatgpt** workflow header `v1.0` → `v1.1`; **chatgpt/claude** gain Phase 8
  (Handoff) and explicit ratings field list; **grok** Phase 1 states 4–8 criteria
  and Phase 6 lists ratings fields.
- README install examples prefer dry-run / non-force defaults.

## [1.1.3] - 2026-07-13

### Fixed

- **Grok `check-core.sh` def-order** — the "Last synced from core" NOTE used `log` /
  `$YELLOW` before those helpers were defined, so a regex-matching real SHA crashed under
  `set -u`. The NOTE now runs after helpers are defined (behaviorally verified).

### Added

- **GxP naming disclaimer** in `README.md` — Guided eXecution Protocol is unrelated to
  regulated-industry GxP (GMP/GLP/GCP).
- **`ROADMAP.md`** — verification-hardening sequence from the 2026-07 external audit
  review: corrected order P0-2 → P0-1 → P0-3, three interaction corrections with evidence,
  P1/P2 dispositions, and deliberately-not-adopted items.
- **P0 draft briefs** — `core/tasks/real-diff-sync-checks.md`,
  `core/tasks/ci-verify-workflow.md`, `core/tasks/staleness-marker-real-sha.md` (binary
  criteria, out-of-scope, verification plan, explicit Depends-on). The staleness brief
  records a post-audit defect: the marker regex requires `core: <hex>` but the bold
  marker format renders `core:** <hex>`, so even a real SHA never matches.
- **`core/failures/jsonl-append-via-shell-heredoc-corrupts-escapes.md`** — shell heredoc
  `\$` lands as an invalid JSON escape in `ratings.jsonl`.
- Review/task briefs for the audit review and this unblocker run under `core/tasks/`.

## [1.1.2] - 2026-07-11

### Changed

- **Ratings ledger policy (live-for-fork-work)** — `core/ratings.jsonl` is a **live** ledger
  for runs whose subject is this repo (brief under `core/tasks/`), while keeping the labeled
  example entries. A run’s rating lives where its artifacts live: rate work done in an
  installed project’s `.ai/ratings.jsonl`, not here. Clarified in Phase 6 of
  `core/workflow.md`. This resolves the earlier ambiguity between “examples only” and the
  real dogfood line added in 1.1.1.

### Added

- **`core/failures/webfetch-summarizer-invents-plausible-details.md`** — research-task trap:
  broad web-fetch summaries can invent plausible specifics (model names, versions, numbers);
  never promote a broad-summary fact to confirmed without a verbatim quote or a second
  independent source. Prefer on-disk clones for citable claims.
- **`.gitignore`** — `/gxp-release-asset/` so the Claude skill zip stays a GitHub Release
  asset only (as the README already documents), never an in-tree binary.

## [1.1.1] - 2026-07-02

### Fixed

- **`scripts/verify.sh`** — no longer swallows adapter sync-check failures (drift now
  fails the build), and now runs `adapters/cowork/sync/check-core.sh`, which its old
  glob silently skipped.
- **Adapter sync checks** — all six now pass honestly on a clean checkout on both bash
  and PowerShell: claude ships the `drift-allowlist.txt` its docs prescribe; grok's
  allowlist matches file paths as documented (not just labels); cursor's `check-core.sh`
  uses the same structural markers as its `.ps1` instead of an always-failing
  byte-compare; the claude/chatgpt/grok `check-core.ps1` copy-install guard runs after
  repo-root resolution (it previously made them silent no-ops on Windows); cowork's
  check reports a missing `python3` as a skip instead of "invalid JSON".
- **`scripts/install-ai-from-core.ps1`** — `-IncludeCursorRule` now actually installs
  the rule into the target repo (named-parameter invocation instead of a broken splat).
- **`adapters/grok/ai-workflow/gxp.ps1`** — removed a self-referential alias that broke
  every `gxp` invocation; UTF-8 BOM added (also to grok's `check-core.ps1`, whose
  BOM-less non-ASCII strings misparsed under Windows PowerShell 5.1 — hangs and
  skipped checks).
- **Cowork plugin sources** — completed a truncated `gxp-failure-capture/SKILL.md` and
  fixed a dangling reference in `gxp-brief/SKILL.md`.
- **Perplexity adapter** — Phase 6 now uses the core ratings schema (`ts`,
  `criteria_met`/`criteria_total`, integer `rating` 1–10) instead of the legacy
  `timestamp`/1–5 form.

### Added

- **`core/failures/verification-wrapper-swallows-exit-codes.md`** — failure capture for
  the silent-no-op patterns fixed above (dogfooding; task brief in `core/tasks/`).

## [1.1.0] - 2026-06-25

### Added

- **`adapters/chatgpt/`** — Custom GPT instructions, model routing, context-loading guide,
  `TEST_PROMPT.md`, and `sync/check-core` scripts for chat.openai.com.
- **`core/routing.md`** — policy row for web-based GXP brief/planning (recommend-to-human);
  Custom GPT / web assistant called out under recommend-to-human routes.
- **`core/templates/task-brief.md`** — `chatgpt` in `engine_candidates`.
- **Downloadable Claude skill** — `gxp-skill.zip` attached to the release; installs via
  claude.ai (Settings → Capabilities → Skills → Upload) or Claude Code (`~/.claude/skills/`).
  Self-contained: the full workflow plus bundled brief/failure templates, ratings schema, and rules.

### Changed

- **`scripts/verify.sh`** — requires ChatGPT adapter files.
- **`README.md`**, **`CONTRIBUTING.md`**, **`adapters/README.md`** — document the ChatGPT adapter.
- **`adapters/claude/.../model-routing.md`** — ChatGPT listed as a sibling handoff target.

## [1.0.0] - 2026-06-20

### Added

- First public release of **GXP (Guided eXecution Protocol)** — verification-first,
  binary-criteria workflow for bounded AI agents.
- Core methodology (`workflow.md`, routing policy, rules, failures, templates).
- Adapters for Cursor, Grok, Claude, Perplexity, and Cowork.
- Cross-platform installer (`.ps1` + `.sh`) and adapter-parity check (`verify.sh`).
- MIT license, `CODE_OF_CONDUCT`, and `SECURITY` policy.

[1.2.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.2.0
[1.1.3]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.3
[1.1.2]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.2
[1.1.1]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.1
[1.1.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.0
[1.0.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.0.0
