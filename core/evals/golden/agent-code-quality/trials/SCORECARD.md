# GXP code-quality eval scorecard (2026-07-14)

Primary metric remains **hidden correctness**. Secondary: process / transcript.

## Campaigns

| Campaign | Design | Mean gap (GXP − control) | Verdict |
|----------|--------|--------------------------:|---------|
| Easy 01/04/05 matched | single-shot | ~0 (ceiling) | **FAIL** |
| Hard 06–08 matched | single-shot | ~0 / slight negative | **FAIL** |
| L2 pilot 09 unconstrained | tools both arms | 0 | **FAIL** |
| L2 public_green vs GXP 09 | stop at public green | **+0.42** | **PASS** |
| L2 hardened multi-seed 09 | zero-write public_green | **+0.77** | **PASS** |
| L2 task 10 public_green vs GXP | second fixture | **+0.68** | **PASS** |
| L2 unconstrained contrast 10 | best-effort control | **0** | **FAIL** |
| L2 control without `.ai/` | Phase-0 isolation | **0** | **FAIL** |

## Claim policy (honest)

**Supported:** GXP (verification beyond weak public green) beats **premature public-green stop** on multi-factor tool-using tasks 09–10.

**Not supported (yet):** GXP beats unconstrained best-effort tool agents when they can read the same prompt (and, if present, `.ai/`).

## Transcript metrics

See [`TRANSCRIPT_METRICS.md`](TRANSCRIPT_METRICS.md). BRIEF rates higher on GXP; phase0 alone does not create hidden Δ when `.ai/` is mounted for control.
