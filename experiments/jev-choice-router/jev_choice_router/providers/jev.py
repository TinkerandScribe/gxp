"""Jev backend stub: would call MCP ``jev_classify`` with frozen options.

Public types stay in ``jev_choice_router.types`` and never mention this
module. This file is the only place that knows classify-request vocabulary.

Hard-usage hold: this tree does **not** open sockets, import urllib, or
invoke MCP. Default transport is ``HeldJevClassifyClient``. Tests inject a
fake ``JevClassifyClient``.

Key handling (never commit secrets; see ``core/rules/01-no-secrets-in-git.md``):

- Live HTTP *would* read ``JEV_API_KEY`` then ``TYPESAFE_API_KEY``.
- MCP *would* inject a client that forwards to the host ``jev_classify``
  tool. The API key stays in the MCP server env, never in tool arguments.
- ``CHOICE_ROUTER`` off → this provider abstains immediately (unused).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from jev_choice_router.flags import is_choice_router_enabled
from jev_choice_router.options import FROZEN_OPTIONS, FROZEN_QUESTION
from jev_choice_router.types import CHOICES, Choice, ChoiceInput, ChoiceResult, State

ClassifyAction = Literal["act", "review", "abstain"]
DEFAULT_ACT_ABOVE = 0.8
DEFAULT_REVIEW_ABOVE = 0.5


class LiveCallsDisabledError(RuntimeError):
    """Raised when a would-be live ``jev_classify`` is invoked under hold."""


@dataclass(frozen=True)
class JevClassifyRequest:
    """MCP ``jev_classify`` arguments (state + question + frozen options)."""

    state: State
    question: str
    options: dict[str, str]
    add_none: bool = False
    act_above: float | None = None
    review_above: float | None = None

    def to_mcp_arguments(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "state": self.state,
            "question": self.question,
            "options": dict(self.options),
            "add_none": self.add_none,
        }
        if self.act_above is not None:
            payload["act_above"] = self.act_above
        if self.review_above is not None:
            payload["review_above"] = self.review_above
        return payload


@dataclass(frozen=True)
class JevClassifyResponse:
    """MCP-shaped ``jev_classify`` result (would-be)."""

    label: str
    probabilities: dict[str, float]
    confidence: float
    action: ClassifyAction
    model: str | None = None
    usage: dict[str, Any] | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> JevClassifyResponse:
        label = data.get("label", data.get("answer", data.get("option")))
        if not label:
            raise ValueError("jev_classify response requires label/answer/option")
        action = data.get("action", "act")
        if action not in ("act", "review", "abstain"):
            raise ValueError(f"unknown jev_classify action: {action!r}")
        probabilities = data.get("probabilities") or data.get("probability") or {}
        if isinstance(probabilities, (int, float)):
            probabilities = {str(label): float(probabilities)}
        confidence = data.get("confidence")
        if confidence is None:
            confidence = float(probabilities.get(str(label), 0.0)) if probabilities else 0.0
        return cls(
            label=str(label),
            probabilities={str(k): float(v) for k, v in dict(probabilities).items()},
            confidence=float(confidence),
            action=action,  # type: ignore[arg-type]
            model=data.get("model"),
            usage=data.get("usage"),
        )


class JevClassifyClient(Protocol):
    """Thin transport: MCP-shaped request in, MCP-shaped response out."""

    def classify(self, request: JevClassifyRequest) -> JevClassifyResponse: ...


class HeldJevClassifyClient:
    """Hard-usage hold. Does not call Jev. ``classify`` raises if reached."""

    def classify(self, request: JevClassifyRequest) -> JevClassifyResponse:
        _ = request
        raise LiveCallsDisabledError(
            "hard-usage hold: jev_classify is not sent. Inject a JevClassifyClient "
            "in tests. Soft spike only — no live Jev/MCP."
        )


def read_api_key_from_env(environ: dict[str, str] | None = None) -> str | None:
    """Read ``JEV_API_KEY`` then ``TYPESAFE_API_KEY``. Never a hardcoded default."""
    env = os.environ if environ is None else environ
    for name in ("JEV_API_KEY", "TYPESAFE_API_KEY"):
        value = env.get(name, "").strip()
        if value:
            return value
    return None


def _cost_from_usage(usage: dict[str, Any] | None) -> float:
    if not usage:
        return 0.0
    if "cost_usd" in usage:
        return float(usage["cost_usd"])
    if "cost" in usage:
        return float(usage["cost"])
    if "est_cost_usd" in usage:
        return float(usage["est_cost_usd"])
    return 0.0


class JevChoiceProvider:
    """ChoiceProvider that *would* map MCP ``jev_classify`` onto ``ChoiceResult``."""

    name = "jev"

    def __init__(
        self,
        client: JevClassifyClient | None = None,
        *,
        enabled: bool | None = None,
        options: dict[str, str] | None = None,
        question: str | None = None,
    ) -> None:
        self.client = client if client is not None else HeldJevClassifyClient()
        self.enabled = is_choice_router_enabled() if enabled is None else enabled
        self.options = dict(options or FROZEN_OPTIONS)
        self.question = question or FROZEN_QUESTION

    async def choose(self, input: ChoiceInput) -> ChoiceResult:
        started = time.perf_counter()
        if not self.enabled:
            return ChoiceResult(
                label="human",
                provider="jev",
                latency_ms=_elapsed_ms(started),
                abstained=True,
                probability=0.0,
                cost_usd=0.0,
                raw={"reason": "choice_router_unused", "flag": "CHOICE_ROUTER"},
            )
        request = JevClassifyRequest(
            state=input.state,
            question=input.question or self.question,
            options=self.options,
            add_none=False,
            act_above=DEFAULT_ACT_ABOVE,
            review_above=DEFAULT_REVIEW_ABOVE,
        )
        try:
            response = self.client.classify(request)
        except LiveCallsDisabledError as exc:
            return ChoiceResult(
                label="human",
                provider="jev",
                latency_ms=_elapsed_ms(started),
                abstained=True,
                probability=0.0,
                cost_usd=0.0,
                raw={"reason": "hard_usage_hold", "error": str(exc)},
            )
        return _result_from_response(response, request, started)


def _result_from_response(
    response: JevClassifyResponse,
    request: JevClassifyRequest,
    started: float,
) -> ChoiceResult:
    abstained = response.action == "abstain" or response.label not in CHOICES
    label: Choice = response.label if response.label in CHOICES else "human"  # type: ignore[assignment]
    probability = float(response.probabilities.get(response.label, response.confidence))
    return ChoiceResult(
        label=label,
        provider="jev",
        latency_ms=_elapsed_ms(started),
        abstained=abstained,
        probability=probability,
        cost_usd=_cost_from_usage(response.usage),
        confidence=response.confidence,
        raw={
            "label": response.label,
            "probabilities": response.probabilities,
            "confidence": response.confidence,
            "action": response.action,
            "model": response.model,
            "usage": response.usage,
            "mcp_arguments": request.to_mcp_arguments(),
        },
    )


def _elapsed_ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000.0
