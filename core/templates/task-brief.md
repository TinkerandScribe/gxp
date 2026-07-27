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
- Ontology (if used): path or name of the domain model that supplies semantic constraints

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

List **4–8** binary, checkable statements that will all be true when this
task is done. Each one should be either clearly true or clearly false; no
weasel words.

**Tag every line** with exactly one of:

- `[outcome]` — observable end-state the work must achieve (**binding**).
- `[guardrail]` — safety, scope, or prohibited-change constraint (**binding**).
- `[hypothesis]` — implementation idea or layout guess (**non-binding**; revisable
  during Phase 1–2 without a formal brief amendment).

Only `[outcome]` and `[guardrail]` count for Phase 2 self-eval and Phase 6
verification. Do not encode a specific mechanism in a binding line unless the
operator required that mechanism. Style-only qualities ("clean," "idiomatic,"
"elegant") are not valid as binding criteria — put them in non-binding notes if
needed.

**Ontology-referenced guardrails (optional):** When a project ontology exists, you may write binding criteria that cite its invariants, for example:

- `[guardrail] Order.status ∈ {Paid, Shipped, Refunded} (ontology:OrderStatus)`
- `[guardrail] hasRefund is functional — at most one refund per Order`
- `[guardrail] Customer and SupportRep are disjoint classes`

These become part of the deterministic verification ladder (see `core/docs/ontology-guardrails.md`).

- [outcome]
- [outcome]
- [outcome]
- [outcome]
- [guardrail]
- [hypothesis]

**Anti-gaming (non-binding review question):** Does the implementation satisfy
the operator's stated objective, not merely the literal checklist? Surface any
conflict before implementation.

## Ontology / Domain Model (optional)

If this task or project uses an external formal ontology (Coyle-style ledger):

- **Path:** `.ai/ontology/` or `ontology/` (or the path declared in PROGRAM.md)
- **Format:** turtle | shacl | json-schema+shacl
- **Relevant classes / constraints for this task:**
- **How validation will be run:** (command or helper)

Leave this section empty when no ontology is in use. Ontology checks are always opt-in.

## Out of scope

What you are deliberately *not* doing in this task. Anything that surfaces
here gets parked, not expanded into.

## Verification plan

How you will check each criterion. Reference commands from `PROGRAM.md`
where possible. Deterministic checks (type/lint/test/build) go first;
**ontology validation (if declared)** next; behavioral and subjective checks after.

## Self-evaluation gate

Before coding, confirm:

- [ ] **Completeness** — brief covers the real goal, nothing load-bearing missing.
- [ ] **Ambiguity** — every *binding* criterion is strictly binary.
- [ ] **Scope trap** — no "while we're here" cleanup smuggled in.
- [ ] **Verification** — every binding criterion has a concrete check.
- [ ] **Approval gates** — destructive/irreversible/public steps are
  named below and will pause for sign-off.
- [ ] **Criteria quality** — each binding ISC is outcome-focused (or an
  explicit guardrail), independently checkable, and does not encode a
  mechanism unless the operator required it. Style-only binding criteria
  are rejected.
- [ ] **Anti-gaming** — answered the standing question above (objective vs
  literal checklist); any conflict is written down before implementation.
- [ ] **Ontology (if used)** — any ontology-referenced guardrails are loadable and the validation method is named.

## Approval gates

List points in the work where the operator must approve before
continuing (destructive ops, schema migrations, public-facing copy,
production touch). Leave empty if none.

-

## Dead ends

Record approaches that failed twice and were abandoned per the anti-loop
rule. After a second failure on the same approach, record the **reframe**
(problem restated + at least one discarded assumption) before any further
attempt. What was tried, why it failed, what is now believed true. Move
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
