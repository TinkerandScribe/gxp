# CONTAMINATION — 2026-07-14 matched Grok+Qwen

## Access

| Actor | Access |
|-------|--------|
| Qwen (Ollama `qwen3.6:27b`) | Prompt + starter text only via chat API; no filesystem access to `hidden_tests/` or `reference/` |
| Grok implement path | Session-constrained fills; `_grok_fill/` used for impl; GXP BRIEF/HANDOFF added without reading hidden tests at implement time |
| Scorer | Canonical `hidden_tests/` at grade time only (Python 3.14) |

## Integrity checks

- All 12 cells: `no_test_tamper=true`, `scope_ok=true`.
- GXP extra files limited to BRIEF.md / HANDOFF.md / raw_model_output.md (scorer allows process extras).
- No hidden test trees copied into result dirs.

## Operational notes

- Ollama model: `qwen3.6:27b` Q4_K_M; VRAM load confirmed via `/api/ps`.
- Empty-content failures when thinking mode exhausted `num_predict`; remediating reruns used `think: false`.
- Scorer: `C:\Python314\python.exe`.
- No release tag created for this campaign.
