# Changelog

All notable changes to the public [GXP](https://github.com/TinkerandScribe/gxp) repo are
documented here. Versioning follows [SemVer](https://semver.org/) for the methodology
package as a whole (core + adapters + install/verify scripts).

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

[1.1.1]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.1
[1.1.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.0
[1.0.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.0.0