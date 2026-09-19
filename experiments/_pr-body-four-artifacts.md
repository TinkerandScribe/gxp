## Summary
- Optional named artifacts (System Prompt, Rule Bank, Safety Memory, Tool Policy) plus a named-inverse rule and a Phase 5 binary brief-walk.
- Phase 0: unfilled core/templates do not count as present. Lightweight lookups skip the pack unless the brief is a live product tree, a handoff, or child/security data.
- Tool Policy stub: live product trees are read-only unless the brief names writes; no exploit-chain retry; vuln-shaped findings go to a human.
- Base is feat/grok-bot-adapter (#25) so this PR is only the two experiment commits, not the adapter itself.

## Test plan
- [ ] scripts/verify.sh exit 0
- [ ] Phase 0 names filled .ai / ~/.gxp copies only
- [ ] Phrase "full undo" is absent
- [ ] grok-bot cursor-handoff.md lists the three rules
- [ ] Do not merge until #25 is ready or this is retargeted to main
