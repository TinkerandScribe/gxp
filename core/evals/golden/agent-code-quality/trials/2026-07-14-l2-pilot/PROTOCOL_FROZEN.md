# PROTOCOL_FROZEN — L2 tool-using pilot 09-rate-limit-service

**Date:** 2026-07-14  
**Task:** 09-rate-limit-service  
**Cells:** 4 (grok,qwen × control,gxp) — matched model within row  

**Models:**  
- `grok` — session tool-using implementer  
- `qwen` — Ollama qwen3.6:27b with minimal tool loop (read/write/run), think=false  

**Arms:**  
- control: prompts/control-tools.md (no formal GXP)  
- gxp: prompts/gxp-tools.md (Phase 0 + BRIEF + verify + HANDOFF)  

## Success rule
PASS if (mean GXP − mean control correctness ≥ 0.10) OR (GXP wins majority of
matched task comparisons), AND no GXP no_test_tamper=false.

## Isolation
Implement path must not read tasks/.../hidden_tests or reference/.
Public tests_public/ and .ai/ are in-workspace and allowed.
