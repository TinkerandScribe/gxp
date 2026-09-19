# Coding-agent brief — thin the four-artifacts experiment

Existing checkout. Do not clone. Do not merge. Do not push. Do not open a PR.
Branch: experiment/four-artifacts-inverse @ 686ab8a (or current HEAD on that branch).
Repo: C:\Users\Reepicheep\Claude\gxp

## Goal
A/B showed empty System Prompt / Rule Bank / Safety Memory never helped. Tool Policy, named inverse, and Phase 5 binary walk did. Cheap lookups got worse when Phase 0 read unfilled templates.

Make the experiment match that: unfilled core/templates do not count as present. Keep Tool Policy stub filled. Leave the other three as empty templates.

## Out of scope
- SHE evolution loop, Cordis runtime
- Merging to main or feat/grok-bot-adapter
- CharlotteMasonGuide MediaRecorder (separate brief, do not touch that repo)
- Committing experiments/bower-ab-*.md or experiments/_handoff-* (leave untracked)
- New numbered phase

## Smallest change
1. core/workflow.md Phase 0: after the four-artifact bullet, one sentence:
   "If present" means a filled copy in the repo (e.g. .ai/system-prompt.md, .ai/tool-policy.md) or ~/.gxp/. Unfilled files under core/templates/ do not count. Lightweight / one-file lookups skip the pack.
2. core/workflow.md lightweight section (Full vs lightweight): lightweight (phases 1, 2, 3, 5) does not load the four artifacts unless the brief is a live product tree, a Phase 3 handoff, or child/security data.
3. core/templates/tool-policy.md.template: keep the live-tree read-only / no exploit-retry / human-for-vuln stub.
4. core/templates/system-prompt.md.template, rule-bank.md.template, safety-memory.md.template: keep as empty operator-owned stubs. Do not invent content.
5. If adapters/grok-bot/ exists on this branch, add three bullets to SKILL.md or instructions/cursor-handoff.md (whichever already lists constraints), not a fourth artifact file:
   - Load filled .ai / ~/.gxp artifacts only; skip unfilled core/templates.
   - Name an inverse for any plugin/MCP/skill/handoff or treat as irreversible.
   - Phase 5 records pass/fail per binding ISC before continuing.
6. If generate-adapter-workflows.py runs off workflow.md, run it; keep the delta to those sentences.
7. Append a short "thinning" note to experiments/four-artifacts-inverse.md (the protocol log). Do not add the Bower A/B logs.

## ISC
- [outcome] Phase 0 states unfilled core/templates do not count as present.
- [outcome] Lightweight skips the pack except live-tree / handoff / child-security.
- [guardrail] Tool Policy stub still names read-only live trees, no exploit retry, human for vuln-shaped findings.
- [guardrail] No new phase. Phase list still 0, 0.5, 1-8.
- [guardrail] Phrase "full undo" still absent.
- [guardrail] No merge, push, or PR.
- [guardrail] experiments/bower-ab-* stay untracked.
- [hypothesis] grok-bot handoff (if present) lists the three rules, not new files.

## Verify
1. git branch is still experiment/four-artifacts-inverse.
2. bash scripts/verify.sh (or Windows equivalent) exit 0.
3. Grep: unfilled / core/templates / if present sentence exists.
4. Grep: tool-policy still has read-only live product tree.
5. git status: no bower-ab files staged.

## Stop
Two same-shape failures then stop. Do not delete the four template files to "fix" Phase 0; clarify presence instead.
