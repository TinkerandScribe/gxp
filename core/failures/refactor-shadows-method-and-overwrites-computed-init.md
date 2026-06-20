# Failure capture

**Date:** 2026-06-15
**Task / context:** Supervisor merge-blockers surfaced after the planner+specialists refactor (`src/agents/supervisor.py`).

## Expected

- A subtask routed to the fallback branch executes via the executor specialist.
- A supervisor built with a medium/high computed trust score exposes that level at `self.capabilities.trust_level`, so trust gating actually varies with trust.

## Actual

- The fallback path `await self._executor_agent(subtask)` raised `TypeError: _executor_agent() missing 1 required positional argument: 'ctx'` — two methods named `_executor_agent` existed (a 2-arg legacy version and a 3-arg delegator); Python kept the later 3-arg one, so the 1-arg call crashed and the legacy body was dead/unreachable.
- `self.capabilities.trust_level` was **always** `"low"`: `__init__` built the trust-aware manifest, then two duplicated copy-paste lines re-assigned `self.capabilities = build_capability_manifest()` (no-arg → default `"low"`), silently discarding the computed level and disabling trust gating.

## Root cause

Incomplete rename during a monolith-splitting refactor (`_shell_runner_agent` → `_executor_agent`) landed a second definition on top of a legacy one (**method shadowing**), and an earlier copy-paste left two redundant manifest re-inits that **overwrote a computed value** with a default.

## Detection

- Grep smell: more than one `async def <name>` for the same method in a class; a no-arg `self.X = build_*()` appearing *after* an earlier `self.X = build_*(param=...)`.
- A call site passing fewer args than the live definition requires.
- Behavioral: `Supervisor(...).capabilities.trust_level` never changes off `"low"` regardless of trust score.

## Resolution

Removed the dead 2-arg `_executor_agent` (kept the 3-arg delegator), passed `ctx` at the fallback call site, and deleted the duplicate no-arg manifest assignments (kept the `trust_level=level` one). `supervisor.py` only; 76 tests pass; behavioral check confirms the level now propagates.

## Prevention

- Regression coverage lives in `tests/test_supervisor_merge_blockers.py`:
  constructor trust propagation (fresh instance, no post-hoc `capabilities` reassignment),
  static guard against no-arg `build_capability_manifest()` in `__init__`,
  behavioral `run()` tests proving high trust dispatches reversible work and low trust withholds it.
- Watch for this class during any refactor that renames methods or re-inits computed state.

## Follow-up

- [x] Add regression test in `tests/` for constructor trust-level propagation (do not reassign `capabilities` in the test).
- [x] Add behavioral `run()` trust-gate tests (low trust withholds / high trust dispatches reversible).
- [ ] During refactors, grep for duplicate `async def` names before committing.

## Repeatable?

Yes — both are generic refactor hazards in a repo that refactors itself. The regression suite now covers constructor propagation and end-to-end gating behavior.
