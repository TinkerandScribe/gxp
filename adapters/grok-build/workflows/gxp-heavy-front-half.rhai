// GXP Heavy front-half orchestration for Grok Build.
// Returns a structured plan artifact. Parent GXP owns /plan approval,
// implement, rating, and failure capture — this script never implements.
//
// Args:
//   goal (string, required) — operator goal
//   repo (string, optional) — path/context for research (e.g. ".")
//   context (string, optional) — extra scoped notes (files, constraints)
//   clarification_protocol (string, optional) — "experimental-v0" enables
//     isolated criteria maker-checker before research/architect.
//     Default / omit / "off" = standard Heavy only. Never auto-enable.

let meta = #{
    name: "gxp-heavy-front-half",
    description: "GXP Heavy front-half: optional experimental clarifier gate, then researcher || architect, then structured plan handoff (no implement)",
    when_to_use: "High-ambiguity or multi-constraint work before /plan; set clarification_protocol=experimental-v0 only when the operator opts in",
    phases: [
        #{ title: "Clarify", detail: "optional experimental-v0 brief + isolated checker" },
        #{ title: "Research", detail: "gxp-researcher || gxp-architect" },
        #{ title: "Synthesize", detail: "merge into one GXP plan object" },
        #{ title: "Handoff", detail: "return plan; parent owns /plan implement rate" },
    ],
};

let brief_schema = #{
    "type": "object",
    "required": ["goal", "criteria", "out_of_scope", "verification_plan"],
    "properties": #{
        "goal": #{ "type": "string" },
        "criteria": #{
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": #{ "type": "string" },
        },
        "out_of_scope": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "verification_plan": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "phase0_files": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "notes": #{ "type": "string" },
    },
};

let checker_schema = #{
    "type": "object",
    "required": ["verdict", "reason"],
    "properties": #{
        "verdict": #{ "type": "string" },
        "reason": #{ "type": "string" },
        "rewrites": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "per_criterion": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
    },
};

let research_schema = #{
    "type": "object",
    "required": ["goal_restatement", "findings", "uncertainty", "candidate_criteria"],
    "properties": #{
        "goal_restatement": #{ "type": "string" },
        "findings": #{
            "type": "array",
            "maxItems": 16,
            "items": #{ "type": "string" },
        },
        "uncertainty": #{
            "type": "array",
            "maxItems": 12,
            "items": #{ "type": "string" },
        },
        "candidate_criteria": #{
            "type": "array",
            "maxItems": 8,
            "items": #{ "type": "string" },
        },
        "phase0_files": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "out_of_scope_candidates": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "risks": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
    },
};

let plan_schema = #{
    "type": "object",
    "required": ["goal", "criteria", "out_of_scope", "verification_plan"],
    "properties": #{
        "goal": #{ "type": "string" },
        "criteria": #{
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": #{ "type": "string" },
        },
        "out_of_scope": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "verification_plan": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "phase0_files": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "approach": #{ "type": "string" },
        "residual_uncertainty": #{
            "type": "array",
            "items": #{ "type": "string" },
        },
        "scaffolding_tier": #{ "type": "string" },
    },
};

fn as_str(x) {
    if x == () { "" } else if type_of(x) == "string" { x } else { "" }
}

fn protocol_is_experimental(proto) {
    let p = as_str(proto);
    p == "experimental-v0" || p == "experimental_v0" || p == "experimental"
}

// --- args ---
let goal = if args == () { () } else { args.goal };
if goal == () || as_str(goal) == "" {
    pause("verification", "Pass args.goal (string) — the operator goal for the GXP Heavy front-half.");
}
let goal_s = as_str(goal);
let goal_q = json_encode(goal_s);

let repo = if args == () { () } else { args.repo };
let repo_s = as_str(repo);
if repo_s == "" { repo_s = "."; }
let repo_q = json_encode(repo_s);

let extra = if args == () { () } else { args.context };
let extra_s = as_str(extra);
let extra_q = json_encode(extra_s);

let proto = if args == () { () } else { args.clarification_protocol };
let use_exp = protocol_is_experimental(proto);

