# Experimental-Skill Advisor

**Status:** Experimental / Operator-gated only  
**Does not alter the stable GXP core path.**

## Purpose

After the Phase 0 repo audit, detect when an experimental skill would likely help the current task and *ask* the operator whether to include it for this run. Never auto-activate.

## Detection window

Late Phase 0 / early Phase 1 (after basic repo audit, before the self-evaluation gate hardens).

## Scan checklist (cheap, high-signal only)

- `.ai/PROGRAM.md` (or `core/PROGRAM.md`)
- `.ai/rules/` and `.ai/failures/`
- `docs/plans/` or any design / ADR directories
- Recent ratings related to maintainability or interface issues
- Multi-file or new-interface surface area of the current task
- Complex type or call-graph patterns

## Signals that raise a suggestion (any 2+ is usually enough)

- [ ] Multi-file or new-interface surface area
- [ ] Existing Program Design artifacts, ADRs, or design docs present
- [ ] Complex or scattered types / call graphs visible
- [ ] Prior failure notes about maintainability, interface drift, or “slop”
- [ ] Task language indicates architecture / design / hierarchy work
- [ ] Other experimental skills match current risk profile
- [ ] Task language indicates codebase grading, design debt, spaghetti, God objects, architecture health, or fix-vs-rebuild decision
- [ ] Large files, cycles, or maintainability failure notes present
- [ ] AI-slop / over-abstraction / weak-boundary language in the request or prior ratings
- [ ] Multi-module structural cleanup or quality-gate work

## Behaviour

- If 2+ strong signals exist, surface the single highest-value experimental skill first.
- Ask the operator explicitly with a short block.
- Default to **no** if the operator continues without answering.
- Only activate the skill for the *current run* if the operator confirms.
- Record the suggestion and the operator’s choice in the brief and ratings entry.

## Suggestion template

```
After scanning the repo I see signals that **{skill-name}** 
would likely help on this task.

Include it for this run?  
Reply with: y / n / skip
```

## Hard rules

- Never auto-activate experimental skills.
- Never apply this check on pure Lightweight trivial tasks unless the task has already been upgraded.
- Prefer the single highest-value skill.
- Keep the ask under 6 lines.
