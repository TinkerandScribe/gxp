#!/usr/bin/env python3
"""Generate adapter instructions/workflow.md from core/workflow.md + deltas.

Adapters: claude, chatgpt, grok, perplexity (text workflows).
Cursor rule.mdc and Cowork build remain hand-managed.

Usage (repo root):
  python scripts/generate-adapter-workflows.py           # write
  python scripts/generate-adapter-workflows.py --check   # fail if drift
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_WF = ROOT / "core" / "workflow.md"
ADAPTERS = ("claude", "chatgpt", "grok", "perplexity")

FRONT_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
MARKER_RE = re.compile(
    r"> \*\*Last synced from core:\*\*[^\n]*",
    re.I,
)


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2).lstrip("\n")


def split_md_sections(body: str) -> dict[str, str]:
    """Split on ## headings; key is heading text without ##."""
    parts = re.split(r"(?m)^(## .+)$", body)
    # parts[0] is preamble before first ##
    sections: dict[str, str] = {"_preamble": parts[0].strip()}
    i = 1
    while i < len(parts) - 1:
        heading = parts[i].lstrip("#").strip()
        content = parts[i + 1]
        # strip leading blank line after heading
        if content.startswith("\n"):
            content = content[1:]
        # trim trailing excess newlines but keep one
        sections[heading] = content.rstrip() + "\n"
        i += 2
    return sections


def core_sections() -> dict[str, str]:
    text = CORE_WF.read_text(encoding="utf-8")
    # Drop H1 title line
    text = re.sub(r"\A#[^\n]*\n+", "", text)
    return split_md_sections(text)


def existing_marker(adapter: str) -> str | None:
    path = (
        ROOT
        / "adapters"
        / adapter
        / "ai-workflow"
        / "instructions"
        / "workflow.md"
    )
    if not path.is_file():
        return None
    m = MARKER_RE.search(path.read_text(encoding="utf-8"))
    return m.group(0).strip() if m else None


def load_delta(adapter: str) -> tuple[dict, dict[str, str]]:
    path = (
        ROOT
        / "adapters"
        / adapter
        / "ai-workflow"
        / "deltas"
        / "workflow.delta.md"
    )
    if not path.is_file():
        raise SystemExit(f"Missing delta: {path}")
    meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
    return meta, split_md_sections(body)


def phase_note_key(heading: str) -> str | None:
    """Map core heading to optional delta note section name."""
    m = re.match(r"Phase (\d+(?:\.\d+)?)\b", heading)
    if not m:
        return None
    return f"Notes — Phase {m.group(1)}"


def generate_one(adapter: str, core: dict[str, str]) -> str:
    meta, delta = load_delta(adapter)
    title = meta.get("title", f"{adapter.title()}-Optimized Workflow (v1.1)")
    blurb = meta.get(
        "blurb",
        f"This is a **{adapter}-optimized** adaptation of the core methodology.",
    )
    marker = existing_marker(adapter) or (
        "> **Last synced from core:** PLACEHOLDER (run scripts/update-sync-markers.sh)"
    )

    lines: list[str] = []
    lines.append(
        "<!-- GENERATED FILE — do not edit by hand.\n"
        "     Sources: core/workflow.md +\n"
        f"              adapters/{adapter}/ai-workflow/deltas/workflow.delta.md\n"
        "     Regenerate: python scripts/generate-adapter-workflows.py\n"
        "     Check:      python scripts/generate-adapter-workflows.py --check\n"
        "-->"
    )
    lines.append(f"# {title}")
    lines.append("")
    lines.append(marker)
    lines.append(
        f"> This file is generated from `core/workflow.md` plus the {adapter} "
        f"delta. Tool-specific notes are in the delta; shared methodology is core. "
        f"Run `../sync/check-core.sh` regularly."
    )
    lines.append("")
    lines.append(blurb)
    lines.append("")

    # Strengths
    strengths = delta.get("Strengths") or delta.get(
        f"{meta.get('tool_name', adapter.title())} Strengths We Leverage"
    )
    if strengths:
        tool = meta.get("tool_name", adapter.title())
        lines.append(f"## {tool} Strengths We Leverage")
        lines.append("")
        lines.append(strengths.rstrip())
        lines.append("")

    # Shared core sections in order (skip Cursor-only)
    order = [
        "Autonomy calibration",
        "Full vs lightweight workflow",
        "Phase 0 — Repo audit",
        "Phase 0.5 — Strategy & Model Selection",
        "Phase 1 — Task brief",
        "Phase 2 — Self-evaluation gate",
        "Phase 3 — Implementation",
        "Phase 4 — Anti-loop rule",
        "Phase 5 — Verification",
        "Phase 6 — Rate",
        "Phase 7 — Failure capture",
        "Phase 8 — Handoff",
        "Weekly refine",
    ]

    # Pre-phase optional block (e.g. Grok strategy)
    pre = delta.get("Pre-phase")
    if pre:
        lines.append(pre.rstrip())
        lines.append("")

    for heading in order:
        body = core.get(heading)
        if body is None:
            # try fuzzy match startswith Phase N
            body = None
            for k, v in core.items():
                if k.startswith(heading.split("—")[0].strip()) or k == heading:
                    body = v
                    heading = k
                    break
        if body is None:
            continue
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(body.rstrip())
        lines.append("")
        # Structural floor in adapters requires a 4…8 token (e.g. 4-8 / 4–8).
        # core/ uses prose "4 to 8", which does not match 4[^alnum]+8.
        if heading.startswith("Phase 1"):
            lines.append(
                "Adapter floor: Ideal State Criteria count is **4–8** "
                "(binary, checkable) — same rule as core's “4 to 8”."
            )
            lines.append("")
        # Adapter note under this phase
        note_key = phase_note_key(heading)

        if note_key and note_key in delta:
            lines.append(f"**{meta.get('tool_name', adapter.title())} note:**")
            lines.append("")
            lines.append(delta[note_key].rstrip())
            lines.append("")
        # Also allow exact "Notes — <full heading>"
        full_note = f"Notes — {heading}"
        if full_note in delta and full_note != note_key:
            lines.append(delta[full_note].rstrip())
            lines.append("")

    # Closing from delta
    closing = delta.get("Closing") or delta.get("Final Reminder")
    if closing:
        lines.append("---")
        lines.append("")
        lines.append(closing.rstrip())
        lines.append("")

    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated content differs from files on disk",
    )
    ap.add_argument(
        "--adapters",
        nargs="*",
        default=list(ADAPTERS),
        help="Subset of adapters to generate",
    )
    args = ap.parse_args()
    core = core_sections()
    drifted = []
    for adapter in args.adapters:
        if adapter not in ADAPTERS:
            print(f"skip unknown adapter {adapter}", file=sys.stderr)
            continue
        out_path = (
            ROOT
            / "adapters"
            / adapter
            / "ai-workflow"
            / "instructions"
            / "workflow.md"
        )
        generated = generate_one(adapter, core)
        if args.check:
            if not out_path.is_file():
                print(f"MISSING {out_path}")
                drifted.append(adapter)
                continue
            existing = out_path.read_text(encoding="utf-8")
            # Normalize newlines for compare
            if existing.replace("\r\n", "\n") != generated.replace("\r\n", "\n"):
                print(f"DRIFT  {out_path}")
                drifted.append(adapter)
            else:
                print(f"OK     {out_path}")
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(generated, encoding="utf-8", newline="\n")
            print(f"WROTE  {out_path}")
    if args.check and drifted:
        print(
            f"\n{len(drifted)} adapter workflow(s) out of date. Run:\n"
            f"  python scripts/generate-adapter-workflows.py",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