let seed_brief = #{
    goal: goal_s,
    criteria: [],
    out_of_scope: [],
    verification_plan: [],
    phase0_files: [],
    notes: "",
};
let clarification_history = [];
let checker_iterations = 0;

// ========== optional experimental clarifier gate ==========
if use_exp {
    phase("Clarify");
    log("experimental-v0 clarifier gate active (operator flag required path)");

    let attempt = 0;
    let passed = false;
    let rewrite_hints = "";

    while attempt < 2 && !passed {
        attempt += 1;
        checker_iterations = attempt;
        log("clarifier attempt " + attempt.to_string() + "/2");

        let clar_prompt = "";
        clar_prompt += "You are a GXP Clarifier (Experimental Clarification Protocol v0).\n";
        clar_prompt += "Draft a GXP brief ONLY. Do NOT implement product code. Do NOT deep-research the whole repo.\n";
        clar_prompt += "You may use read-only tools lightly (PROGRAM.md, rules/, failures/, AGENTS.md) if helpful.\n\n";
        clar_prompt += "Operator goal (JSON): " + goal_q + "\n";
        clar_prompt += "Repo path (JSON): " + repo_q + "\n";
        clar_prompt += "Extra context (JSON): " + extra_q + "\n";
        if rewrite_hints != "" {
            clar_prompt += "\nPrevious checker rewrites to address:\n" + rewrite_hints + "\n";
        }
        clar_prompt += "\nReturn JSON matching the schema:\n";
        clar_prompt += "- goal: one sentence\n";
        clar_prompt += "- criteria: 4-8 binary Ideal State Criteria strings (tag [outcome]/[guardrail]/[hypothesis] when useful)\n";
        clar_prompt += "- out_of_scope: explicit list\n";
        clar_prompt += "- verification_plan: named checks/commands per criterion or group\n";
        clar_prompt += "- phase0_files: files parent should open\n";
        clar_prompt += "- notes: short residual ambiguity only\n";
        clar_prompt += "Mark mentally: clarification_protocol experimental-v0. Do not invent scope beyond the goal.\n";

        let clar = agent(clar_prompt, #{
            label: "clarifier:" + attempt.to_string(),
            capability_mode: "read-only",
            output_schema: brief_schema,
        });

        if clar == () || !clar.success || clar.output == () {
            log("clarifier agent failed or empty; treating as FAIL for this attempt");
            rewrite_hints = "Clarifier returned no usable brief. Re-draft Goal + 4-8 binary criteria + out_of_scope + verification_plan.";
            clarification_history.push("attempt " + attempt.to_string() + ": clarifier failed");
            continue;
        }

        seed_brief = clar.output;
        // Isolated checker: ONLY brief artifacts — never proposer CoT.
        let brief_payload = #{
            goal: seed_brief.goal,
            criteria: seed_brief.criteria,
            out_of_scope: seed_brief.out_of_scope,
            verification_plan: seed_brief.verification_plan,
        };
        let brief_q = json_encode(brief_payload);

        let chk_prompt = "";
        chk_prompt += "You are the GXP Criteria Checker (Experimental Clarification Protocol v0).\n";
        chk_prompt += "You receive ONLY the brief artifacts below — no proposer chain-of-thought.\n";
        chk_prompt += "Do NOT implement. Do NOT invent new criteria. Do NOT expand scope.\n\n";
        chk_prompt += "Brief artifacts (JSON):\n" + brief_q + "\n\n";
        chk_prompt += "Evaluate binarity, completeness vs goal, ambiguity, scope fidelity, verifiability.\n";
        chk_prompt += "Return JSON: verdict must be exactly PASS or FAIL (uppercase); reason; optional rewrites[]; optional per_criterion[].\n";
        chk_prompt += "If fewer than 4 strong binary criteria: verdict=FAIL.\n";

        let chk = agent(chk_prompt, #{
            label: "criteria-checker:" + attempt.to_string(),
            capability_mode: "read-only",
            output_schema: checker_schema,
        });

        if chk == () || !chk.success || chk.output == () {
            log("criteria-checker failed or empty; fail-closed as FAIL");
            rewrite_hints = "Checker produced no verdict. Strengthen binary criteria and verification plan.";
            clarification_history.push("attempt " + attempt.to_string() + ": checker failed");
            continue;
        }

        let verdict = as_str(chk.output.verdict);
        // normalize simple variants without regex
        if verdict == "pass" || verdict == "Pass" || verdict == "PASS" {
            passed = true;
            clarification_history.push("attempt " + attempt.to_string() + ": PASS — " + as_str(chk.output.reason));
            log("criteria-checker PASS");
        } else {
            let rewrites = chk.output.rewrites;
            rewrite_hints = as_str(chk.output.reason);
            if rewrites != () {
                let i = 0;
                while i < rewrites.len() {
                    rewrite_hints += "\n- " + as_str(rewrites[i]);
                    i += 1;
                }
            }
            clarification_history.push("attempt " + attempt.to_string() + ": FAIL — " + as_str(chk.output.reason));
            log("criteria-checker FAIL: " + as_str(chk.output.reason));
        }
    }

    if !passed {
        let hist = "";
        let hi = 0;
        while hi < clarification_history.len() {
            hist += "- " + as_str(clarification_history[hi]) + "\n";
            hi += 1;
        }
        let esc = write_scratch_file("clarification_history.md", "# Clarification history (escalated)\n\n" + hist);
        await_user(
            "verification",
            "Experimental clarifier failed after 2 checker rounds. Review scratch " + as_str(esc)
                + " and the last brief draft, then resume to continue into Heavy research with best-effort draft,"
                + " or stop the run and rewrite the operator goal / criteria by hand."
        );
        log("operator resumed after clarifier escalate; continuing Heavy with best-effort draft");
    }
} else {
    log("clarification_protocol off — standard Heavy front-half");
}

