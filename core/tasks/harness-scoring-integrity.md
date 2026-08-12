# Task brief

**Date:** 2026-08-10
**Task slug:** harness-scoring-integrity
**Workflow:** full

## Goal

Make `score_trial.py` produce scores that mean what they claim: a cheating solution
must not score as correct, and a GXP-compliant solution must not be zeroed for emitting
the artifacts GXP itself mandates.

## Context

- Related files: `core/evals/golden/agent-code-quality/harness/score_trial.py`
  (`_run_unittest_dir` L72–105, `score_scope` L165–210, composite L244–258);
  `scripts/eval-agent-code-quality-selftest.sh` (in-tree regression gate);
  `core/evals/golden/agent-code-quality/tasks/*/hidden_tests/`.
- Related PRs / tickets: raised as finding F1 (critical) and F2 (medium) in the
  2026-07 codebase review; **both re-verified still open on 2026-08-10**.
- Relevant rules: none binding beyond the usual; no secrets or local context involved.
- Relevant failures: `core/failures/webfetch-summarizer-invents-plausible-details.md`
  (verify by execution, not by reading) — this brief's claims were produced by running
  the reproducer, not by inspection alone.
- Ontology (if used): none.

**Defect 1 — scores are forgeable (critical).** `_run_unittest_dir` discovers and runs
the hidden tests **in the scorer's own process**, and the hidden tests import the
candidate module, so candidate top-level code executes before any assertion. A solution
that returns `{}` for every input but sets
`unittest.TestResult.addFailure = lambda *a, **k: None` (and `addError`) scores
`correctness 1.0, tests_passed 10/10, no_test_tamper True, disqualified False,
primary_code_score 1.0`. Reproduced twice, most recently today. `subprocess` is
imported at L16 but never used. The `no_test_tamper` gate cannot help: it only hashes a
`hidden_tests/` dir *shipped by the agent* (L230–238), and defaults to `True` when the
agent ships none — which is the normal case. `disqualified` is defined as
`not no_tamper` (L257), so it is near-permanently `False`.

*Detection hint for the implementer:* the custom result class still appends `FAIL …`
lines to `buf_out` even when the patched base swallows the failure, so under this
attack `test_log` and `tests_passed` disagree. That inconsistency is a useful assertion
but is **not** a sufficient fix — other vectors (e.g. patching the runner) leave no such
trace. Process isolation is the fix; the log/count cross-check is a cheap belt-and-braces.

**Defect 2 — the harness penalizes GXP's own outputs (medium, measurement-validity).**
`score_scope` permits any `*.md`, plus `test_*`, `tests/`, `BRIEF*`, `HANDOFF*`, and an
`allowed_exact` set (`ERROR.txt`, `agent_tool_log.jsonl`, `raw_model_output.md`, …).
It does **not** permit `ratings.jsonl` (the Phase 6 artifact GXP requires) or a
`verify_adhoc.py` (a Phase 5 verification script). Both therefore set `scope_ok=False`,
which zeroes `primary_code_score` via `code_ok` (L245). Verified: a reference solution
scoring `correctness 1.0` plus those two files reports
`scope_ok False, primary_code_score 0.0`. This is not merely unfair — it biases
campaigns *against* the GXP arm in trials whose purpose is measuring whether GXP helps.
The 2026-07-13 blind campaign's recorded FAIL was driven partly by exactly two GXP-arm
scope failures of this kind.

**Strategy/Model:** claude-code / local-agent — single-file change with an executable
reproducer as the acceptance test; no design novelty, but correctness-critical.

**Scaffolding tier:** standard — well-understood change (run tests out-of-process),
bounded surface, strong deterministic verification available.

## Routing

- **privacy_class:** public
- **stakes:** high — this scorer underwrites the project's public claims about GXP's
  effect; a wrong number here propagates into `GXP_WINS.md`-class assertions.
- **engine_candidates:** [claude-code, local-agent, cursor]
- **forbidden_engines:** []
- **exec_mode:** recommend-to-human (brief approved before implementation)
- **output_contract:** PR modifying the harness + a committed reproducer fixture;
  selftest and `verify.sh` green; before/after scores for the reproducer recorded.

## Ideal State Criteria

- [outcome] 1. The monkeypatch reproducer (candidate that returns `{}` and patches
  `unittest.TestResult.addFailure`/`addError`) scores `correctness` ≤ 0.1 **and** is
  reported as failing — i.e. it can no longer present as a correct solution.
- [outcome] 2. Hidden tests execute in a **separate process** from the scorer, such
  that candidate module-level code cannot mutate the scorer's `unittest` objects,
  result class, or runner; and the scorer's own `os.environ` is unchanged after a
  scoring run (currently mutated globally at L73–100).
- [outcome] 3. `bash scripts/eval-agent-code-quality-selftest.sh` exits 0 — every task's
  reference still scores 1.0 and every starter still scores strictly below its
  reference (no regression from the isolation change).
