# Transcript metrics — L2 tool loops (2026-07-14)

**Scorer:** [`harness/score_transcript.py`](../harness/score_transcript.py)  
**Data:** [`TRANSCRIPT_METRICS.json`](TRANSCRIPT_METRICS.json) (all `agent_tool_log.jsonl` under `trials/`)

## Metrics (secondary; never override hidden correctness)

| Metric | Meaning |
|--------|---------|
| `phase0_hit` | Read under `.ai/` before first `service/` write |
| `tool_verify_ran` | Ran public unittest / preflight public verify |
| `brief_written` | Wrote `BRIEF.md` |
| `handoff_written` | Wrote `HANDOFF.md` |
| `service_writes` | Count of writes under `service/` |

## Snapshot (n=12 Qwen tool-loop cells)

| Metric | Rate |
|--------|-----:|
| phase0_hit | **10/12** |
| tool_verify_ran | **11/12** |
| brief_written | **7/12** (mostly GXP arms) |

### By arm (approximate)

| Arm | phase0 | verify | brief | Notes |
|-----|--------|--------|-------|-------|
| `gxp` | high | high | high | Reads `.ai/` then edits; often BRIEF |
| `control` | high* | high | low | *Also reads `.ai/` when mounted in workspace |
| `public_green` (hardened) | n/a preflight | yes | no | Zero service writes when public green |

\* Unconstrained control still has `.ai/` available — so phase0_hit does **not** isolate GXP; only BRIEF/HANDOFF and stop rules do.

## Findings tied to correctness campaigns

1. **public_green PASS** correlates with **low service_writes** (0 on hardened preflight), not with missing verify.  
2. **Unconstrained FAIL (gap 0)** shows control also hits phase0+verify when `.ai/` is present — process metrics alone do not buy hidden Δ.  
3. GXP uniquely raises **brief_written** / **handoff_written** rates.  
4. Hidden correctness remains primary; transcript metrics explain *behavior*, not replace scores.

## Usage

```bash
python core/evals/golden/agent-code-quality/harness/score_transcript.py --scan-trials \
  --out core/evals/golden/agent-code-quality/trials/TRANSCRIPT_METRICS.json
```

## Success rule note

Transcript metrics are **not** part of the pre-registered correctness PASS rule.
They support honest interpretation of GXP process adherence.
