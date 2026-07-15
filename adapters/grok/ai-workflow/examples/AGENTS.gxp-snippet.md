# AGENTS.md — GXP project defaults (snippet)

Copy the block below into your project root `AGENTS.md` (create the file if needed).
Grok Build respects project instructions; this encodes eval-backed stop rules without
a full `.ai/` install.

---

## GXP (Guided eXecution Protocol) — defaults for this repo

### When to use full GXP
- Multi-file or multi-constraint changes
- Config, security, path/isolation, or state-machine behavior
- Underspecified operator asks (agent must invent most criteria)
- Smoke/public tests are thin relative to real “done”

### When lightweight is OK
- Single-file, reversible typo/comment/one-line fix
- Strong named verify already exists and covers the change

### Non-negotiables
1. **Phase 0 before code** when the ask is thin: open project docs / `.ai/PROGRAM.md`,
   `rules/`, `failures/` when present (or state they are absent).
2. Write **4–8 binary Ideal State Criteria** before multi-file work.
3. **Weak public green ≠ done.** Walk each criterion with a tool check.
4. Prefer **two-layer verify**: project suite, then criteria edges.
5. **Handoff** lists commands run and what they proved.

### Heavy / expert path in Grok Build
1. `/plan <task>` — plan must include criteria + verification plan.
2. Approve plan only when criteria are checkable.
3. Implement under GXP; optionally spawn **gxp-verifier** persona for Layer 2.

### Verify
Prefer commands documented in `.ai/PROGRAM.md` or this section. Example placeholder:

```bash
# replace with your real suite
# cargo test
# zig build test
# npm test
```

---
