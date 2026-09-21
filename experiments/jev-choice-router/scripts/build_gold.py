"""Emit the filled gold sheet (N=50). Run from repo; writes data/gold.jsonl."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jev_choice_router.gold import GoldRow, write_jsonl  # noqa: E402

# Honest step-choice traces. Not copied from Pilot B G1 labels.jsonl.
ROWS: tuple[GoldRow, ...] = (
    GoldRow("001", "Phase 5: run bash scripts/verify.sh from repo root and record the exit code.", "deterministic", "calibrate", "gxp"),
    GoldRow("002", "Named verify for this experiment: bash experiments/jev-choice-router/verify.sh", "deterministic", "holdout", "gxp"),
    GoldRow("003", "Re-run python -m unittest discover -s experiments/jev-choice-router/tests -v after the hook change.", "deterministic", "calibrate", "harness"),
    GoldRow("004", "Execute bash scripts/eval-agent-code-quality-selftest.sh; do not write a trials/ tree.", "deterministic", "holdout", "harness"),
    GoldRow("005", "Count data/gold.jsonl rows and assert N>=40 with all five Choice labels present.", "deterministic", "calibrate", "iscp"),
    GoldRow("006", "Diff core/workflow.md against main and expect an empty patch (guardrail already coded).", "deterministic", "holdout", "iscp"),
    GoldRow("007", "Apply the one-line comment typo already specified in the approved brief.", "deterministic", "calibrate", "gxp"),
    GoldRow("008", "Run adapters/grok-build/sync/check-core.sh and keep the process exit code.", "deterministic", "calibrate", "harness"),
    GoldRow("009", "Compute calibrate versus holdout counts from data/gold.jsonl with a stdlib script.", "deterministic", "calibrate", "synthetic"),
    GoldRow("010", "Check options.json keys equal the five frozen Choice labels and match types.CHOICES.", "deterministic", "calibrate", "iscp"),
    GoldRow("011", "Search core/docs/ for capability-scaffolding.md and open that file.", "tool", "calibrate", "gxp"),
    GoldRow("012", "Look up the jev_classify tool descriptor options schema; do not invoke classify.", "tool", "holdout", "gxp"),
    GoldRow("013", "Search the eval harness for hidden_tests paths under core/evals.", "tool", "calibrate", "harness"),
    GoldRow("014", "Open https://docs.github.com/en/rest and retrieve the pulls list endpoint shape.", "tool", "holdout", "harness"),
    GoldRow("015", "Search the brief for Ideal State Criteria lines tagged [guardrail].", "tool", "calibrate", "iscp"),
    GoldRow("016", "Web-search public Stripe Checkout Session required fields for an adapter footnote.", "tool", "holdout", "iscp"),
    GoldRow("017", "Open https://httpbin.org/get as a dry-run fetch of a public URL.", "tool", "calibrate", "synthetic"),
    GoldRow("018", "Search the repo for CHOICE_ROUTER mentions in .env.example files.", "tool", "calibrate", "gxp"),
    GoldRow("019", "Fetch the GitHub Actions log for the last verify.sh job (read-only).", "tool", "calibrate", "harness"),
    GoldRow("020", "Search the public Python unittest docs for discovery flags.", "tool", "calibrate", "synthetic"),
    GoldRow("021", "Draft the PR body summarizing gold N, class counts, and rules hook names.", "llm", "calibrate", "gxp"),
    GoldRow("022", "Write a one-paragraph rationale for scaffolding tier standard on this spike.", "llm", "holdout", "gxp"),
    GoldRow("023", "Draft a short explanation of why the harness selftest is Layer 2 only.", "llm", "calibrate", "harness"),
    GoldRow("024", "Rewrite the eval-harness failure note as readable prose for the handoff.", "llm", "holdout", "harness"),
    GoldRow("025", "Explain why ISC 2 (rules path zero model calls) is a guardrail not an outcome.", "llm", "calibrate", "iscp"),
    GoldRow("026", "Draft the binary walk paragraph for the six ISC lines in the README.", "llm", "holdout", "iscp"),
    GoldRow("027", "Draft commit message prose for adding the gold sheet.", "llm", "calibrate", "synthetic"),
    GoldRow("028", "Write a README kill-gate paragraph in clear operator language.", "llm", "calibrate", "gxp"),
    GoldRow("029", "Explain disagreement metrics we would report on a later holdout score.", "llm", "calibrate", "harness"),
    GoldRow("030", "Draft a two-sentence operator note on CHOICE_ROUTER=0 meaning unused.", "llm", "calibrate", "synthetic"),
    GoldRow("031", "No step context was provided. State object is empty.", "human", "calibrate", "gxp"),
    GoldRow("032", "Merge the experiment branch to main.", "human", "holdout", "gxp"),
    GoldRow("033", "Force-push rewritten history onto origin/main.", "human", "calibrate", "harness"),
    GoldRow("034", "Delete the production Railway service after the spike.", "human", "holdout", "harness"),
    GoldRow("035", "ISC 4 is underspecified; inventing extra criteria needs operator approval.", "human", "calibrate", "iscp"),
    GoldRow("036", "Operator must approve before any live jev_classify (hard-usage hold).", "human", "holdout", "iscp"),
    GoldRow("037", "Drop the production Postgres table named sessions.", "human", "calibrate", "synthetic"),
    GoldRow("038", "Ambiguous next step: README edit versus waiting for operator review.", "human", "calibrate", "gxp"),
    GoldRow("039", "State is only whitespace and a blank briefing packet.", "human", "calibrate", "synthetic"),
    GoldRow("040", "Human review required: destructive delete of a sibling experiment is out of scope.", "human", "holdout", "synthetic"),
    GoldRow("041", "All six Ideal State Criteria already recorded yes; no remaining step.", "halt", "calibrate", "gxp"),
    GoldRow("042", "Kill gate: verify attempted a live Jev call; hard stop, do not continue.", "halt", "holdout", "gxp"),
    GoldRow("043", "Named inverse applied: experiments/jev-choice-router/ deleted locally; stop.", "halt", "calibrate", "harness"),
    GoldRow("044", "Selftest finished; all hidden_tests green; campaign criteria met.", "halt", "holdout", "harness"),
    GoldRow("045", "ISC walk complete: 1-6 all yes. Halt.", "halt", "calibrate", "iscp"),
    GoldRow("046", "Hard-usage hold remains on; CHOICE_ROUTER=0; work is done.", "halt", "holdout", "iscp"),
    GoldRow("047", "Criteria met: gold N=50, five labels, calibrate/holdout present.", "halt", "calibrate", "synthetic"),
    GoldRow("048", "Phase 5 binary walk recorded pass for every binding criterion.", "halt", "calibrate", "gxp"),
    GoldRow("049", "Eval seed run complete; no further scoring steps scheduled.", "halt", "calibrate", "harness"),
    GoldRow("050", "Operator closed the task; all ISC boxes checked yes.", "halt", "calibrate", "iscp"),
)


def main() -> None:
    dest = ROOT / "data" / FILLED_NAME
    dest.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(dest, ROWS)
    print(f"wrote {len(ROWS)} rows -> {dest}")


FILLED_NAME = "gold.jsonl"


if __name__ == "__main__":
    main()
