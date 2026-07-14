# CAMPAIGN_REPORT — 2026-07-14 L2 public-green vs GXP

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Task:** `09-rate-limit-service`  
**Design:** same model + tools; only **verification stop rule** differs  
**Scorer:** Python 3.14 package mode  

## Arms

| Arm | Discipline |
|-----|------------|
| `public_green` | Done when public `tests_public` exits 0 (green trap allowed) |
| `gxp` | Phase 0 + BRIEF + multi-factor criteria beyond public tests |

## Correctness (matched pairs)

| Model | public_green | GXP | Δ | Winner |
|-------|-------------:|----:|---:|--------|
| grok | **0.17** (2/12) | **1.00** (12/12) | **+0.83** | **gxp** |
| qwen | **0.92** (11/12) | **0.92** (11/12) | 0.00 | **tie** |

All: `no_test_tamper=true`, `scope_ok=true`.  
Grok GXP / Qwen GXP process_score = 1.0 where BRIEF present.

## Means

| Arm | Mean correctness |
|-----|-----------------:|
| public_green | **0.542** |
| gxp | **0.958** |

**Gap (GXP − public_green):** **+0.417** (≥ 0.10)

## Wins

| Metric | Value |
|--------|------:|
| GXP wins | **1** |
| public_green wins | **0** |
| Ties | **1** |

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **PASS** (+0.417) |
| Majority GXP wins | **PASS** (1 > 0) |
| No GXP tamper | **PASS** |

### Verdict: **PASS**

**Meaningful GXP win** under this pre-registered design: GXP beats a public-green-stop control on mean hidden correctness by a large margin, driven by Grok fully repairing multi-factor bugs while public_green left the weak-green starter.

## Interpretation (honest)

1. **What we measured:** GXP’s claim that “public tests alone ≠ done” matters when the control arm is instructed (and for Grok, disciplined) to stop at public green.  
2. **Grok row is clean:** public_green ran public verify (exit 0) and **did not edit** service code (starter score 0.17). GXP fixed all multi-factor bugs (1.0).  
3. **Qwen row is noisy:** the model still rewrote `service/*` before a later public-green auto-stop, so both arms reached 0.92 (same remaining invalid-config miss). Auto-stop only enforced after a green `run`, not “never fix beyond public.”  
4. **Not a universal proof** that GXP always beats unconstrained tool agents — only that **verification-discipline GXP beats premature public-green stop** under this protocol.  
5. Prior L2 pilot (unconstrained control vs GXP) had gap 0; **this arm definition is the lever** that produced a PASS.

## Limits

- N=1 task, N=1 seed.  
- Grok session implementer (not blind desktop).  
- Qwen JSON tool loop is minimal.  
- public_green is a strong control for “vibe verify,” not for “best-effort engineer without GXP label.”

## Follow-ups

- Harden public_green enforcement earlier (block writes after first green).  
- Multi-seed + second L2 task for robustness.  
- Optional: unconstrained-control row retained as contrast (expect smaller Δ).
