# PROTOCOL_FROZEN — matched Grok + local Qwen

**Date:** 2026-07-14  
**Models (matched within model):**  
- `qwen` — Ollama `qwen3.6:27b`  
- `grok` — session implement / subagent (same process both arms)  

**Tasks:** 04-safe-join, 05-count-words, 01-parse-kv  
**Cells:** 12 (2 models × 2 arms × 3 tasks)

## Success rule
PASS if (mean GXP − mean control correctness ≥ 0.10) OR (GXP wins majority of
matched task comparisons), AND no GXP `no_test_tamper=false`.

## Isolation
Implement path must not read `hidden_tests/` or `reference/`.

## Qwen runner note
Ollama `qwen3.6:27b` defaults to thinking mode. Campaign cells that need
reliable `message.content` must call chat with **`think: false`** (or extract
code from `message.thinking` if content is empty). Documented after empty-content
failures when thinking exhausted `num_predict`.
