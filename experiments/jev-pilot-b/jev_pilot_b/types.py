"""Provider-neutral decision types (frozen contract).

Python field names are snake_case aliases of the TypeScript contract:

    type Decision = 'pass' | 'fail' | 'needs_review'
    interface DecideInput { artifact, question, yesMeans?, noMeans?,
                            yesAtOrAbove?, noAtOrBelow? }
    interface DecideResult { decision, p?, confidence?, provider, latencyMs,
                             cost?, abstained, raw? }
    interface DecisionProvider { name; decide(input): Promise<DecideResult> }
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol, get_args

Decision = Literal["pass", "fail", "needs_review"]
DECISIONS: tuple[Decision, ...] = get_args(Decision)

ProviderName = Literal["rules", "jev", "llm", "human"]
PROVIDERS: tuple[ProviderName, ...] = get_args(ProviderName)

Artifact = str | dict[str, Any] | list[Any]


@dataclass(frozen=True)
class DecideInput:
    """One artifact plus one yes/no question (typically an Ideal State Criterion)."""

    artifact: Artifact
    question: str
    yes_means: str | None = None
    no_means: str | None = None
    yes_at_or_above: float | None = None
    no_at_or_below: float | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> DecideInput:
        """Accept snake_case or the frozen camelCase field names."""
        return cls(
            artifact=data["artifact"],
            question=data["question"],
            yes_means=data.get("yes_means", data.get("yesMeans")),
            no_means=data.get("no_means", data.get("noMeans")),
            yes_at_or_above=data.get("yes_at_or_above", data.get("yesAtOrAbove")),
            no_at_or_below=data.get("no_at_or_below", data.get("noAtOrBelow")),
        )


@dataclass(frozen=True)
class DecideResult:
    decision: Decision
    provider: ProviderName
    latency_ms: float
    abstained: bool
    p: float | None = None
    confidence: float | None = None
    cost: float | None = None
    raw: Any = None


class DecisionProvider(Protocol):
    """Caller-owned backend. Implementations live in ``providers/``."""

    name: str

    async def decide(self, input: DecideInput) -> DecideResult: ...
