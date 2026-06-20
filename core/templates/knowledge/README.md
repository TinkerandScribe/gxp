# Local knowledge layout

Project-specific knowledge stays **local-only** (see `core/rules/02-local-context-never-committed.md`).
Copy this layout to `~/.gxp/knowledge/` (preferred) or repo `knowledge/` (gitignored).

```
knowledge/
  machines/     # bed sizes, software, maintenance notes
  materials/    # stock list, thickness limits, supplier refs (no costs in git)
  pricing/      # rate cards — local only, never commit filled files
```

Use `_example.md` files in each subfolder as structure guides. Delete the leading
underscore when you create real files, or add new `.md` files alongside them.

A context loader reads bounded excerpts from the first existing
`knowledge/{machines,materials,pricing}/*.md` under `~/.gxp/knowledge/` or repo `knowledge/`.