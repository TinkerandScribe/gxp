# Task brief — Cursor rule on generator (Roadmap M8, deferred)

**Status:** draft — **deferred** until M4–M5 stable; high risk  
**Depends on:** generator stable in production use; operator re-open  
**Workflow:** full  

## Goal

Evaluate and (if approved) put Cursor’s published methodology surface on a
controlled generation path **without** destroying Phase -1 capability gate or
dual-path `.ai` vs `core` notes.

## Context

- Hybrid P2-4 explicitly left `rule.mdc` hand-authored.  
- Cursor check is structural markers on `rule.mdc`, not the same floor as claude/grok.  
- Full core dump into alwaysApply rules may be too large / wrong shape.

## Ideal State Criteria (if executed)

- [ ] 1. Written ADR: generate full rule vs generate appendix vs keep hand-authored.  
- [ ] 2. If generate: delta file holds Phase -1 + Cursor-only content; shared phases
  from core or a compressed template.  
- [ ] 3. `adapters/cursor/.../check-core.sh` and `.ps1` still PASS.  
- [ ] 4. `verify.sh` exit 0; no whole-file allowlist regression.  
- [ ] 5. Document edit path in CONTRIBUTING.  
- [ ] 6. Generator `--check` (or cursor-specific check) in CI if generated.

## Out of scope

- Forcing Cowork plugin onto the same generator.  
- Removing Phase -1.

## Verification plan

Cursor sync checks; verify.sh; manual Cursor session smoke (operator).

## Default disposition

**Do not pick up** until operator explicitly prioritizes Cursor packaging over M6/M7.
