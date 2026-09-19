"""Gate G1: one artifact + one Ideal State Criterion → decide()."""

from __future__ import annotations

from jev_pilot_b.types import Artifact, DecideInput, DecideResult, DecisionProvider


async def gate_g1(
    artifact: Artifact,
    criterion: str,
    provider: DecisionProvider,
    *,
    yes_means: str | None = None,
    no_means: str | None = None,
    yes_at_or_above: float | None = None,
    no_at_or_below: float | None = None,
) -> DecideResult:
    """Evaluate a single Ideal State Criterion against one artifact.

    ``criterion`` is the yes/no question passed through as ``DecideInput.question``.
    The caller chooses which ``DecisionProvider`` (or cascade wrapper) to use.
    """
    return await provider.decide(
        DecideInput(
            artifact=artifact,
            question=criterion,
            yes_means=yes_means,
            no_means=no_means,
            yes_at_or_above=yes_at_or_above,
            no_at_or_below=no_at_or_below,
        )
    )
