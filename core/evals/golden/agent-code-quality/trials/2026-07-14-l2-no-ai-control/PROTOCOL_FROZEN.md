# PROTOCOL_FROZEN — control without .ai/ vs GXP with .ai/

**Date:** 2026-07-14  
**Task:** 10-circuit-breaker  

## Arms
- `control_no_ai`: best-effort tools; workspace has **no** `.ai/` tree; full task prompt only
- `gxp`: full GXP; workspace **includes** `.ai/` PROGRAM/rules/failures

## Success rule
PASS if mean GXP − mean control ≥ 0.10 OR majority GXP wins; no GXP tamper.

## Isolation
Control cannot Phase-0 from repo memory files (removed). Both arms get task prompt text in tool runner system prompt.