// ========== research || architect ==========
phase("Research");

let research_prompt = "";
research_prompt += "You are a GXP research specialist (gxp-researcher role).\n";
research_prompt += "Use read-only tools aggressively (read_file, grep, list_dir). Do NOT implement product code.\n";
research_prompt += "Prefer evidence from PROGRAM.md / .ai/PROGRAM.md, rules/, failures/, AGENTS.md, tests.\n";
research_prompt += "An empty findings list is valid ONLY after you have actually inspected the repo.\n\n";
research_prompt += "Operator goal (JSON): " + goal_q + "\n";
research_prompt += "Repo path (JSON): " + repo_q + "\n";
research_prompt += "Extra context (JSON): " + extra_q + "\n";
if use_exp {
    research_prompt += "Seed brief after clarifier (JSON): " + json_encode(seed_brief) + "\n";
}
research_prompt += "\nReturn JSON: goal_restatement, findings[], uncertainty[], candidate_criteria[] (4-8 binary),";
research_prompt += " phase0_files[], out_of_scope_candidates[], risks[].\n";

let architect_prompt = "";
architect_prompt += "You are a GXP architect / planner (gxp-architect role).\n";
architect_prompt += "Use read-only tools as needed. Do NOT implement product code.\n";
architect_prompt += "Produce a tight GXP-shaped plan draft (criteria must be binary and checkable).\n";
architect_prompt += "Thin public/smoke green is not enough alone on multi-factor work — name edge checks.\n\n";
architect_prompt += "Operator goal (JSON): " + goal_q + "\n";
architect_prompt += "Repo path (JSON): " + repo_q + "\n";
architect_prompt += "Extra context (JSON): " + extra_q + "\n";
if use_exp {
    architect_prompt += "Seed brief after clarifier (JSON): " + json_encode(seed_brief) + "\n";
}
architect_prompt += "\nReturn JSON plan: goal, criteria[] (4-8), out_of_scope[], verification_plan[],";
architect_prompt += " phase0_files[], approach, residual_uncertainty[], scaffolding_tier (usually \"standard\").\n";

let panel = parallel([
    #{
        prompt: research_prompt,
        label: "gxp-researcher",
        capability_mode: "read-only",
        output_schema: research_schema,
    },
    #{
        prompt: architect_prompt,
        label: "gxp-architect",
        capability_mode: "read-only",
        output_schema: plan_schema,
    },
]);

