"""Jev backend: MCP-shaped ``jev_check`` semantics behind DecisionProvider.

Public types stay in ``jev_pilot_b.types`` and never mention this module.
This file is the only place that knows check-verdict vocabulary
(``yes`` / ``no`` / ``uncertain``) and optional HTTP/MCP transport.

Key handling (never commit secrets; see ``core/rules/01-no-secrets-in-git.md``):

- HTTP client reads ``JEV_API_KEY`` then ``TYPESAFE_API_KEY`` from the
  environment (same order documented by jev-mcp).
- MCP usage: inject a ``JevCheckClient`` that forwards to the host's
  ``jev_check`` tool. The API key stays in the MCP server env, never in
  tool arguments or in this repo.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from jev_pilot_b.predisposition import (
    DEFAULT_FAIL_BORDER_MID,
    apply_fail_border_handoff,
)
from jev_pilot_b.types import Artifact, DecideInput, DecideResult, Decision

CheckVerdict = Literal["yes", "no", "uncertain"]
DEFAULT_YES_AT_OR_ABOVE = 0.7
DEFAULT_NO_AT_OR_BELOW = 0.3
DEFAULT_HTTP_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-latest"


@dataclass(frozen=True)
class JevCheckRequest:
    """MCP ``jev_check`` arguments (state + question + optional thresholds)."""

    state: Artifact
    question: str
    yes_means: Any | None = None
    no_means: Any | None = None
    yes_at_or_above: float | None = None
    no_at_or_below: float | None = None

    def to_mcp_arguments(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"state": self.state, "question": self.question}
        if self.yes_means is not None:
            payload["yes_means"] = self.yes_means
        if self.no_means is not None:
            payload["no_means"] = self.no_means
        if self.yes_at_or_above is not None:
            payload["yes_at_or_above"] = self.yes_at_or_above
        if self.no_at_or_below is not None:
            payload["no_at_or_below"] = self.no_at_or_below
        return payload


@dataclass(frozen=True)
class JevCheckResponse:
    """MCP-shaped ``jev_check`` result."""

    verdict: CheckVerdict
    probability_yes: float
    model: str | None = None
    usage: dict[str, Any] | None = None
    thresholds: dict[str, float] | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> JevCheckResponse:
        if "verdict" not in data or "probability_yes" not in data:
            raise ValueError("jev_check response requires verdict and probability_yes")
        verdict = data["verdict"]
        if verdict not in ("yes", "no", "uncertain"):
            raise ValueError(f"unknown jev_check verdict: {verdict!r}")
        return cls(
            verdict=verdict,
            probability_yes=float(data["probability_yes"]),
            model=data.get("model"),
            usage=data.get("usage"),
            thresholds=data.get("thresholds"),
        )


def verdict_from_probability(
    probability_yes: float,
    *,
    yes_at_or_above: float = DEFAULT_YES_AT_OR_ABOVE,
    no_at_or_below: float = DEFAULT_NO_AT_OR_BELOW,
) -> CheckVerdict:
    """MCP ``jev_check`` band: yes / no / uncertain from p(yes)."""
    if probability_yes >= yes_at_or_above:
        return "yes"
    if probability_yes <= no_at_or_below:
        return "no"
    return "uncertain"


def map_check_verdict(
    raw: dict[str, Any] | JevCheckResponse,
    *,
    abstain_on_uncertain: bool = False,
) -> tuple[Decision, bool]:
    """Map ``jev_check`` yes→pass, no→fail, uncertain→needs_review.

    When ``abstain_on_uncertain`` is true, an uncertain verdict still maps to
    ``needs_review`` but ``abstained`` is true so a cascade can continue.
    """
    response = raw if isinstance(raw, JevCheckResponse) else JevCheckResponse.from_mapping(raw)
    if response.verdict == "yes":
        return "pass", False
    if response.verdict == "no":
        return "fail", False
    if response.verdict == "uncertain":
        return "needs_review", abstain_on_uncertain
    raise ValueError(f"unhandled verdict: {response.verdict!r}")


class JevCheckClient(Protocol):
    """Thin transport: MCP-shaped request in, MCP-shaped response out."""

    def check(self, request: JevCheckRequest) -> JevCheckResponse: ...


class MissingApiKeyError(RuntimeError):
    """Raised when HTTP transport is used without an env key."""


def read_api_key_from_env(
    environ: dict[str, str] | None = None,
) -> str | None:
    """Read ``JEV_API_KEY`` then ``TYPESAFE_API_KEY``. Never a hardcoded default."""
    env = os.environ if environ is None else environ
    for name in ("JEV_API_KEY", "TYPESAFE_API_KEY"):
        value = env.get(name, "").strip()
        if value:
            return value
    return None


class HttpJevCheckClient:
    """Optional HTTP transport for TypeSafe System One (noul ≈ jev_check).

    Base URL and model come from ``JEV_BASE_URL`` / ``JEV_MODEL``. The key
    is read at request time from the environment so it is never stored in
    source. Tests should inject a fake ``JevCheckClient`` instead of calling
    the network.
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float = 15.0,
        opener: Any | None = None,
    ) -> None:
        self.base_url = base_url or os.environ.get("JEV_BASE_URL", DEFAULT_HTTP_URL)
        self.model = model or os.environ.get("JEV_MODEL", DEFAULT_MODEL)
        self.timeout_s = timeout_s
        self._opener = opener

    def check(self, request: JevCheckRequest) -> JevCheckResponse:
        key = read_api_key_from_env()
        if not key:
            raise MissingApiKeyError(
                "HTTP Jev client needs JEV_API_KEY or TYPESAFE_API_KEY in the "
                "environment. For MCP, inject a JevCheckClient that calls "
                "jev_check and keep the key on the MCP server."
            )
        yes_at = (
            request.yes_at_or_above
            if request.yes_at_or_above is not None
            else DEFAULT_YES_AT_OR_ABOVE
        )
        no_at = (
            request.no_at_or_below
            if request.no_at_or_below is not None
            else DEFAULT_NO_AT_OR_BELOW
        )
        question: dict[str, Any] = {
            "type": "noul",
            "instructions": request.question,
        }
        criteria: dict[str, Any] = {}
        if request.yes_means is not None:
            criteria["true"] = request.yes_means
        if request.no_means is not None:
            criteria["false"] = request.no_means
        if criteria:
            question["criteria"] = criteria
        body = {
            "model": self.model,
            "state": request.state,
            "questions": {"check": question},
        }
        raw_response = self._post_json(body, key)
        answers = raw_response.get("answers") or {}
        check = answers.get("check") or {}
        if "noul" not in check:
            raise ValueError("HTTP response missing answers.check.noul")
        probability_yes = float(check["noul"])
        verdict = verdict_from_probability(
            probability_yes, yes_at_or_above=yes_at, no_at_or_below=no_at
        )
        return JevCheckResponse(
            verdict=verdict,
            probability_yes=probability_yes,
            model=raw_response.get("model"),
            usage=raw_response.get("usage"),
            thresholds={"yes_at_or_above": yes_at, "no_at_or_below": no_at},
        )

    def _post_json(self, body: dict[str, Any], key: str) -> dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            self.base_url,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        open_fn = self._opener.open if self._opener is not None else urllib.request.urlopen
        try:
            with open_fn(req, timeout=self.timeout_s) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Jev HTTP {exc.code}: {detail}") from exc


