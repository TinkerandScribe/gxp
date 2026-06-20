# Default rules (binding)

GXP repos enforce a small set of binding rules. The two canonical ones ship with this plugin and are reproduced in full as `rule-01-no-secrets-in-git.md` and `rule-02-local-context-never-committed.md` in this references folder.

## 01 — No secrets in git

Never commit credentials, API keys, tokens, private keys, OAuth secrets, database passwords, or session cookies. This includes `.env`, configuration with secrets inlined, test fixtures with real values, and any file that looks like it might contain one.

If you see a secret in a diff you're about to commit — stop. Rotate it. Then continue.

## 02 — Local context never committed

Personal working memory (`CLAUDE.md` in a personal repo, scratch notes, local caches, anything machine-specific) does not get committed to a shared repo. It either lives outside the repo or in `.gitignore`.

The rationale is that shared repos must remain portable to other contributors and to CI; local state is by definition not portable.

## Adding your own rules

Drop a numbered markdown file in `rules/` (or `core/rules/` in a gxp repo). Conventions:

- Number prefix for ordering (`03-...md`).
- Title line is the rule in one sentence.
- Body explains the rationale and any exceptions.
- Cross-reference from `rules/README.md` so a Phase 0 audit finds it.

Rules should be **narrow, actionable, and justified.** A rule that doesn't pay rent in real decisions is noise — prune it at the weekly refine.
