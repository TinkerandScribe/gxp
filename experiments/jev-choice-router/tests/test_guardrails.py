"""Isolation: no Pilot B cues, no live Jev, no workflow.md edits in this tree."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from jev_choice_router.noul import HeldSafeToActClient, SafeToActRequest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
README = EXPERIMENT_ROOT / "README.md"

_BANNED_IMPORTS = frozenset({"jev_pilot_b", "urllib", "urllib.request", "http.client", "requests", "socket"})
_BANNED_SUBSTRINGS = (
    "policy_v1",
    "cue_list",
    "empty_artifact",
    "incomplete_evidence",
    "contradictory_markers",
    "fail_border_handoff",
    "gate_g1",
)


def _iter_py_files() -> list[Path]:
    files: list[Path] = []
    for path in EXPERIMENT_ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        files.append(path)
    return files


class TestGuardrails(unittest.TestCase):
    def test_readme_documents_isc_flag_and_soft_vs_live(self) -> None:
        text = README.read_text(encoding="utf-8")
        lowered = text.lower()
        for token in (
            "CHOICE_ROUTER",
            "JEV_",
            "deterministic",
            "tool",
            "llm",
            "human",
            "halt",
            "confidence floor",
            "kill gate",
            "soft",
            "hard-usage hold",
            "core/workflow.md",
            "out of scope",
        ):
            self.assertIn(token.lower(), lowered, f"README missing {token!r}")
        self.assertIn("code/rules can finish this step", text)
        self.assertIn("call a named tool / retrieval", text)
        self.assertIn("generative model needed (draft / reason / explain)", text)
        self.assertIn("stop for review", text)
        self.assertIn("criteria met or hard stop", text)
        self.assertIn("label", lowered)
        self.assertIn("probability", lowered)
        self.assertIn("latency_ms", lowered)
        self.assertIn("cost_usd", lowered)

    def test_no_pilot_b_imports_or_cues(self) -> None:
        for path in _iter_py_files():
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        self.assertNotIn(root, _BANNED_IMPORTS, f"{path.name} imports {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".")[0]
                    self.assertNotIn(root, _BANNED_IMPORTS, f"{path.name} imports {node.module}")
            rel = path.relative_to(EXPERIMENT_ROOT)
            if rel.parts[0] == "tests":
                continue
            lowered = source
            for token in _BANNED_SUBSTRINGS:
                # Allow a single explicit "do not reuse" mention in comments.
                if token in lowered and "do not" not in lowered.lower() and "not Pilot" not in source:
                    # hooks.py / rules docstring mention they are not Pilot B cues.
                    if "not Pilot B" in source or "not an unshipped" in source:
                        continue
                    self.fail(f"{rel} contains Pilot B token {token!r}")

    def test_package_has_no_network_imports(self) -> None:
        banned = {"urllib", "urllib.request", "http.client", "requests", "socket"}
        pkg = EXPERIMENT_ROOT / "jev_choice_router"
        for path in pkg.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules: list[str] = []
                if isinstance(node, ast.Import):
                    modules.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules.append(node.module)
                for module in modules:
                    root = module.split(".")[0]
                    self.assertNotIn(root, banned, f"{path.name} imports {module}")
                    self.assertNotIn(module, banned, f"{path.name} imports {module}")

    def test_noul_safe_to_act_is_held(self) -> None:
        result = HeldSafeToActClient().check(
            SafeToActRequest(state="merge to main", tool_name="git_push")
        )
        self.assertTrue(result.abstained)
        self.assertIsNone(result.verdict)
        self.assertEqual(result.probability, 0.0)
        self.assertEqual(result.cost_usd, 0.0)
        self.assertEqual(result.raw["reason"], "hard_usage_hold")

    def test_readme_names_inverse_and_no_default_gxp_path(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("delete", text.lower())
        self.assertIn("experiments/jev-choice-router/", text)
        self.assertIn("no default gxp path change", text.lower())
