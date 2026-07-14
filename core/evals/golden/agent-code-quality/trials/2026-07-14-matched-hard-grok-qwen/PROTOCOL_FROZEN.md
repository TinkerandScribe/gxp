# PROTOCOL_FROZEN — matched Grok + local Qwen (hard pack (ceiling-break))

**Date:** 2026-07-14  
**Trial dir:** `2026-07-14-matched-hard-grok-qwen`  
**Models (matched within model):**  
- `qwen` — Ollama `qwen3.6:27b` (`think: false`)  
- `grok` — session implement / subagent (same process both arms)  

**Tasks:** 06-lru-ttl, 07-deep-merge, 08-line-chunker  
**Cells:** 12 (2 models × 2 arms × 3 tasks)

## Success rule
PASS if (mean GXP − mean control correctness ≥ 0.10) OR (GXP wins majority of
matched task comparisons), AND no GXP `no_test_tamper=false`.

## Isolation
Implement path must not read `hidden_tests/` or `reference/`.

## Qwen runner
Ollama chat with **`think: false`** (thinking can empty `message.content`).
