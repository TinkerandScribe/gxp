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
| L2 short prompt + Phase 0 | underspec prompt both; `.ai/` available | **+0.14** | **PASS** |
| L2 short prompt + control no `.ai/` | underspec + strip control memory | **+0.14** | **PASS** |

## Claim policy (honest)

**Supported:**
1. GXP beats **premature public-green stop** on multi-factor tool-using tasks 09–10.  
2. Under **underspecified user prompts**, GXP Phase 0 (mine `.ai/`) can raise hidden correctness vs incomplete control (shown on Grok for task 10; Qwen tied).

**Not supported:** GXP beats unconstrained best-effort agents given the **same complete prompt** (with or without `.ai/` mounted).

## Transcript metrics

Re-scan locally (output under gitignored `trials/`):

```bash
python core/evals/golden/agent-code-quality/harness/score_transcript.py --scan-trials \
  --out core/evals/golden/agent-code-quality/trials/TRANSCRIPT_METRICS.json
```

BRIEF rates tend to be higher on GXP; phase0 alone does not create a hidden-correctness
gap when `.ai/` is mounted for control.

## Goal status

**Meaningful GXP wins: YES** — see [`GXP_WINS.md`](GXP_WINS.md).  
Recurring iterate-until-win loops should stop or retarget; do not re-run public_green for another PASS.
