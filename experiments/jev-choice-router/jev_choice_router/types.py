"""Provider-neutral choice types (frozen contract).

Python field names are snake_case aliases of the TypeScript contract:

    type Choice = 'deterministic' | 'tool' | 'llm' | 'human' | 'halt'
    interface ChooseInput { state; question? }
    interface ChooseResult { label; probability; latencyMs; costUsd;
                             confidence?; provider; abstained; raw? }
    interface ChoiceProvider { name; choose(input): Promise<ChooseResult> }
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol, get_args

Choice = Literal["deterministic", "tool", "llm", "human", "halt"]
CHOICES: tuple[Choice, ...] = get_args(Choice)

ProviderName = Literal["rules", "jev", "human"]
PROVIDERS: tuple[ProviderName, ...] = get_args(ProviderName)

State = str | dict[str, Any] | list[Any] | None


@dataclass(frozen=True)
class ChoiceInput:
    """Short next-step context. ``question`` defaults to the frozen classify prompt."""

    state: State
    question: str | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> ChoiceInput:
        """Accept snake_case or the frozen camelCase field names."""
        return cls(
            state=data.get("state", data.get("step")),
            question=data.get("question"),
        )


@dataclass(frozen=True)
class ChoiceResult:
    label: Choice
    provider: ProviderName
    latency_ms: float
    abstained: bool
    probability: float = 0.0
    cost_usd: float = 0.0
    confidence: float | None = None
    raw: Any = None


class ChoiceProvider(Protocol):
    """Caller-owned backend. Implementations live in ``providers/``."""

    name: str

    async def choose(self, input: ChoiceInput) -> ChoiceResult: ...