let research_out = ();
let architect_out = ();
if panel.len() > 0 && panel[0] != () && panel[0].success {
    research_out = panel[0].output;
}
if panel.len() > 1 && panel[1] != () && panel[1].success {
    architect_out = panel[1].output;
}

if research_out == () && architect_out == () {
    pause(
        "verification",
        "Both researcher and architect failed or returned empty. Resume after fixing repo access / budget, or stop and run personas manually."
    );
}

// ========== synthesize ==========
phase("Synthesize");

let syn_prompt = "";
syn_prompt += "You are the GXP parent synthesizer. Merge research + architect drafts into ONE coherent GXP plan.\n";
syn_prompt += "Do NOT implement. Prefer binary Ideal State Criteria (4-8). Keep out_of_scope tight.\n";
syn_prompt += "Do not expand beyond the operator goal. Prefer tool-backed verification steps.\n\n";
syn_prompt += "Operator goal (JSON): " + goal_q + "\n";
syn_prompt += "Research output (JSON): " + json_encode(research_out) + "\n";
syn_prompt += "Architect output (JSON): " + json_encode(architect_out) + "\n";
if use_exp {
    syn_prompt += "Clarifier seed brief (JSON): " + json_encode(seed_brief) + "\n";
}
syn_prompt += "\nReturn the final plan JSON: goal, criteria[], out_of_scope[], verification_plan[],";
syn_prompt += " phase0_files[], approach, residual_uncertainty[], scaffolding_tier.\n";

let syn = agent(syn_prompt, #{
    label: "gxp-synthesize",
    capability_mode: "read-only",
    output_schema: plan_schema,
});

let final_plan = ();
if syn != () && syn.success && syn.output != () {
    final_plan = syn.output;
} else if architect_out != () {
    log("synthesizer failed; falling back to architect draft");
    final_plan = architect_out;
} else if use_exp {
    log("synthesizer+architect failed; falling back to clarifier seed");
    final_plan = #{
        goal: seed_brief.goal,
        criteria: seed_brief.criteria,
        out_of_scope: seed_brief.out_of_scope,
        verification_plan: seed_brief.verification_plan,
        phase0_files: seed_brief.phase0_files,
        approach: "fallback from clarifier seed only",
        residual_uncertainty: ["synthesizer failed — parent must re-validate criteria"],
        scaffolding_tier: "standard",
    };
} else {
    pause("verification", "No usable plan object after synthesize. Resume or re-run with a clearer args.goal.");
}

// ========== handoff ==========
phase("Handoff");

let report = "";
report += "# GXP Heavy front-half result\n\n";
report += "**clarification_protocol:** " + (if use_exp { "experimental-v0" } else { "off" }) + "\n";
report += "**checker_iterations:** " + checker_iterations.to_string() + "\n\n";
report += "Parent must: (1) present via `/plan` or brief for operator approval, ";
report += "(2) implement only after approval, (3) Layer-2 verify, (4) rate + capture failures.\n";
report += "This workflow does **not** implement product code.\n\n";
report += "## Plan (JSON)\n\n```json\n" + json_encode(final_plan) + "\n```\n";

if clarification_history.len() > 0 {
    report += "\n## Clarification history\n\n";
    let hi2 = 0;
    while hi2 < clarification_history.len() {
        report += "- " + as_str(clarification_history[hi2]) + "\n";
        hi2 += 1;
    }
}

let report_path = write_scratch_file("gxp_heavy_plan.md", report);
log("plan ready for parent /plan — scratch " + as_str(report_path));

complete(#{
    summary: "GXP Heavy front-half complete — parent owns /plan, implement, rate",
    clarification_protocol: if use_exp { "experimental-v0" } else { "off" },
    checker_iterations: checker_iterations,
    plan: final_plan,
    report_path: report_path,
    next_steps: [
        "Parent synthesizes operator-facing brief if needed",
        "Operator approves via /plan (or explicit proceed)",
        "Implement (composer-coder worktree or parent) — smallest viable change",
        "Optional: run workflow gxp-layer2-verify with args.criteria from plan",
        "Parent honest rating + failure capture",
    ],
});
