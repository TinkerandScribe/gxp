# PROTOCOL_FROZEN — L2 hardened public_green + multi-seed GXP

**Date:** 2026-07-14  
**Task:** 09-rate-limit-service  

## Arms
- `public_green`: preflight public verify; if green, zero writes (enforced in runner)
- `gxp`: full GXP tool loop; Qwen multi-seed s1–s3 independent runs

## Success rule
PASS if mean(GXP) − mean(public_green) ≥ 0.10 OR GXP wins majority of matched
comparisons (for multi-seed: each seed paired with same-model public_green baseline),
AND no GXP tamper.

## Matched comparisons
- grok: public_green vs gxp
- qwen: public_green vs each of s1,s2,s3 (3 pairs) — or report mean GXP vs pg
