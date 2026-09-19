"""Caller-owned cascade helper.

Default order (documented, not wired into any product bot):

    rules → jev → llm → human

A provider that sets ``abstained=True`` is skipped; the next provider runs.
The caller assembles the provider list; this module only walks it.
"""

from __future__ import annotations

from collections.abc import Sequence

from jev_pilot_b.types import DecideInput, DecideResult, DecisionProvider

# Re-declare here so cascade.py is the source of order for callers/README.
CASCADE_ORDER: tuple[str, ...] = ("rules", "jev", "llm", "human")


async def cascade(
    providers: Sequence[DecisionProvider],
    input: DecideInput,
) -> DecideResult:
    """Run providers in caller-supplied order until one does not abstain.

    If every provider abstains, the last result is returned (still marked
    abstained) so the caller can route to a human gate without inventing
    a decision.
    """
    if not providers:
        raise ValueError("cascade requires at least one DecisionProvider")

    last: DecideResult | None = None
    for provider in providers:
        result = await provider.decide(input)
        last = result
        if not result.abstained:
            return result
    assert last is not None
    return last
