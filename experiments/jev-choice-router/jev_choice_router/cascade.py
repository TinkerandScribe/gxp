"""Caller-owned cascade helper.

Default order (documented, not wired into any product bot):

    rules → jev_stub → confidence_floor → human

A provider that sets ``abstained=True`` is skipped. After a non-abstaining
Jev result, ``apply_confidence_floor`` rewrites the label to ``human`` when
confidence (else probability) is below the configurable floor.

When ``CHOICE_ROUTER`` is off, ``default_providers`` omits Jev entirely
(flag off = unused).
"""

from __future__ import annotations

from collections.abc import Sequence

from jev_choice_router.flags import (
    DEFAULT_CONFIDENCE_FLOOR,
    is_choice_router_enabled,
    read_confidence_floor,
)
from jev_choice_router.types import ChoiceInput, ChoiceProvider, ChoiceResult

# Source of order for callers / README. confidence_floor is a filter, not a provider.
CASCADE_ORDER: tuple[str, ...] = ("rules", "jev", "confidence_floor", "human")


def apply_confidence_floor(
    result: ChoiceResult,
    floor: float = DEFAULT_CONFIDENCE_FLOOR,
) -> ChoiceResult:
    """Force ``human`` when a Jev label sits below the confidence floor."""
    if result.abstained or result.provider != "jev":
        return result
    score = result.confidence if result.confidence is not None else result.probability
    if score >= floor:
        return result
    return ChoiceResult(
        label="human",
        provider="human",
        latency_ms=result.latency_ms,
        abstained=False,
        probability=0.0,
        cost_usd=result.cost_usd,
        confidence=score,
        raw={
            "reason": "confidence_floor",
            "floor": floor,
            "prior_label": result.label,
            "prior_confidence": score,
            "prior": {
                "label": result.label,
                "provider": result.provider,
                "probability": result.probability,
            },
        },
    )


async def cascade(
    providers: Sequence[ChoiceProvider],
    input: ChoiceInput,
    *,
    confidence_floor: float | None = None,
) -> ChoiceResult:
    """Run providers until one does not abstain; apply the Jev confidence floor."""
    if not providers:
        raise ValueError("cascade requires at least one ChoiceProvider")

    floor = DEFAULT_CONFIDENCE_FLOOR if confidence_floor is None else confidence_floor
    last: ChoiceResult | None = None
    for provider in providers:
        result = await provider.choose(input)
        last = result
        if result.abstained:
            continue
        if getattr(provider, "name", "") == "jev" or result.provider == "jev":
            return apply_confidence_floor(result, floor)
        return result
    assert last is not None
    return last


def default_providers(
    *,
    environ: dict[str, str] | None = None,
    jev_client: object | None = None,
):
    """rules → (jev if CHOICE_ROUTER) → human. Jev omitted when the flag is off."""
    from jev_choice_router.providers.human import HumanProvider
    from jev_choice_router.providers.jev import JevChoiceProvider
    from jev_choice_router.providers.rules import RulesProvider

    providers: list[ChoiceProvider] = [RulesProvider()]
    if is_choice_router_enabled(environ):
        providers.append(JevChoiceProvider(client=jev_client))  # type: ignore[arg-type]
    providers.append(HumanProvider())
    return providers


def default_confidence_floor(environ: dict[str, str] | None = None) -> float:
    return read_confidence_floor(environ)
