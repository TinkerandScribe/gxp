// GXP Layer-2 verification fan-out for Grok Build.
// Walks each Ideal State Criterion with an independent read-only agent.
// Fail-closed: missing/failed agent slots are NOT counted as PASS.
// Parent owns overall GO/NO-GO acceptance, ratings, and failure capture.
//
// Args:
//   criteria (array of strings, required) — Ideal State Criteria to check
//   goal (string, optional)
//   repo (string, optional) — default "."
//   context (string, optional) — paths, commands, notes for verifiers

let meta = #{
    name: "gxp-layer2-verify",
    description: "GXP Layer-2: one read-only verifier agent per Ideal State Criterion; fail-closed; no product edits",
    when_to_use: "After implementation, when smoke is thin or multi-constraint criteria need independent tool-backed checks",
    phases: [
        #{ title: "Verify", detail: "parallel criterion checks" },
        #{ title: "Summarize", detail: "aggregate PASS/FAIL/UNKNOWN fail-closed" },
    ],
};

let criterion_schema = #{
    "type": "object",
    "required": ["criterion", "result", "check", "evidence"],
    "properties": #{
        "criterion": #{ "type": "string" },
        "result": #{ "type": "string" },
        "check": #{ "type": "string" },
        "evidence": #{ "type": "string" },
        "notes": #{ "type": "string" },
    },
};

fn as_str(x) {
    if x == () { "" } else if type_of(x) == "string" { x } else { "" }
}

fn is_pass(s) {
    let v = as_str(s);
    v == "PASS" || v == "pass" || v == "Pass"
}

// --- args ---
let criteria = if args == () { () } else { args.criteria };
if criteria == () {
    pause("verification", "Pass args.criteria as an array of Ideal State Criterion strings (from the approved plan).");
}
if type_of(criteria) != "array" {
    pause("verification", "args.criteria must be an array of strings.");
}
if criteria.len() == 0 {
    pause("verification", "args.criteria is empty — no Ideal State Criteria to verify.");
}

const MAX_CRITERIA = 8;
let work = [];
let i = 0;
while i < criteria.len() && i < MAX_CRITERIA {
    work.push(criteria[i]);
    i += 1;
}
if criteria.len() > MAX_CRITERIA {
    log("truncated: " + (criteria.len() - MAX_CRITERIA).to_string()
        + " criteria beyond cap " + MAX_CRITERIA.to_string()
        + " — parent must verify remainder");
}

let goal = if args == () { () } else { args.goal };
let goal_s = as_str(goal);
let goal_q = json_encode(goal_s);

let repo = if args == () { () } else { args.repo };
let repo_s = as_str(repo);
if repo_s == "" { repo_s = "."; }
let repo_q = json_encode(repo_s);

let extra = if args == () { () } else { args.context };
let extra_s = as_str(extra);
let extra_q = json_encode(extra_s);

phase("Verify");

let jobs = [];
let j = 0;
while j < work.len() {
    let c = work[j];
    let c_s = as_str(c);
    let c_q = json_encode(c_s);
    let prompt = "";
    prompt += "You are a GXP Layer-2 verification critic (gxp-verifier role).\n";
    prompt += "You do NOT edit product code. Use read-only tools and/or execute tests/linters only as checks.\n";
    prompt += "Set result=PASS only with concrete evidence you independently inspected.\n";
    prompt += "If you cannot check, result=UNKNOWN (not PASS). Prefer FAIL over optimistic PASS.\n";
    prompt += "Empty evidence is not allowed for PASS.\n\n";
    prompt += "Goal (JSON): " + goal_q + "\n";
    prompt += "Repo path (JSON): " + repo_q + "\n";
    prompt += "Context (JSON): " + extra_q + "\n";
    prompt += "Single Ideal State Criterion to check (JSON): " + c_q + "\n\n";
    prompt += "Return JSON: criterion, result (PASS|FAIL|UNKNOWN), check (command or tool used), evidence, notes.\n";

    jobs.push(#{
        prompt: prompt,
        label: "verify:" + j.to_string(),
        capability_mode: "read-only",
        output_schema: criterion_schema,
    });
    j += 1;
}

