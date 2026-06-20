# Cowork Adapter

Packages GXP as a **Cowork plugin** — a `.plugin` zip the operator installs into Anthropic's Cowork desktop app to get four GXP skills available across all Cowork sessions.

## Skills shipped

| Skill                  | Purpose                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `gxp-workflow`         | Full Phases 0–8 loop on a non-trivial task.                                              |
| `gxp-brief`            | Draft a brief (Phase 1) only — never implement. Asks clarifying questions if needed.     |
| `gxp-rate`             | Append one honest line to `ratings.jsonl` (Phase 6). Refuses flat-8 stamping.            |
| `gxp-failure-capture`  | Write a `failures/` entry (Phase 7) with expected/actual/root/detection/resolution/prev. |

## Source-of-truth model: option (a) — references generated at build time

The adapter checks in only the **unique** content:

```
adapters/cowork/
├── plugin-src/
│   ├── .claude-plugin/plugin.json     # manifest
│   ├── README.md                       # ships inside the .plugin
│   └── skills/
│       ├── gxp-workflow/
│       │   ├── SKILL.md                # adapter-authored
│       │   └── references/             # adapter-authored references only
│       │       ├── ratings-schema.md
│       │       └── rules-summary.md
│       ├── gxp-brief/SKILL.md
│       ├── gxp-rate/SKILL.md
│       └── gxp-failure-capture/SKILL.md
├── build.sh / build.ps1                # assembles dist/gxp.plugin from plugin-src + core/
└── sync/check-core.sh                  # drift check (frontmatter shape + core file presence)
```

At build time the script copies `core/workflow.md`, `core/templates/task-brief.md`, `core/templates/failure-capture.md`, and the two binding rules into the appropriate `references/` folders, then zips the result. **`core/` is the single source of truth.** No `references/workflow.md` or template copies live in git under `plugin-src/`.

The generated `dist/` is gitignored.

## Build

From the repo root:

```bash
bash adapters/cowork/build.sh
```

or on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File adapters/cowork/build.ps1
```

Output: `adapters/cowork/dist/gxp.plugin` — a ~30 KB ZIP ready to install.

## Install

In Cowork, install the produced `.plugin` via Settings → Capabilities → Install Plugin → select `adapters/cowork/dist/gxp.plugin`.

The four skills auto-trigger on relevant phrases (see each SKILL.md for trigger phrases).

## Drift check

```bash
bash adapters/cowork/sync/check-core.sh
```

Validates that:

- Each SKILL.md has well-formed YAML frontmatter.
- Each skill's `name` field matches its directory name.
- No `description` field contains `<...>` XML-tag patterns (Cowork's validator rejects these).
- The `core/` files the build script depends on still exist.

Drift in `references/workflow.md` or the templates is impossible under option (a) — they don't live in git.

## Update procedure

1. Change canonical content in `core/` (e.g. edit `core/workflow.md`).
2. Re-run `bash adapters/cowork/build.sh`.
3. Re-install the new `dist/gxp.plugin` in Cowork.

If a SKILL.md needs an update (different trigger phrases, new instructions), edit `plugin-src/skills/<skill>/SKILL.md` directly — those are adapter-authored.
