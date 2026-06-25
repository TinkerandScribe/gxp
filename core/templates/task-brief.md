# Task brief

**Date:**
**Task slug:**
**Workflow:** full / lightweight

## Goal

One sentence describing what success looks like.

## Context

- Related files:
- Related PRs / tickets:
- Relevant `.ai/rules/` entries:
- Relevant `.ai/failures/` entries:
- Background needed to understand the task:

**Strategy/Model:** [chosen engine] — [one-line reason tied to the criteria]

## Routing

For dispatch via the routing policy (`core/routing.md`). Fill when the job may be
routed to an engine automatically; otherwise leave defaults.

- **privacy_class:** public | private — *private → local engines only (hard rail)*
- **stakes:** low | high | safety — *safety → real critic + human sign-off*
- **engine_candidates:** [claude-code | local-agent | perplexity | grok | cursor | chatgpt | api-direct]
- **forbidden_engines:** [...] — *e.g. all API/web routes when private*
- **exec_mode:** auto | recommend-to-human
- **output_contract:** [expected shape of the result]

## Ideal State Criteria

List 4 to 8 binary, checkable statements that will all be true when this
task is done. Each one should be either clearly true or clearly false; no
weasel words.

- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

## Out of scope

What you are deliberately *not* doing in this task. Anything that surfaces
here gets parked, not expanded into.

## Verification plan

How you will check each criterion. Reference commands from `PROGRAM.md`
where possible. Deterministic checks (type/lint/test/build) go first;
behavioral and subjective checks after.

## Self-evaluation gate

Before coding, confirm:

- [ ] **Completeness** — brief covers the real goal, nothing load-bearing missing.
- [ ] **Ambiguity** — every criterion is strictly binary.
- [ ] **Scope trap** — no "while we're here" cleanup smuggled in.
- [ ] **Verification** — every criterion has a concrete check.
- [ ] **Approval gates** — destructive/irreversible/public steps are
  named below and will pause for sign-off.

## Approval gates

List points in the work where the operator must approve before
continuing (destructive ops, schema migrations, public-facing copy,
production touch). Leave empty if none.

-

## Dead ends

Record approaches that failed twice and were abandoned per the anti-loop
rule. What was tried, why it failed, what is now believed true. Move
durable lessons to `failures/` on handoff.

-

## Handoff notes

To fill in at the end:

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Approval gates hit and outcomes:
- New `failures/` entries or rules:
- Rating entry reference:
