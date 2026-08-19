# Routing Policy (GXP Phase 0.5)

Operationalizes **GXP Phase 0.5 engine selection** as a runtime routing policy: given a
job, decide **which engine** runs it and **whether a human must be in the loop**. This
file is portable, tool-agnostic methodology. A dispatcher *applies* it; you *own* and
adapt it. The engine names below are **examples** — replace them with the tools you
actually use.

**Note:** Scaffolding capability tier (`frontier` | `standard` | `constrained`) is
orthogonal to this routing table. It modulates prompt/skill intensity for a chosen
engine; it does not replace privacy/stakes rails or `exec_mode`. See
`core/docs/capability-scaffolding.md`.

## Two kinds of route (important)

Not every engine is something a dispatcher can invoke autonomously:

- **Auto-dispatch routes** — a dispatcher can run these directly without a human:
  e.g. an autonomous coding agent, a local model, direct API model calls.
  - **Headless approval rule:** an autonomous run should withhold **irreversible** and
    **destructive** actions unless a human has pre-approved them. Reversible (undoable)
    work can run unattended; anything you cannot cleanly undo gates on a human. Make this
    explicit in the engine's invocation (e.g. an `--approve-reversible` flag), not implicit.
  - **Named inverse:** if you load an adapter, plugin, MCP, skill, or Phase 3 handoff,
    name its inverse (how to unload it). Unload = apply that named inverse (left-inverse;
    LIFO if several). If you cannot name an inverse, treat the action as irreversible and
    use the existing human gate. Inverse correctness is the author's obligation; GXP does
    not verify it.
- **Recommend-to-human routes** — the policy *selects* them but a human executes:
  e.g. a browser-driven research tool, an in-IDE assistant, a Custom GPT / web assistant
  for brief/planning, a human-in-the-loop composer. The dispatcher surfaces a
  recommendation; it does **not** auto-run these.

Every routed job therefore carries an `exec_mode`: `auto` or `recommend-to-human`.

## Routing keys

Classify each job on the Phase 0.5 dimensions: **task type · privacy class · stakes ·
cost · latency · location (desk/mobile) · reversibility.**

## Policy table (example — adapt the engine column to your stack)

| Job need | Privacy / Stakes | Route | Exec mode | Verification |
|---|---|---|---|---|
| Research / ideation / critique | low / web-ok | research tool | recommend | optional second-model critic\* |
| Autonomous multi-file coding | public / verified | strong coding agent | auto | GXP deterministic + optional critic\* |
| Long autonomous build-verify loops | mixed | autonomous agent (auto) · IDE (recommend) | auto · recommend | GXP + honest ratings |
| Offline / private code execution | **private** | local agent + local model | auto | independent review\* — not the agent's own self-score |
| Cheap / bulk / background | low / private | local model | auto | spot-check |
| Scheduled monitoring / briefing | read-only | dispatcher-direct | auto | — |
| High-stakes / safety-relevant | **safety** | strong agent → human | auto + **human** | independent review\* + **human sign-off** |
| In-IDE scoped edits | at-desk | IDE assistant | recommend | GXP lightweight |
| GXP brief / planning (web, no repo) | low / web-ok | Custom GPT / web assistant | recommend | binary criteria + verification plan |

## Hard overrides (applied after the table match)

1. **Privacy rail.** A `private`/local-only job is routable **only** to local engines
   (local agent, local model, dispatcher-direct). Never to a web tool, a hosted API, or
   the open web. No exceptions.
2. **Stakes → verification depth.** `low` = spot-check · `high` = GXP deterministic +
   an independent review\* · `safety` = independent review\* **and** human sign-off before
   any output is emitted. High/safety verification is **never** an agent grading its own
   work.

\* **Critic language (recommended, not shipped):** "real critic" / second-model critic means
an independent review pass — a second engine, human, or checklist — not a required subsystem
in this package. Shipping an automatic multi-provider critic (keys, cost, providers) is
explicitly out of scope for the core methodology package; projects that need it can add an
opt-in `scripts/critic.sh` later. The table still **recommends** independent review for
high/safety stakes; it does not require this repo to host that tooling.

## Decision procedure (hybrid)

1. **Deterministic match** on (task type, privacy, stakes) against the table.
2. **LLM classify** (dispatcher) only if no clean match — and **log the decision**.
3. Apply the **hard overrides** (privacy rail, stakes gate) — they win over any match.
4. Unknown / unclassifiable → fall back to `recommend-to-human`; never silent auto-run.

## Escalation / fallback

On failure or low confidence, re-evaluate at the **GXP Phase 4 anti-loop gate** and
escalate the engine — e.g. `small → large model`, `local → API`, `autonomous → human-in-loop`.
Never retry the same engine on the same failure.

## Job contract

Jobs are described with the GXP task brief plus its **Routing block** (see
`templates/task-brief.md`): `privacy_class`, `stakes`, `engine_candidates`,
`forbidden_engines`, `exec_mode`, `output_contract`.

## Validation criteria (binary — must hold before you rely on the router)

Adapt these into tests against your own dispatcher:

- [ ] A `private`/local-only job routes **only** to local engines and **never** touches an
  API or web route.
- [ ] A `safety`/`high`-stakes job always reaches a real critic **and** a human sign-off
  step before any output is emitted.
- [ ] An unclassifiable job resolves to `recommend-to-human`, not a silent auto-run.
- [ ] No `recommend-to-human` route is ever auto-executed.
