"""Optional parallel Noul sketch: ``safe_to_act`` before destructive tools.

Stub interface only. No live Jev / Noul / MCP calls. Hard-usage hold.
Callers that would ask Noul before a destructive tool inject a
``SafeToActClient``; the default held client abstains with stub zeros.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol

from jev_choice_router.types import State

SafeToActVerdict = Literal["yes", "no"]
SAFE_TO_ACT_QUESTION = "Is it safe to act with this destructive tool?"


@dataclass(frozen=True)
class SafeToActRequest:
    state: State
    tool_name: str
    question: str = SAFE_TO_ACT_QUESTION

    def to_noul_arguments(self) -> dict[str, Any]:
        """Would-be noul/check payload. Never sent on this spike."""
        return {
            "state": self.state,
            "question": self.question,
            "tool_name": self.tool_name,
        }


@dataclass(frozen=True)
class SafeToActResult:
    verdict: SafeToActVerdict | None
    probability: float
    latency_ms: float
    cost_usd: float
    abstained: bool
    raw: Any = None


class SafeToActClient(Protocol):
    def check(self, request: SafeToActRequest) -> SafeToActResult: ...


class HeldSafeToActClient:
    """Hard-usage hold: does not call Noul. Always abstains."""

    def check(self, request: SafeToActRequest) -> SafeToActResult:
        _ = request
        return SafeToActResult(
            verdict=None,
            probability=0.0,
            latency_ms=0.0,
            cost_usd=0.0,
            abstained=True,
            raw={"reason": "hard_usage_hold", "interface": "safe_to_act"},
        )
