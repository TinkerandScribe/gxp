# Jev Choice Router — step-choice experiment

Opt-in scaffold under `experiments/` only. **Not** a product adapter. Does not
wire Grok Bot, WorkshopOS, or the default GXP path.

**Inverse of this experiment:** delete `experiments/jev-choice-router/` and
close the pull request.

## Why this exists

This spike asks whether a provider-neutral `ChoiceProvider` plus a caller-owned
cascade (`rules → jev_stub → confidence floor → human`) can pick the **next-step
mode** for a short GXP / ISCP / harness-shaped state. It is a **sibling** of
`experiments/jev-pilot-b/` (DecisionProvider / Gate G1), **not** a fork of Pilot
B labels or cue lists.

Repo language is Python (evals/scripts); the frozen TypeScript contract is
mirrored 1:1 with snake_case fields.

## Frozen contract

```ts
type Choice = 'deterministic' | 'tool' | 'llm' | 'human' | 'halt'
interface ChooseInput {
  state: string | Record<string, unknown> | unknown[]
  question?: string
}
interface ChooseResult {
  label: Choice
  probability: number
  latencyMs: number
  costUsd: number
  confidence?: number
  provider: 'rules' | 'jev' | 'human'
  abstained: boolean
  raw?: unknown
}
interface ChoiceProvider {
  name: string
  choose(input: ChooseInput): Promise<ChooseResult>
}
```

Python: `ChooseResult.latency_ms` ↔ `latencyMs`, `cost_usd` ↔ `costUsd`.
Public types live in `jev_choice_router/types.py` and have no vendor-specific
type names.

## Frozen classify options

Exact option text (also `options.json`). A would-be `jev_classify` call uses
these five keys, `add_none: false`, and the question
`Which next-step mode should handle this step?`:

| Choice | Option text |
|---|---|
| `deterministic` | code/rules can finish this step |
| `tool` | call a named tool / retrieval |
| `llm` | generative model needed (draft / reason / explain) |
| `human` | stop for review |
| `halt` | criteria met or hard stop |

Do not add a sixth label in this tree.

## Cascade order

Caller-owned helper `cascade(providers, input)` walks:

1. **rules** — high-precision hooks; abstain when no hook fires
2. **jev_stub** — would call `jev_classify` with the frozen options (injected
   client; default is a held stub)
3. **confidence floor** — if the Jev label's confidence (else probability) is
   below the threshold, rewrite to `human`
4. **human** — terminal stub; does not abstain

When `CHOICE_ROUTER` is unset/`0`, `default_providers()` **omits Jev**
(flag off = unused). Confidence floor is configurable
(`CHOICE_CONFIDENCE_FLOOR`, default **0.6**) or via
`cascade(..., confidence_floor=...)`.

### Rules hook names

Default `RulesProvider()` registers these hooks (pass `hooks=()` to always
abstain). **Zero model calls** on this path.

| Hook | Fires when | Choice |
|---|---|---|
| `empty_state` | state is `""` / `{}` / `[]` / `None` | `human` |
| `all_criteria_yes` | structured criteria all yes, or “all criteria already yes” | `halt` |
| `hard_stop` | kill gate / named inverse / “criteria met” / hard stop | `halt` |
| `destructive_action` | merge to main / force-push / production-destructive | `human` |
| `draft_prose` | draft prose / PR body / explain / rewrite | `llm` |
| `named_verify` | `verify.sh` / `python -m unittest` / named test command | `deterministic` |
| `open_url_or_search` | open `http(s)://` or search / look up / fetch | `tool` |

Frozen positive fixtures: `tests/fixtures/rules_positives.json`.

These hooks are **not** Pilot B `policy_v1` cues and do not import
`jev_pilot_b` or `data/labels.jsonl`.

## Soft vs live

**This PR is a soft spike.** Hard-usage hold is on.

- Tests inject a fake `JevClassifyClient`. The default
  `HeldJevClassifyClient` never opens a socket; `classify()` raises
  `LiveCallsDisabledError` if reached, and the provider abstains.