class JevProvider:
    """DecisionProvider that maps MCP ``jev_check`` onto ``DecideResult``."""

    name = "jev"

    def __init__(
        self,
        client: JevCheckClient | None = None,
        *,
        abstain_on_uncertain: bool = False,
        fail_border_handoff: bool = True,
        fail_border_mid: float = DEFAULT_FAIL_BORDER_MID,
    ) -> None:
        self.client = client if client is not None else HttpJevCheckClient()
        self.abstain_on_uncertain = abstain_on_uncertain
        self.fail_border_handoff = fail_border_handoff
        self.fail_border_mid = fail_border_mid

    async def decide(self, input: DecideInput) -> DecideResult:
        started = time.perf_counter()
        request = JevCheckRequest(
            state=input.artifact,
            question=input.question,
            yes_means=input.yes_means,
            no_means=input.no_means,
            yes_at_or_above=input.yes_at_or_above,
            no_at_or_below=input.no_at_or_below,
        )
        response = self.client.check(request)
        decision, abstained = map_check_verdict(
            response, abstain_on_uncertain=self.abstain_on_uncertain
        )
        result = DecideResult(
            decision=decision,
            provider="jev",
            latency_ms=(time.perf_counter() - started) * 1000.0,
            abstained=abstained,
            p=response.probability_yes,
            cost=_cost_from_usage(response.usage),
            raw={
                "verdict": response.verdict,
                "probability_yes": response.probability_yes,
                "model": response.model,
                "usage": response.usage,
                "thresholds": response.thresholds,
                "mcp_arguments": request.to_mcp_arguments(),
            },
        )
        if self.fail_border_handoff:
            no_at = (
                input.no_at_or_below
                if input.no_at_or_below is not None
                else DEFAULT_NO_AT_OR_BELOW
            )
            result = apply_fail_border_handoff(
                result,
                no_at_or_below=no_at,
                fail_border_mid=self.fail_border_mid,
            )
        return result


def _cost_from_usage(usage: dict[str, Any] | None) -> float | None:
    if not usage:
        return None
    if "cost" in usage:
        return float(usage["cost"])
    if "est_cost_usd" in usage:
        return float(usage["est_cost_usd"])
    return None
