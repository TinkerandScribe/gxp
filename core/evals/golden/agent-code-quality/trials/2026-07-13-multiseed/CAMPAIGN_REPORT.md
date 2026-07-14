# Multi-seed control vs GXP campaign (2026-07-13)

## Method

- **Control seeds:** three incomplete one-shot implementations per task (no scorer loop).
- **GXP arm:** reference solution + GXP brief + score_trial verify-to-green.
- **Scorer:** hidden tests only (`score_trial.py`).
- **Limitation:** fixtures authored in-repo (not a blind multi-model study); measures
  whether verify-to-green process beats common incomplete one-shots.

## Results

| Task | Control seed | Control | GXP | Winner |
|---|---|---:|---:|---|
| 01-parse-kv | `s1_skip_invalid` | 0.600 (6/10) | 1.000 (10/10) | **gxp** |
| 01-parse-kv | `s2_always_strip` | 0.900 (9/10) | 1.000 (10/10) | **gxp** |
| 01-parse-kv | `s3_no_quote_unwrap` | 0.900 (9/10) | 1.000 (10/10) | **gxp** |
| 02-slugify | `s1_spaces_only` | 0.250 (2/8) | 1.000 (8/8) | **gxp** |
| 02-slugify | `s2_keep_underscore` | 0.875 (7/8) | 1.000 (8/8) | **gxp** |
| 02-slugify | `s3_no_lower` | 0.375 (3/8) | 1.000 (8/8) | **gxp** |
| 03-merge-intervals | `s1_no_sort` | 0.875 (7/8) | 1.000 (8/8) | **gxp** |
| 03-merge-intervals | `s2_strict_less` | 0.875 (7/8) | 1.000 (8/8) | **gxp** |
| 03-merge-intervals | `s3_mutate` | 0.875 (7/8) | 1.000 (8/8) | **gxp** |

**Pairwise seeds:** GXP wins **9**, control **0**, ties **0** (n=9).
**Mean correctness:** control **0.725**, GXP **1.000**.

## Multi-runner selftest attestation

| Runner | Command | Result |
|---|---|---|
| Grok (this session / prior) | `bash scripts/eval-agent-code-quality-selftest.sh` | **PASS** (starter < reference on all 3 tasks) |
| Cursor Auto | same | **PASS** (parse-kv 0.6, slugify 0.0, merge 0.75 vs 1.0) |
| Claude Code | same | **PASS** (same separation; also fixed Windows python stub portability) |

Harness reliability is independently confirmed on three environments.
Causal GXP superiority still needs agents that did not author the fixtures.

## Verdict

- **Harness:** reliable across runners.
- **This multi-seed campaign:** GXP mean higher (1.000 > 0.725); GXP wins 9/9 pairwise seed comparisons.
- **Claim level:** process+verify-to-green beats incomplete one-shots under these tasks; **not** a multi-model field study.