- `verify.sh` and scripts do **not** call Jev or MCP.
- Live `jev_classify` (HTTP or host MCP) is the **parent run’s job after
  merge**, only with `CHOICE_ROUTER=1` and an injected client. Not implemented
  here.

### Opt-in flags

Documented in `.env.example`:

```bash
# default: unused
CHOICE_ROUTER=0
# CHOICE_ROUTER=1
# CHOICE_CONFIDENCE_FLOOR=0.6

# Live keys unused on this spike (never commit):
# JEV_API_KEY=
# TYPESAFE_API_KEY=
# JEV_BASE_URL=
# JEV_MODEL=
```

MCP usage (later, not this tree): keep the key on the **server** env, inject a
client whose `classify()` forwards `{state, question, options, add_none}` to
`jev_classify`.

## Optional Noul sketch

`safe_to_act` yes/no **before destructive tools** is a stub interface only
(`jev_choice_router/noul.py`). `HeldSafeToActClient` abstains with log zeros.
No live Noul / Jev calls.

## Logging shape

Every cascade result projects to these fields (**present even if stub zeros**):

| Field | Meaning |
|---|---|
| `label` | chosen `Choice` |
| `probability` | mass on that label (rules fire = `1.0`; stubs may be `0.0`) |
| `latency_ms` | provider wall time |
| `cost_usd` | backend cost when reported; `0.0` on stubs |

See `choice_log()` in `jev_choice_router/logging_shape.py`.

## Gold sheet (N=50)

Filled sheet: **`data/gold.jsonl`**. Regenerator (optional):
`scripts/build_gold.py`.

| Column | Values |
|---|---|
| `id` | row id (`001`…`050`) |
| `state` | short step context |
| `gold` | `deterministic` \| `tool` \| `llm` \| `human` \| `halt` |
| `split` | `calibrate` \| `holdout` (~2/1) |
| `source_tag` | `gxp` \| `harness` \| `iscp` \| `synthetic` |

Honest step-choice traces from GXP / ISCP / harness-shaped moments, plus a
synthetic tail. Classes are balanced 10/10/10/10/10. Split is **34 calibrate /
16 holdout**. Holdout mixes all five golds and all four tags. No PII, secrets,
or Pilot B G1 rows.

## Kill gate

Stop the experiment (delete the folder / close the PR) if any of these hold:

- Named verify needs a live Jev or MCP call to pass
- `core/workflow.md` must change for the spike to be useful
- Pilot B `data/labels.jsonl` or `policy_v1` cues are imported or copied
- A sixth Choice label appears in types or `options.json`

## Named verify

```bash
# from repo root
bash experiments/jev-choice-router/verify.sh
```

Stdlib `unittest` only. No new dependencies. Root `bash scripts/verify.sh` is
unchanged (adapter parity); this experiment is opt-in.

## Ideal State Criteria (this PR)

1. `[outcome]` Only five Choice labels in types / `options.json`
2. `[guardrail]` Deterministic / rules path makes zero model calls (test)
3. `[outcome]` Gold ≥40 with `calibrate` / `holdout` and all five labels
4. `[guardrail]` Opt-in flag `CHOICE_ROUTER` documented; `core/workflow.md` untouched
5. `[guardrail]` No live Jev in verify
6. `[guardrail]` No Pilot B `labels.jsonl` or `policy_v1` cues reused

## Out of scope

- **no default GXP path change** (`core/workflow.md`, product bots, Grok Bot)
- Live `jev_classify` / MCP / HTTP
- Implementing a real Noul `safe_to_act` backend
- Copying Pilot B G1 labels or unshipped cue lists
- Wiring a winner into adapters

## Layout

```
experiments/jev-choice-router/
  README.md
  verify.sh
  .env.example
  options.json
  data/gold.jsonl
  scripts/build_gold.py
  jev_choice_router/types.py
  jev_choice_router/options.py
  jev_choice_router/cascade.py
  jev_choice_router/hooks.py
  jev_choice_router/flags.py
  jev_choice_router/gold.py
  jev_choice_router/logging_shape.py
  jev_choice_router/noul.py
  jev_choice_router/route.py
  jev_choice_router/providers/{rules,jev,human}.py
  tests/
  tests/fixtures/rules_positives.json
```
