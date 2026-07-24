# gxp-refine — Cursor invoke prompt

**Operator-invoked only.** Paste this when you explicitly want a `gxp-refine` run.
Do **not** paste this for ordinary implement work. Ordinary
[`START_SESSION.md`](START_SESSION.md) must **not** enter this mode.

Trigger phrases that authorize this mode: **`gxp-refine`**, **`run gxp-refine`**.

---

**Paste this into Cursor:**

```
OPERATOR REQUEST: gxp-refine

Follow core/docs/gxp-refine.md and fill core/templates/gxp-refine-run.md
(copy to core/tasks/<slug>-gxp-refine-run.md).

Hard constraints from core/tasks/gxp-refine-design.md:
- Mode name is gxp-refine only (do not rename the mode).
- Mutation budget = 1 (one weakness, one hypothesis, one logical change, one target, one eval plan).
- Operator-invoked only; do not start refine from ordinary GXP implement/START.
- GATE 1: stop for experiment approval before any candidate edits.
- Evaluate pinned baseline vs candidate on a preregistered corpus/metric.
- GATE 2: separate promotion approval. No auto-apply. No auto-merge.
- Do not weaken core/routing.md rails or core/workflow.md approval gates /
  Verification ladder / anti-loop / L3/L4 language.

Start by skimming evidence (ratings, failures, verify/eval signals), propose the
single weakness+hypothesis+target+eval plan, then STOP at GATE 1.
```

---

## Follow-ups (not this file)

- Claude / Grok skill ports of the same mode
- Always-on rule.mdc auto-entry (forbidden — must stay explicit)
