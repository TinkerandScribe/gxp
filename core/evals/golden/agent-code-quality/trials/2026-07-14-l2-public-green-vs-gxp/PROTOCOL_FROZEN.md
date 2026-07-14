# PROTOCOL_FROZEN — L2 public-green control vs GXP

**Date:** 2026-07-14  
**Task:** 09-rate-limit-service  
**Cells:** 4 (grok,qwen × public_green,gxp)

## Arms (pre-registered)

| Arm | Prompt discipline |
|-----|-------------------|
| `public_green` | Stop when public `tests_public` exits 0; do not chase hidden edges |
| `gxp` | Full GXP: Phase 0, BRIEF, criteria beyond public tests, HANDOFF |

Same model + tools within each row. Difference is **verification stop rule** only.

## Success rule
PASS if (mean GXP − mean public_green correctness ≥ 0.10) OR (GXP wins majority
of matched pairs), AND no GXP `no_test_tamper=false`.

## Isolation
No hidden_tests/reference at implement time.
