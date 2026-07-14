# CAMPAIGN_REPORT — 2026-07-14 L2 hardened public_green + multi-seed GXP

**Protocol:** [`PROTOCOL_FROZEN.md`](PROTOCOL_FROZEN.md)  
**Task:** `09-rate-limit-service`  
**Scorer:** Python 3.14 package mode  

## Design (hardened)

| Arm | Enforcement |
|-----|-------------|
| `public_green` | **Preflight** public unittest; if green → **zero writes** (runner blocks further product edits) |
| `gxp` | Full tool loop + BRIEF; Qwen **3 independent seeds** (s1–s3) |

This closes the honesty gap from the prior PASS where Qwen public_green still rewrote `service/*` before auto-stop.

## Correctness

| Model | Arm | Correctness | Notes |
|-------|-----|------------:|-------|
| grok | public_green | **0.17** (2/12) | no service edits |
| grok | gxp | **1.00** (12/12) | full multi-factor fix |
| qwen | public_green | **0.17** (2/12) | preflight auto-done |
| qwen | gxp s1 | **0.92** (11/12) | miss invalid-config only |
| qwen | gxp s2 | **0.92** (11/12) | same |
| qwen | gxp s3 | **0.92** (11/12) | same |

All cells: `scope_ok=true`, `no_test_tamper=true`.

### Matched pairs (public_green baseline per model)

| Pair | public_green | GXP | Δ | Winner |
|------|-------------:|----:|---:|--------|
| grok | 0.17 | 1.00 | **+0.83** | **gxp** |
| qwen × s1 | 0.17 | 0.92 | **+0.75** | **gxp** |
| qwen × s2 | 0.17 | 0.92 | **+0.75** | **gxp** |
| qwen × s3 | 0.17 | 0.92 | **+0.75** | **gxp** |

## Means

| Pool | Mean correctness |
|------|-----------------:|
| public_green (n=2) | **0.167** |
| gxp (n=4: grok + 3 qwen seeds) | **0.938** |

**Gap (GXP − public_green):** **+0.771**

## Wins

| Metric | Value |
|--------|------:|
| GXP wins | **4** |
| public_green wins | **0** |
| Ties | **0** |

## Pre-registered rule

| Clause | Result |
|--------|--------|
| Gap ≥ 0.10 | **PASS** (+0.771) |
| Majority GXP wins | **PASS** (4–0) |
| No GXP tamper | **PASS** |

### Verdict: **PASS**

**Robust meaningful GXP win** under hardened public-green control: both models’ public_green stay at starter hidden score (**0.17**); GXP lifts Grok to **1.0** and Qwen seeds stably to **0.92**.

## Interpretation

1. **Hardened enforcement works** — Qwen public_green no longer “cheats” by rewriting before stop.  
2. **Multi-seed Qwen GXP is stable** — three runs all **0.92** (same remaining fail: invalid config body).  
3. **Claim scope remains** “GXP beats premature public-green stop,” not “beats unconstrained best-effort.”  
4. Residual Qwen miss (invalid config fail-closed) is a good next single-shot trap for GXP criteria quality.

## Limits

- One task.  
- Grok GXP is session implementer.  
- Qwen GXP often hit max steps; still wrote service/* before timeout.  
- Unconstrained control contrast not re-run here.

## Follow-ups

- Second L2 task for multi-task majority.  
- Optional unconstrained-control contrast row.  
- Stronger invalid-config coverage in agent-visible docs/tests.
