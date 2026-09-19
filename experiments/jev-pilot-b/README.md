# Jev Pilot B — DecisionProvider experiment

Opt-in scaffold under `experiments/` only. **Not** a product adapter. Does not
wire Grok Bot, WorkshopOS, or any chat surface.

**Inverse of this experiment:** delete `experiments/jev-pilot-b/` and close the
pull request.

## Why this exists

Pilot B asks whether a provider-neutral `DecisionProvider` plus a caller-owned
cascade (`rules → jev → llm → human`) can score one artifact against one Ideal
State Criterion (Gate G1). This folder freezes the contract, stubs the
backends, and ships a 120-row label-sheet plan. It does not run a live A/B.

Repo language is Python (evals/scripts); the frozen TypeScript contract is
mirrored 1:1 with snake_case fields.

## Frozen contract

```ts
type Decision = 'pass' | 'fail' | 'needs_review'
interface DecideInput {
  artifact: string | Record<string, unknown> | unknown[]
  question: string
  yesMeans?: string
  noMeans?: string
  yesAtOrAbove?: number
  noAtOrBelow?: number
}
interface DecideResult {
  decision: Decision
  p?: number
  confidence?: number
  provider: 'rules' | 'jev' | 'llm' | 'human'
  latencyMs: number
  cost?: number
  abstained: boolean
  raw?: unknown
}
interface DecisionProvider {
  name: string
  decide(input: DecideInput): Promise<DecideResult>
}
```

Python: `DecideInput.yes_means` ↔ `yesMeans`, `DecideResult.latency_ms` ↔
`latencyMs`. Public types live in `jev_pilot_b/types.py` and have no
vendor-specific type names.

## Cascade order

Caller-owned helper `cascade(providers, input)` walks this default order:

1. **rules** — deterministic hooks; abstain when no hook fires
2. **jev** — MCP-shaped check (`yes→pass`, `no→fail`, `uncertain→needs_review`)
3. **llm** — judge interface only; live calls not implemented (abstains)
4. **human** — terminal stub; `needs_review`, does not abstain

A provider that returns `abstained=True` is skipped. The caller assembles the
list (omit or swap backends). Nothing here is installed into a bot.

Optional: construct the Jev backend with `abstain_on_uncertain=True` so an
uncertain check continues the cascade instead of stopping at `needs_review`.

## Gate G1

```text
gate_g1(artifact, criterion, provider) → decide()
```

One artifact, one Ideal State Criterion string (the yes/no `question`). Pass a
single provider or wrap `cascade` in a tiny adapter that implements
`DecisionProvider`.

## Label sheet (N=120 plan)

Templates: `data/labels.template.jsonl` and `data/labels.template.csv`.

| Column | Values |
|---|---|
| `id` | row id (`001`…`120`) |
| `artifact` | text or serialized state |
| `criterion` | Ideal State Criterion (yes/no question) |
| `gold` | `pass` \| `fail` \| `needs_review` |
| `split` | `calibrate` \| `holdout` |
| `source_tag` | provenance (`synthetic-stub` today) |

Shipped rows: 5 synthetic examples (3 calibrate / 2 holdout). Planned sheet:
**120** labelled rows, suggested **60 calibrate / 60 holdout**. Do not pull
real labelled data in this scaffold.

## Metrics (report these on a later A/B)

| Metric | Meaning |
|---|---|
| **accuracy** | `decision == gold` on holdout (optionally treat `needs_review` as neither) |
| **calibration** | reliability of `p` vs empirical pass rate on calibrate, then confirm holdout |
| **latency** | `latency_ms` per call and per cascade |
| **cost** | `cost` when the backend reports it |
| **abstention** | rate of `abstained=True` (and of `needs_review` when that is the stop) |
| **disagreement** | pairwise provider mismatch on the same `(artifact, criterion)` |

## How to run A/B later

1. Fill `data/labels.template.jsonl` (or CSV) to 120 gold rows; keep splits
   disjoint.
2. Calibrate check thresholds (`yes_at_or_above` / `no_at_or_below`) and any
   rules hooks on **calibrate** only.
3. Freeze the cascade variants to compare, for example:
   - A: `rules → human`
   - B: `rules → jev → human`
   - optional C: `rules → jev → llm → human` once an LLM judge exists
4. Score **holdout** for the six metrics above. Do not retune on holdout.
5. Keep the run local (`core/evals/**/trials/` style). Do not wire winners
   into product bots from this folder.

Live HTTP (optional, not required for verify):

```bash
export JEV_API_KEY=   # or TYPESAFE_API_KEY; never commit
# optional: JEV_BASE_URL, JEV_MODEL
```

**MCP:** configure the host `jev_check` server with `JEV_API_KEY` /
`TYPESAFE_API_KEY` in *server* env (not tool arguments). Inject a
`JevCheckClient` whose `check()` forwards MCP-shaped
`{state, question, yes_means, no_means, yes_at_or_above, no_at_or_below}`
and returns `{verdict, probability_yes, ...}`.

## Named verify

```bash
# from repo root
bash experiments/jev-pilot-b/verify.sh
```

Stdlib `unittest` only. No new dependencies. Root `bash scripts/verify.sh`
is unchanged (adapter parity); this experiment is opt-in.

## Ideal State Criteria (this scaffold)

Binding criteria from the Pilot B brief:

1. `[outcome]` Public types have no Jev-specific names
2. `[guardrail]` `core/workflow.md` and `adapters/grok-bot` core path unchanged
   (diff empty for those)
3. `[guardrail]` Opt-in experiment only; no product bot wiring
4. `[guardrail]` The two-word phrase that means a nameless revert is absent
   from this tree (named inverse only: delete the folder / close the PR)
5. `[outcome]` This README lists cascade order and metrics: accuracy,
   calibration, latency, cost, abstention, disagreement
6. `[outcome]` Label template has columns for the 120-row plan
7. `[outcome]` Named verify (`bash experiments/jev-pilot-b/verify.sh`) passes

## Out of scope

- Product bots, Grok Bot adapter wiring, WorkshopOS
- Prose generation
- Fleet MCP install
- Implementing live LLM calls
- Pulling real labelled data (stub rows only)

## Layout

```
experiments/jev-pilot-b/
  README.md
  verify.sh
  .env.example
  data/labels.template.jsonl
  data/labels.template.csv
  jev_pilot_b/types.py
  jev_pilot_b/cascade.py
  jev_pilot_b/gate_g1.py
  jev_pilot_b/labels.py
  jev_pilot_b/providers/{rules,jev,llm,human}.py
  tests/
```
