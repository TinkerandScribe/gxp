# Containment checklist (opt-in)

**Status:** opt-in methodology note.  
**Use when:** the run is high-stakes, uses the network, or writes to a product repo.  
**Skip when:** the task is a lightweight typo, comment, or one-line fix.

This checklist is a pre-approval walk for those higher-stakes runs. It is
not a gate for lightweight tasks. GXP records the asks below. It does not
install host sandboxes, and it does not currently enforce eBPF or AppArmor.

Walk it from Phase 0 or an approval gate in `core/workflow.md`. One link
there is enough. Stop at the approval gate until the operator accepts the
residual items the platform cannot enforce.

## Sources

- OpenAI, “Toward safety cases for frontier AI training”:
  <https://openai.com/index/towards-safety-cases-for-frontier-ai-training/>
- DeepSeek Elastic Compute / DSec (AppArmor policies and per-sandbox eBPF
  network allowlists): <https://arxiv.org/abs/2609.22978>
- Approval bound to the exact bytes that will run (separation of duties):
  <https://arxiv.org/abs/2609.38224>

## Checks

- [ ] **No monitor, no run (aspirational / platform).** Privileged work
      (shell, network, product writes) starts only when monitoring and a
      pause path are enabled. Disabling the monitor from inside the run is
      out of bounds. Where the host cannot enforce this, name the gap and
      get a human gate before the run. GXP’s workflow text cannot block a
      cloud agent by itself.
- [ ] **Immutable or append-only logs.** Ratings and experience-memory
      ledgers stay append-only (`fleet/README.md`: `ratings.jsonl`,
      `em-records.jsonl`). Corrections are new lines. Prefer write-once or
      append-only storage for privileged-run transcripts when the platform
      offers it. Do not rewrite shared ledger history.
- [ ] **Incident → regression.** A repeatable failure capture names or
      links a matching regression check (`core/failures/README.md`,
      `fleet/README.md`). New `failures/*.md` for an incident class ships
      with `regressions/*.md` for that same class.
- [ ] **Egress allowlist ask.** Before a networked run, name the hosts,
      ports, and protocols the job needs. Ask the platform for an allowlist
      (cached or mirrored fetches where live internet is unnecessary). If
      the host cannot filter egress, record that and pause for a human
      gate on any live-network step.
- [ ] **AppArmor / eBPF-equivalent (platform if available).** When the
      sandbox offers file, socket, or packet controls — AppArmor-style
      policy or per-sandbox eBPF allowlists, as in DSec — ask the operator
      to turn them on for that run. Record “platform does not provide
      this” when it does not. This checklist does not claim GXP enforces
      eBPF or AppArmor today.

## Residual

Items the platform cannot enforce stay on the approval card. Proceed only
after the operator accepts those residuals for this run.