- [outcome] 4. A solution that is otherwise perfect and additionally emits
  `ratings.jsonl` and `verify_adhoc.py` reports `scope_ok true` and retains its
  non-zero `primary_code_score`; the scope policy (what is allowed and why) is stated
  in a comment or doc next to the rule.
- [outcome] 5. The reproducer from criterion 1 is committed as a regression fixture
  under `core/evals/` and is exercised by the selftest (or an adjacent script wired
  into `scripts/verify.sh`), so the bypass cannot silently return.
- [guardrail] 6. No changes to any `tasks/*/hidden_tests/`, `tasks/*/reference/`, or
  `tasks/*/starter/` content — the fix is in the scorer, not in what it scores.
- [guardrail] 7. `bash scripts/verify.sh` exits 0, and package-mode (L119–141, used by
  the L2 tool-using tasks) still scores at least one existing package-mode task
  unchanged versus its pre-change score.
- [hypothesis] 8. Implementation runs `python -m unittest` (or a small runner script) in
  a `subprocess` against the temp dir, parsing counts from machine-readable output
  rather than sharing objects. The implementer may choose another isolation mechanism
  that satisfies criteria 1–3.

**Anti-gaming (non-binding review question):** Does the change make scores *trustworthy*,
or merely defeat the one reproducer in criterion 1? A fix that special-cases this exact
monkeypatch while leaving in-process execution intact satisfies the literal checklist and
fails the objective. Criterion 2 is the real bar; criterion 1 is only its witness.

## Ontology / Domain Model (optional)

Not in use.

## Out of scope

- Sandboxing untrusted code in a security sense (resource limits, syscall filtering).
  This is a local eval harness for solutions the operator solicited; process isolation
  for *integrity* is the goal, not defense against hostile code.
- Re-running or re-scoring historical campaigns. **But note the consequence:** fixing
  defect 2 changes how past GXP-arm trials would score, so recorded outcomes (notably
  the 2026-07-13 blind campaign FAIL) may no longer reflect what the fixed harness
  would produce. Flagged as a **recommended follow-up**, not silently absorbed here.
- Broadening the eval task set, or the `score_brief` process-scoring heuristic.
- The `no_test_tamper` hash including `__pycache__` (review finding F6, cosmetic).

## Verification plan

Deterministic first:

1. **C1** — run the committed reproducer through the scorer; assert `correctness ≤ 0.1`
   and non-success. Record before/after JSON in the handoff.
2. **C2** — inspect that no code path executes candidate modules in-process; assert
   `os.environ` identical before/after a scoring run; confirm a candidate that patches
   `unittest` internals has no effect on the reported counts.
3. **C3** — `bash scripts/eval-agent-code-quality-selftest.sh` → exit 0, with the
   per-task `starter=… reference=…` lines shown.
4. **C4** — construct reference + `ratings.jsonl` + `verify_adhoc.py` in a temp dir,
   score it, assert `scope_ok true` and `primary_code_score` equal to `correctness`.
5. **C5** — remove the isolation fix locally, confirm the regression fixture *fails*,
   restore, confirm it passes (the fixture must bite).
6. **C6/C7** — `git diff --stat` shows no `tasks/**` content changes;
   `bash scripts/verify.sh` → exit 0; one package-mode task scored before and after with
   matching results.

Behavioral: none beyond the above (the artifact under test is itself a test harness).
Subjective: confirm the scope-policy comment reads clearly for a future contributor.

## Self-evaluation gate

- [x] **Completeness** — covers the forgery hole, the false-penalty rule, non-regression,
  and a fixture so it cannot silently return. The consequence for past campaign numbers
  is named rather than buried.
- [x] **Ambiguity** — every binding criterion is a score threshold, an exit code, a diff,
  or an equality assertion.
- [x] **Scope trap** — sandboxing, task-set growth, and campaign re-scoring are all
  explicitly parked.
- [x] **Verification** — each binding criterion has a concrete check; criteria 1 and 5
  are proven by induced failure, not merely by a green run.
- [x] **Approval gates** — no destructive or outward-facing step; changes are local and
  reversible. Brief approval is the gate.
- [x] **Criteria quality** — 1–5 are outcomes, 6–7 guardrails, 8 an explicit
  non-binding mechanism hypothesis. Criterion 2 states the property, not the
  implementation, so an alternative isolation approach is not blocked.
- [x] **Anti-gaming** — answered above; the stated risk is defeating the reproducer
  without fixing the class, which criterion 2 exists to prevent.
- [x] **Ontology (if used)** — n/a.

## Approval gates

- **Gate 1 — brief approval** before implementation.
- **Gate 2 — before any public claim is revised.** If the implementer's before/after
  numbers suggest a past campaign outcome would flip, stop and surface it; changing
  published evidence claims is the operator's call, not part of this task.

## Dead ends

- (none yet)

## Handoff notes

To fill in at the end:

- What changed:
- What was verified (and how):
- Explicitly not done / parked / follow-ups:
- Approval gates hit and outcomes:
- New `failures/` entries or rules:
- Rating entry reference:
