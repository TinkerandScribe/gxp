# Changelog

All notable changes to the public [GXP](https://github.com/TinkerandScribe/gxp) repo are
documented here. Versioning follows [SemVer](https://semver.org/) for the methodology
package as a whole (core + adapters + install/verify scripts).

## [1.1.0] - 2026-06-25

### Added

- **`adapters/chatgpt/`** — Custom GPT instructions, model routing, context-loading guide,
  `TEST_PROMPT.md`, and `sync/check-core` scripts for chat.openai.com.
- **`core/routing.md`** — policy row for web-based GXP brief/planning (recommend-to-human);
  Custom GPT / web assistant called out under recommend-to-human routes.
- **`core/templates/task-brief.md`** — `chatgpt` in `engine_candidates`.

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

[1.1.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.1.0
[1.0.0]: https://github.com/TinkerandScribe/gxp/releases/tag/v1.0.0