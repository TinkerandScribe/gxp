"""Jev Choice Router — opt-in step-choice experiment (not a product adapter)."""

from jev_choice_router.cascade import (
    CASCADE_ORDER,
    DEFAULT_CONFIDENCE_FLOOR,
    apply_confidence_floor,
    cascade,
    default_providers,
)
from jev_choice_router.flags import (
    CHOICE_ROUTER_ENV,
    is_choice_router_enabled,
)
from jev_choice_router.hooks import RULES_HOOKS, RULES_HOOK_NAMES
from jev_choice_router.logging_shape import LOG_FIELDS, choice_log
from jev_choice_router.options import FROZEN_OPTIONS, FROZEN_QUESTION, load_frozen_options
from jev_choice_router.route import route_choice
from jev_choice_router.types import (
    CHOICES,
    PROVIDERS,
    Choice,
    ChoiceInput,
    ChoiceProvider,
    ChoiceResult,
    ProviderName,
    State,
)

__all__ = [
    "CASCADE_ORDER",
    "CHOICES",
    "CHOICE_ROUTER_ENV",
    "DEFAULT_CONFIDENCE_FLOOR",
    "FROZEN_OPTIONS",
    "FROZEN_QUESTION",
    "LOG_FIELDS",
    "PROVIDERS",
    "RULES_HOOKS",
    "RULES_HOOK_NAMES",
    "Choice",
    "ChoiceInput",
    "ChoiceProvider",
    "ChoiceResult",
    "ProviderName",
    "State",
    "apply_confidence_floor",
    "cascade",
    "choice_log",
    "default_providers",
    "is_choice_router_enabled",
    "load_frozen_options",
    "route_choice",
]
