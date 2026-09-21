"""Tiny caller helper: state → ChoiceResult via the default cascade."""

from __future__ import annotations

from collections.abc import Sequence

from jev_choice_router.cascade import cascade, default_confidence_floor, default_providers
from jev_choice_router.types import ChoiceInput, ChoiceProvider, ChoiceResult, State


async def route_choice(
    state: State,
    *,
    question: str | None = None,
    providers: Sequence[ChoiceProvider] | None = None,
    confidence_floor: float | None = None,
    environ: dict[str, str] | None = None,
    jev_client: object | None = None,
) -> ChoiceResult:
    chain = (
        list(providers)
        if providers is not None
        else default_providers(environ=environ, jev_client=jev_client)
    )
    floor = default_confidence_floor(environ) if confidence_floor is None else confidence_floor
    return await cascade(
        chain,
        ChoiceInput(state=state, question=question),
        confidence_floor=floor,
    )
