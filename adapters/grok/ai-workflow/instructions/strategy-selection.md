# Grok Build Strategy & Model Selection (Prototype)

**Canonical definition:** core/workflow.md Phase 0.5 (tool-agnostic Strategy
& Model Selection).

**Coordination reference:** `core/tasks/EXAMPLE-feature-brief.md`

This is a **Grok-Build-specific specialization** of the core Phase 0.5 process.
It provides automatic task-based switching between:
- Native Grok models (strong reasoning, tool use, long context)
- Composer 2.5 (via `/model composer-2.5` or persona override — excellent for coherent multi-file agentic coding)
- Structured handoff to Cursor Composer (when visual IDE, side-by-side editing, or Cursor-specific strengths are better)

It must feed GXP critic scoring (gxp_alignment_score, criteria_evaluation) and
respect the coordination brief's constraints. The decision skeleton (classify,
choose least-capable engine with margin, record, re-evaluate) lives in core.

## When to Invoke Strategy Selection

Run this **early** (end of Phase 0 or start of Phase 1/3) for any non-trivial goal. Use GXP language for the classification.

Trigger signals (lightweight version of self-evaluation gate):
- High ambiguity, architecture, planning, research, or multi-constraint underspecified goal → **Parallel research + planning** (gxp-researcher + gxp-architect) then **`/plan`**
- Underspecified multi-factor ask or thin smoke verify → **`/plan` first**, then full GXP execute (suggest `/plan` explicitly in transcript)
- Coherent multi-file edits, long-running implementation, "make it work end-to-end", large refactors → Composer 2.5 (composer-coder)
- "Visual", "side-by-side", "in the IDE", "Cursor specific", "browse files visually" → Cursor handoff
- After implement on multi-file / multi-constraint work → optional **gxp-verifier** persona (criteria-only; no product edits)
- Quick terminal/debug/small reversible change → Fast native Grok (lightweight GXP OK)

Always produce a short "Strategy Decision" note using GXP style:
- Goal classification
- Chosen brain + justification (tied to Ideal State Criteria style)
- Capability check note (see below)
- Scoped context plan

## Classification Logic (GXP-aligned)

Classify using the same rigor as Phase 2 self-evaluation gate:

1. **Read the goal + any initial brief.**
2. Ask (internally or with a quick subagent if complex):
   - Does this have genuine ambiguity about approach? (Phase 0/plan-mode trigger)
   - Is the core work "coherent multi-file coding / agentic implementation over many files"? (Composer strength per Cursor adapter)
   - Does success require visual inspection, inline edits in context of many open files, or Cursor ecosystem features?
   - Is it small, reversible, terminal-heavy?
3. Map to persona / mode / handoff.
4. Document decision with binary-style justification.

**Example Decision Output (must appear in transcript):**
```
[Strategy Selection]
Goal: Add full task-based model switching...
Classification:
- Multi-file coherent refactoring across adapter + instructions + examples
- Requires long-context agentic coding with clean diffs
- No strong visual/IDE requirement in this repo
Chosen: composer-coder persona (model=composer-2.5, high reasoning effort)
Justification: Matches "coherent multi-file" ISC from coordination brief. Better sustained work than native on this class of task.
Capability note: external_apis available (GROK/XAI keys present); future "grok_subagent" connector would be checked here.
Scoped context: Only the coordination brief + relevant adapter files + workflow.md will be provided to the subagent.
Next: Spawn subagent with composer-coder persona.
```

## Recommended Personas (define in ~/.grok/personas/ or project .grok/personas/)

See examples in this adapter under `examples/grok-build-strategy/personas/`.
`install-grok-skill` copies them into `~/.grok/personas/*.toml`.

| Persona | Primary use |
|---------|-------------|
| `gxp-researcher` | Parallel research: aggressive tool use, candidate criteria, uncertainty notes |
| `gxp-architect` | Parallel planning: binary criteria, out-of-scope, verification plan, trade-offs |
| `grok-native-planner` | Single-agent planning / high-ambiguity (lighter alternative to parallel pair) |
| `composer-coder` | Coherent multi-file implementation (Composer 2.5) |
| `gxp-verifier` | Layer-2 criteria-only critic after implement (no product edits) |

- **gxp-researcher.toml** / **gxp-architect.toml** — prefer these two in parallel for Heavy-style front-half work.
- **composer-coder.toml** — model = composer-2.5, clean multi-file diffs.
- **gxp-verifier.toml** — criteria-only; runs tests; does not edit product code.
- **grok-native-planner.toml** — native Grok single planner when parallel spawn is unnecessary.

For Cursor handoff, use a skill instead of persona (see below).

## Parallel Research + Planning (Heavy-style front half)

When classification signals high ambiguity, multi-constraint, or underspecified multi-factor goals, prefer a short parallel team instead of a single planner:

1. **Spawn in parallel** (scoped context only):
   - `gxp-researcher` — explore codebase/docs/failures, surface findings + candidate criteria + residual uncertainty.
   - `gxp-architect` — shape a GXP plan (goal, 4–8 binary Ideal State Criteria, out-of-scope, verification plan, Phase 0 files).