let results = parallel(jobs);

phase("Summarize");

let rows = [];
let pass_n = 0;
let fail_n = 0;
let unknown_n = 0;
let k = 0;
while k < work.len() {
    let crit = as_str(work[k]);
    let slot = if k < results.len() { results[k] } else { () };
    if slot == () || !slot.success || slot.output == () {
        // fail-closed: missing agent is not a pass
        unknown_n += 1;
        rows.push(#{
            criterion: crit,
            result: "UNKNOWN",
            check: "",
            evidence: "verifier agent missing, failed, or returned empty (fail-closed)",
            notes: "not counted as PASS",
        });
    } else {
        let out = slot.output;
        let res = as_str(out.result);
        if is_pass(res) {
            let ev = as_str(out.evidence);
            if ev == "" {
                // evidence required for PASS
                unknown_n += 1;
                rows.push(#{
                    criterion: crit,
                    result: "UNKNOWN",
                    check: as_str(out.check),
                    evidence: "PASS claimed without evidence — demoted (fail-closed)",
                    notes: as_str(out.notes),
                });
            } else {
                pass_n += 1;
                rows.push(#{
                    criterion: crit,
                    result: "PASS",
                    check: as_str(out.check),
                    evidence: ev,
                    notes: as_str(out.notes),
                });
            }
        } else if res == "FAIL" || res == "fail" || res == "Fail" {
            fail_n += 1;
            rows.push(#{
                criterion: crit,
                result: "FAIL",
                check: as_str(out.check),
                evidence: as_str(out.evidence),
                notes: as_str(out.notes),
            });
        } else {
            unknown_n += 1;
            rows.push(#{
                criterion: crit,
                result: "UNKNOWN",
                check: as_str(out.check),
                evidence: as_str(out.evidence),
                notes: as_str(out.notes),
            });
        }
    }
    k += 1;
}

let total = work.len();
let overall = "NO-GO";
if fail_n == 0 && unknown_n == 0 && pass_n == total && total > 0 {
    overall = "GO";
} else if fail_n > 0 {
    overall = "NO-GO";
} else {
    overall = "NO-GO"; // unknowns remain
}

let report = "";
report += "# GXP Layer-2 verify\n\n";
report += "**overall:** " + overall + "\n";
report += "**PASS:** " + pass_n.to_string() + "  **FAIL:** " + fail_n.to_string()
    + "  **UNKNOWN:** " + unknown_n.to_string() + "  **checked:** " + total.to_string() + "\n\n";
report += "Fail-closed: missing agents and PASS-without-evidence are UNKNOWN, not PASS.\n";
report += "Parent owns final acceptance, ratings, and failure capture.\n\n";

let r = 0;
while r < rows.len() {
    let row = rows[r];
    report += "## [" + as_str(row.result) + "] " + as_str(row.criterion) + "\n";
    report += "- check: " + as_str(row.check) + "\n";
    report += "- evidence: " + as_str(row.evidence) + "\n";
    if as_str(row.notes) != "" {
        report += "- notes: " + as_str(row.notes) + "\n";
    }
    report += "\n";
    r += 1;
}

let report_path = write_scratch_file("gxp_layer2_verify.md", report);
log(overall + " — " + pass_n.to_string() + "/" + total.to_string()
    + " PASS (fail " + fail_n.to_string() + ", unknown " + unknown_n.to_string() + ")");

complete(#{
    summary: overall + " Layer-2: " + pass_n.to_string() + "/" + total.to_string() + " PASS",
    overall: overall,
    pass: pass_n,
    fail: fail_n,
    unknown: unknown_n,
    checked: total,
    criteria_truncated: criteria.len() > MAX_CRITERIA,
    results: rows,
    report_path: report_path,
});
