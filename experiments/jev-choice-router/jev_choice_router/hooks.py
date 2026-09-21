"""High-precision step-choice rules hooks.

Each hook returns a Choice or None (abstain). Hooks fire on obvious
structural shapes and a small frozen phrase set — not Pilot B G1 labels
and not an unshipped ``policy_v1`` cue list.

Order (first hit wins): empty_state → all_criteria_yes → hard_stop →
destructive_action → draft_prose → named_verify → open_url_or_search.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from typing import Any

from jev_choice_router.types import Choice, ChoiceInput, State

EMPTY_STATE_HOOK = "empty_state"
ALL_CRITERIA_YES_HOOK = "all_criteria_yes"
HARD_STOP_HOOK = "hard_stop"
DESTRUCTIVE_ACTION_HOOK = "destructive_action"
DRAFT_PROSE_HOOK = "draft_prose"
NAMED_VERIFY_HOOK = "named_verify"
OPEN_URL_OR_SEARCH_HOOK = "open_url_or_search"

_YES_TOKENS = frozenset({"yes", "true", "pass", "met", "ok"})
_NAMED_COMMANDS = (
    "verify.sh",
    "python -m unittest",
    "unittest discover",
    "pytest",
    "npm test",
    "check-core.sh",
    "eval-agent-code-quality-selftest.sh",
)
_DRAFT_PHRASES = (
    "draft the pr",
    "draft a pr",
    "pr body",
    "draft prose",
    "draft commit message",
    "draft the commit",
    "write a one-paragraph",
    "write a readme",
    "explain why",
    "explain how",
    "rewrite the",
    "draft a short",
    "draft the binary",
    "draft a two-sentence",
    "operator note",
    "rationale for",
    "readable prose",
)
_DESTRUCTIVE_PHRASES = (
    "merge to main",
    "merge into main",
    "force-push",
    "force push",
    "push --force",
    "delete the production",
    "drop the production",
    "drop table",
    "rm -rf",
)
_HARD_STOP_PHRASES = (
    "hard stop",
    "kill gate",
    "named inverse applied",
    "work is done",
    "criteria met",
    "halt.",
    "halt:",
)
_ALL_CRITERIA_PHRASES = (
    "all criteria already yes",
    "all ideal state criteria already",
    "isc walk complete",
    "all six ideal state criteria already",
    "all six isc",
    "isc 1–6 all yes",
    "isc 1-6 all yes",
    "every binding criterion",
)


def state_text(state: State) -> str:
    if state is None:
        return ""
    if isinstance(state, str):
        return state
    return json.dumps(state, ensure_ascii=False)


def is_empty_state(state: State) -> bool:
    if state is None:
        return True
    if isinstance(state, str) and not state.strip():
        return True
    if isinstance(state, (dict, list)) and len(state) == 0:
        return True
    return False


def empty_state(input: ChoiceInput) -> Choice | None:
    """human when the step context is structurally empty."""
    if is_empty_state(input.state):
        return "human"
    return None


def all_criteria_yes(input: ChoiceInput) -> Choice | None:
    """halt when every recorded criterion is already yes."""
    art = input.state
    if isinstance(art, dict):
        block = art.get("criteria", art.get("isc", art.get("ideal_state_criteria")))
        if _all_yes_block(block):
            return "halt"
        if art.get("all_criteria") in ("yes", True, "met"):
            return "halt"
    low = state_text(input.state).lower()
    if any(phrase in low for phrase in _ALL_CRITERIA_PHRASES):
        return "halt"
    return None


def hard_stop(input: ChoiceInput) -> Choice | None:
    """halt on an explicit kill-gate / criteria-met / named-inverse stop."""
    low = state_text(input.state).lower()
    if any(phrase in low for phrase in _HARD_STOP_PHRASES):
        return "halt"
    return None


def destructive_action(input: ChoiceInput) -> Choice | None:
    """human for merge-to-main / force-push / production-destructive steps."""
    low = state_text(input.state).lower()
    if any(phrase in low for phrase in _DESTRUCTIVE_PHRASES):
        return "human"
    if re.search(r"\bmerge\b.*\bto main\b", low):
        return "human"
    return None


def draft_prose(input: ChoiceInput) -> Choice | None:
    """llm when the step is drafting / explaining / rewriting prose."""
    low = state_text(input.state).lower()
    if any(phrase in low for phrase in _DRAFT_PHRASES):
        return "llm"
    if re.search(r"\bdraft\b", low) and any(
        token in low for token in ("pr", "prose", "paragraph", "readme", "handoff", "rationale")
    ):
        return "llm"
    return None


def named_verify(input: ChoiceInput) -> Choice | None:
    """deterministic when the step is a named test / verify command."""
    low = state_text(input.state).lower()
    if any(name in low for name in _NAMED_COMMANDS):
        return "deterministic"
    return None


def open_url_or_search(input: ChoiceInput) -> Choice | None:
    """tool when the step is open-URL or search / retrieval."""
    text = state_text(input.state)
    low = text.lower()
    if re.search(r"https?://", text):
        return "tool"
    if re.search(
        r"\b(open url|search the |search repo|web-search|web search|"
        r"look up |fetch the |retrieve the )\b",
        low,
    ):
        return "tool"
    if low.startswith("search ") or " search " in f" {low} ":
        return "tool"
    return None


def _all_yes_block(block: Any) -> bool:
    if isinstance(block, dict):
        if not block:
            return False
        return all(_atom_yes(value) for value in block.values())
    if isinstance(block, list):
        if not block:
            return False
        return all(_atom_yes(item) for item in block)
    return False


def _atom_yes(value: Any) -> bool:
    if isinstance(value, bool):
        return value is True
    if isinstance(value, str):
        return value.strip().lower() in _YES_TOKENS
    if isinstance(value, dict):
        met = value.get("met", value.get("yes", value.get("status")))
        return _atom_yes(met)
    return False


RULES_HOOKS: tuple = (
    empty_state,
    all_criteria_yes,
    hard_stop,
    destructive_action,
    draft_prose,
    named_verify,
    open_url_or_search,
)

RULES_HOOK_NAMES: tuple[str, ...] = (
    EMPTY_STATE_HOOK,
    ALL_CRITERIA_YES_HOOK,
    HARD_STOP_HOOK,
    DESTRUCTIVE_ACTION_HOOK,
    DRAFT_PROSE_HOOK,
    NAMED_VERIFY_HOOK,
    OPEN_URL_OR_SEARCH_HOOK,
)


def hook_name(hook: Any) -> str:
    return getattr(hook, "__name__", repr(hook))


def first_firing_hook(input: ChoiceInput, hooks: Sequence | None = None) -> str | None:
    for hook in hooks if hooks is not None else RULES_HOOKS:
        if hook(input) is not None:
            return hook_name(hook)
    return None
