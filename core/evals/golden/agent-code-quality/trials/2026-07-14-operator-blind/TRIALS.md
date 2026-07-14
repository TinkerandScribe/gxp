# Trial cards — 2026-07-14 operator-blind

**Repo:** `C:\Users\Reepicheep\Claude\gxp-public`  
**BASE:** `C:\Users\Reepicheep\Claude\gxp-public\core\evals\golden\agent-code-quality\trials\2026-07-14-operator-blind`

Open a **new** desktop chat for each row. Paste **only** the single prompt from
`DESKTOP_LAUNCH.md` and set **TRIAL_ID** to the number below (or paste the whole
row’s one-liner).

| ID | App | Arm | Task | Model | Correctness (py3.14) | Status |
|----|-----|-----|------|--------|---------------------:|--------|
| 1 | Claude | control | 01-parse-kv | fable | 1.00 | done |
| 2 | Claude | gxp | 01-parse-kv | opus high | 1.00 | done |
| 3 | Claude | control | 04-safe-join | sonnet med | 1.00 | done |
| 4 | Claude | gxp | 04-safe-join | haiku | 1.00 | done |
| 5 | Claude | control | 05-count-words | sonnet extra | 1.00 | done |
| 6 | Claude | gxp | 05-count-words | opus extra | 1.00 | done |
| 7 | Cursor | control | 01-parse-kv | auto | 1.00 | done |
| 8 | Cursor | gxp | 01-parse-kv | grok 4.5 high fast | 1.00 | done |
| 9 | Cursor | control | 04-safe-join | gpt 5.6 terra med | 1.00 | done |
| 10 | Cursor | gxp | 04-safe-join | composer 2.5 | 1.00 | done |
| 11 | Cursor | control | 05-count-words | composer 2.5 | 1.00 | done |
| 12 | Cursor | gxp | 05-count-words | gpt 5.6 terra med | 1.00 | done |

DEST paths: `results/<tool>/<arm>/<task>/` under this BASE (absolute paths in git history of earlier TRIALS revision if needed).

After all 12: run scoring (see `DESKTOP_LAUNCH.md` § After all trials).
