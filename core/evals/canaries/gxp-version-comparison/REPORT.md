# REPORT — Did v1.2.0 GXP improve outputs?

**Date:** 2026-07-13  
**Before:** `v1.1.3` (`cf05abb`)  
**After:** `HEAD` (v1.2.0 line + marker refresh + CI green note)  
**Method:** process-guarantee scorecard + two fixed canaries (brief + handoff)

## Verdict

### **Improved — primarily process enforcement & handoff completeness**

| Question | Answer |
|---|---|
| Are silent failure modes harder to ship? | **Yes** — induced structural drift fails checks after; silent after whole-file allowlist before |
| Are agent-facing required artifacts more complete by default? | **Yes** — Phase 8 + ratings field names + structural verify language |
| Did we prove better *code quality* on open-ended tasks? | **No** — not measured; same-model canaries only score completeness/adherence |

## Layer A — Process guarantees (primary)

Source: [`process-guarantees.md`](process-guarantees.md) from
`bash scripts/eval-gxp-process-guarantees.sh v1.1.3 HEAD`.

| Side | Score |
|---|---|
| Before (v1.1.3) | **2 / 11** |
| After (HEAD) | **11 / 11** |
| Checks improved | **9** |
| Regressions | **0** |

Critical behavioral result:

- **Before:** mutating Claude `workflow.md` (or injecting drift) under v1.1.3
  check-core + allowlist → **exit 0** (silent).  
- **After:** deleting Phase 8 → **`verify.sh` exit non-zero**.

That is direct evidence that *future agent mistakes of the form “workflow silently
diverged / handoff phase missing”* are more likely to be **caught**.

## Layer B — Canary outputs (secondary)

Source: [`scores.md`](scores.md), artifacts under `before/` and `after/`.

| Side | Shared rubric | Version-specific | Combined |
|---|---|---|---|
| Before | 4.5 / 5 | 0 / 3 | **4.5 / 8** |
| After | 5 / 5 | 3 / 3 | **8 / 8** |

Interpretation: after-version instructions **force** a fuller done-state (handoff +
ratings schema + structural verification). Before-version “done” can be honest and
still omit those artifacts without violating its own adapter text.

## What improved (concrete)

1. **Detectability** of adapter methodology drift (structural floor + CI negative test).  
2. **Staleness visibility** (real SHA markers + threshold fail + auto-bump).  
3. **Default handoff completeness** (Phase 8 + ratings fields in adapter workflows).  
4. **Cross-platform enforcement path** (Windows PS checks in CI).

## What did *not* get proven

1. Higher code correctness on multi-file product features.  
2. Better judgment/architecture choices.  
3. Multi-model or multi-run statistical gains.  
4. Zero contamination (one agent authored both sides).

## Limitations (must keep when citing this report)

- Canaries are **short docs/process tasks**, not large coding problems.  
- Scorer and author are the **same model session**.  
- Guarantee scorecard weights all checks equally (enforcement checks should matter more
  than prose presence; the behavioral drift row is the heavy one).

## Recommendation

- Treat v1.2.0 as a **successful enforcement upgrade**.  
- For ongoing “output quality” tracking, add golden coding canaries with frozen
  fixtures and independent scoring — not only process completeness.  
- Re-run `scripts/eval-gxp-process-guarantees.sh` on each release tag.

## Reproduction

```bash
bash scripts/eval-gxp-process-guarantees.sh v1.1.3 HEAD
bash scripts/verify.sh
```
