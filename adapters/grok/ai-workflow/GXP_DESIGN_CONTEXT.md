# GXP Design Context (Experimental)

**Operator-invoked only** (or via Experimental-Skill Advisor).

Paste this (or `@GXP_DESIGN_CONTEXT.md`) when you explicitly want a `gxp-design-context` run, or when the advisor has recommended it and you replied `y`.

Canonical how-to: `core/docs/experimental/gxp-design-context.md`.

---

**Paste this into Grok / Grok Build:**

```
OPERATOR REQUEST: gxp-design-context

Follow core/docs/experimental/gxp-design-context.md.

Hard constraints:
- Never write implementation bodies
- Keep artifacts short and scannable (call-stack trees with +/-, file-tree diffs, types + signatures only)
- Produce least-confident decisions list
- Suggest 4-8 binary Ideal State Criteria from the design decisions
- Stop for operator review of least-confident decisions before any implementation

Write the artifacts under docs/plans/<feature-slug>/03-program-design.md (or project equivalent).

Start by scanning relevant existing design artifacts, types, and call flows, then draft the Program Design artifacts.
```

---

## Not always-on

Ordinary GXP `SKILL.md` / Full-workflow sessions do **not** auto-enter this mode.
It is activated only by explicit operator request or confirmed advisor suggestion.
