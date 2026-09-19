"""High-precision deterministic rules hooks for Pilot B Spike B.

Each hook returns a Decision or None (abstain). Hooks fire only on
unambiguous structural shapes — not on free-text cue lists.

``policy_v1`` cue matching stays UNSHIPPED and must not be imported here.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from jev_pilot_b.types import DecideInput, Decision

# Named hook that ends rules-always-abstain on a frozen positive set.
EMPTY_ARTIFACT_HOOK = "empty_artifact"
CONTRADICTORY_MARKERS_HOOK = "contradictory_markers"
# Same token as the named incomplete-evidence path (README + verify).
INCOMPLETE_EVIDENCE_HOOK = "incomplete_evidence"


def empty_artifact(input: DecideInput) -> Decision | None:
    """Fail when the artifact is structurally empty (nothing to score)."""
    art = input.artifact
    if art is None:
        return "fail"
    if isinstance(art, str) and not art.strip():
        return "fail"
    if isinstance(art, dict) and len(art) == 0:
        return "fail"
    if isinstance(art, list) and len(art) == 0:
        return "fail"
    return None


def contradictory_markers(input: DecideInput) -> Decision | None:
    """needs_review when a structured artifact marks both pass and fail."""
    art = input.artifact
    if not isinstance(art, dict):
        return None
    markers = art.get("markers", art.get("decision_markers"))
    has_pass, has_fail = _marker_pair(markers)
    if has_pass and has_fail:
        return "needs_review"
    return None


def incomplete_evidence(input: DecideInput) -> Decision | None:
    """Named incomplete-evidence path: needs_review before Jev disposition.

    Fires only on a structured dict that declares incompleteness:

    - ``evidence_complete`` is false
    - ``evidence_pack`` is present and empty
    - ``checklist`` / ``evidence_checklist`` lists ``required`` fields that
      are missing from ``present``
    """
    art = input.artifact
    if not isinstance(art, dict):
        return None
    if art.get("evidence_complete") is False:
        return "needs_review"
    if "evidence_pack" in art and _is_empty_pack(art["evidence_pack"]):
        return "needs_review"
    checklist = art.get("evidence_checklist", art.get("checklist"))
    if isinstance(checklist, dict) and _checklist_missing_required(checklist):
        return "needs_review"
    return None


def _is_empty_pack(pack: Any) -> bool:
    if pack is None:
        return True
    if isinstance(pack, (dict, list, str, tuple, set)):
        return len(pack) == 0
    return False


def _checklist_missing_required(checklist: dict[str, Any]) -> bool:
    required = checklist.get("required", checklist.get("required_fields"))
    if not isinstance(required, (list, tuple)) or not required:
        return False
    present = checklist.get("present")
    if present is None:
        present = {
            key: value
            for key, value in checklist.items()
            if key not in ("required", "required_fields", "present", "fields")
        }
    if not isinstance(present, dict):
        return True
    for field in required:
        value = present.get(field)
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, (dict, list, tuple, set)) and len(value) == 0:
            return True
    return False


def _marker_pair(markers: Any) -> tuple[bool, bool]:
    if isinstance(markers, dict):
        has_pass = bool(markers.get("pass") or markers.get("yes"))
        has_fail = bool(markers.get("fail") or markers.get("no"))
        return has_pass, has_fail
    if isinstance(markers, (list, tuple, set)):
        norm = {str(item).strip().lower() for item in markers}
        has_pass = bool(norm & {"pass", "yes"})
        has_fail = bool(norm & {"fail", "no"})
        return has_pass, has_fail
    return False, False


HIGH_PRECISION_HOOKS: tuple = (
    empty_artifact,
    contradictory_markers,
    incomplete_evidence,
)

HIGH_PRECISION_HOOK_NAMES: tuple[str, ...] = (
    EMPTY_ARTIFACT_HOOK,
    CONTRADICTORY_MARKERS_HOOK,
    INCOMPLETE_EVIDENCE_HOOK,
)


def hook_name(hook: Any) -> str:
    return getattr(hook, "__name__", repr(hook))


def first_firing_hook(input: DecideInput, hooks: Sequence | None = None) -> str | None:
    for hook in hooks if hooks is not None else HIGH_PRECISION_HOOKS:
        if hook(input) is not None:
            return hook_name(hook)
    return None
