# CONTAMINATION — 2026-07-14 matched hard Grok+Qwen

## Access

| Actor | Access |
|-------|--------|
| Qwen (Ollama) | Prompt + starter via chat API only; no `hidden_tests/` or `reference/` paths |
| Grok implement path | Prompt + starter; no scorer injection until grade time |
| Scorer | Canonical hidden tests at grade time (Python 3.14) |

## Integrity

- All 12 cells: `no_test_tamper=true`, `scope_ok=true`.
- GXP extras: BRIEF.md / HANDOFF.md / raw_model_output.md only.
- Ollama: `think: false` for reliable `message.content`.

## Notes

- Trial: `trials/2026-07-14-matched-hard-grok-qwen`
- Model: `qwen3.6:27b`
- No tag/release from this campaign