2. **Parent synthesizes** the two artifacts into one coherent plan. Resolve conflicts in favor of binary, tool-checkable criteria and explicit out-of-scope.

3. **Present the synthesized plan** (or feed it into `/plan`) for operator approval. Do not treat plan approval as “tests already passed.”

4. **After approval**, hand to `composer-coder` (or native implementer) for execution, then optionally `gxp-verifier` for Layer 2.

Example Strategy Decision for this path:
```
[Strategy Selection]
Goal: ...
Classification:
- High ambiguity / multi-constraint / underspecified
- Benefits from parallel research + structured planning before code
Chosen: parallel gxp-researcher + gxp-architect → synthesize → /plan
Justification: Matches Heavy-style front-half pattern; keeps Ideal State Criteria binary and Phase 0 first.
Capability note: external_apis / subagent spawn available.
Scoped context: brief + 2–4 key files + any existing PROGRAM.md / failures notes only.
Next: Spawn both personas in parallel; synthesize; request plan approval.
```

This pattern stays inside GXP rails: no scope expansion without operator approval, binary criteria remain sacred, two-layer verify still required on multi-file work.

## Cursor Handoff Skill (Prototype)

When classification chooses Cursor:
- Generate (or reuse) a GXP task brief.
- Produce a self-contained handoff block that the user can paste into Cursor Composer.
- The handoff must align with `adapters/cursor/ai-workflow/rule.mdc` and `START_SESSION.md`:
  - Reference `.ai/PROGRAM.md` and verification commands.
  - Emphasize "Review the full Composer diff before accepting".
  - Use binary criteria where possible.

Example handoff output (the skill should emit this):

```
=== CURSOR COMPOSER HANDOFF (GXP aligned) ===
Goal: [paste goal]
Context: [key files + links + previous ratings/failures]
Ideal State Criteria:
- [ ] ...
Out of scope: ...
Verification plan: Run commands from .ai/PROGRAM.md first.

Paste the following into Cursor Composer (use @-references for files):
"Follow the GXP workflow. Use Composer for this coherent multi-file work.
[full brief here]
Start by reading the coordination brief and relevant adapter files."
```

## Capability Gate Integration (Enhanced)

Before choosing a "different brain":
- Check `external_apis` in CapabilityManifest (covers LLM surfaces like GROK_API_KEY, XAI_API_KEY per capability_gate.py).
- Log explicitly: "Capability check: external_apis = <bool> (from env or manifest)".
- For Grok Build sessions: assume available unless env keys missing; fall back to native if not.
- Extension point: In future (post Phase 2b/3), add connectors like "grok_subagent_model" or "cursor_composer_handoff" to CONNECTORS and derive per AgentType in derive_agent_capabilities().

Example check (can be implemented via env probe or future tool):
```
$hasGrokKey = $env:GROK_API_KEY -or $env:XAI_API_KEY
$capabilityNote = "Capability check: external_apis = $hasGrokKey"
```

If false, fall back and document limitation in Strategy Decision. This advances ISC #3 from coordination brief.

## Automatic Invocation

This strategy logic is intended to be invoked automatically by the main GXP skill for goals that trigger "should_brief" or complex signals (see orchestrator patterns and workflow.md).

In a Grok Build session:
- The agent (you) should run the classification as the first tool-using step for qualifying tasks.
- Then call `spawn_subagent` with the chosen persona (or `/model` + normal subagent), passing **scoped context only** (e.g., brief + 2-3 key files + strategy decision; no full trace per Phase 2a spirit).
- Example spawn (with scoped prompt):
  ```
  spawn_subagent with persona "composer-coder", prompt: "Strategy Decision: [paste decision]. Goal: ... Context (scoped): [brief + relevant files only]. Implement per GXP."
  ```
- Include the full "Strategy Decision" block in rich_for_critique or as extra evidence so parent critic can compute gxp_alignment_score / criteria_evaluation against the original brief. This feeds Phase 6 rating.
- Or emit the handoff and pause for user to switch contexts.

This advances ISC #4 (scoped) and #5 (critic feed) from the coordination brief.

## Verification of This Prototype

- Adapter sync remains green (Composer guidance and capability sections untouched; re-run check-core.ps1 -Lenient after changes).
- Classification decisions appear in transcripts with GXP language (binary ISC justification, capability note, scoped plan).
- Handoff artifacts are copy-paste ready for Cursor and reference the right rules (rule.mdc, PROGRAM.md, full diff review).
- Decisions feed critic-style scoring (include in rich_for_critique or as gxp_ extra; supports gxp_alignment_score).
- Small e2e: Use the "Strategy selection test" in TEST_PROMPT.md; demonstrates >=2 classes with artifacts.

See the coordination brief for the full 8 Ideal State Criteria this prototype advances (now #2, #3 (via check+log), #4 (scoped examples), #5 (critic example), #6, #7, #8).

---

**Prototype status:** Enhanced implementation in Grok adapter (capability check, scoped spawn examples, critic feed). Does not modify the upstream orchestrator, core/, or capability_gate (per out-of-scope and plan sequencing). Extension points documented for Phase 2b/3. Advances multiple ISCs in adapter layer; B1 path fix + last-synced refresh included as parallel Track B hygiene.
