# GXP named workflows (Rhai)

Runnable Grok Build orchestrations for the Heavy path. These **complement** the
markdown recipes (`heavy-gxp.md`, `clarifier-then-heavy.md`); they do not replace
stable `core/workflow.md`.

| Script | Purpose |
|--------|---------|
| [`gxp-heavy-front-half.rhai`](gxp-heavy-front-half.rhai) | Optional experimental clarifier gate → researcher \|\| architect → plan handoff |
| [`gxp-layer2-verify.rhai`](gxp-layer2-verify.rhai) | One fail-closed verifier agent per Ideal State Criterion |

## Ownership split (non-negotiable)

| Slice | Owner |
|-------|--------|
| Research / architect / optional clarifier | **Workflow** |
| `/plan` approval, implement, rating, failures | **Parent GXP agent** |
| Layer-2 criterion fan-out | **Workflow** (optional) |

Workflows never implement product code and never auto-enable experimental-v0.

## Install

Default installer copies `*.rhai` from this directory to `~/.grok/workflows/`:

```powershell
.\install-grok-build.ps1 -Force
# or workflows only:
.\install-grok-build.ps1 -Force -SkipPersonas
```

```bash
bash install-grok-build.sh --force
```

Skip with `-SkipWorkflows` / `--skip-workflows`. Project-local alternative:

```text
cp adapters/grok-build/workflows/*.rhai <repo>/.grok/workflows/
```

## Run

```text
/workflow gxp-heavy-front-half
# args JSON example:
# { "goal": "…", "repo": ".", "context": "optional notes" }

# Experimental clarifier branch (operator flag only):
# { "goal": "…", "clarification_protocol": "experimental-v0" }

/workflow gxp-layer2-verify
# { "goal": "…", "criteria": ["[outcome] …", "[guardrail] …"], "repo": "." }
```

Or invoke by name after install (`/gxp-heavy-front-half` when registered).

## Routing rule

```text
lightweight / sequential implement:
  → parent GXP only (no workflow)

underspecified / multi-constraint, flag OFF:
  → optional gxp-heavy-front-half

underspecified / multi-constraint + clarification_protocol: experimental-v0:
  → same workflow with experimental gate (max 2 FAIL → await_user)

after approved plan + implement:
  → optional gxp-layer2-verify with plan.criteria

always:
  → parent owns rating + failure capture
  → never auto-enable experimental-v0
```

## Smoke check limits

`validate_only` compiles the script and walks one canned-host path. It does not
prove live persona quality, every branch, or real tool evidence. Prefer a real
run after install when changing prompts.
