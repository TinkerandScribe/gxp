# CONTAMINATION — 2026-07-14 L2 pilot

## Access

| Actor | Access |
|-------|--------|
| Grok implement | Workspace starter only; no `tasks/.../hidden_tests` or `reference` |
| Qwen tool loop | Same workspace; tools list/read/write/run only inside workspace |
| Scorer | Canonical hidden tests at grade time |

## Integrity

- All cells `no_test_tamper=true` after rescoring.  
- Scope allowlist updated for agent telemetry files (not product creep).  
- No release tag.
