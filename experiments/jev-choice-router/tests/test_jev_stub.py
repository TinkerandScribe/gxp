"""Jev classify stub: injected fake client; hold client never networks."""

from __future__ import annotations

import os
import unittest

from jev_choice_router.options import FROZEN_OPTIONS, FROZEN_QUESTION
from jev_choice_router.providers.jev import (
    HeldJevClassifyClient,
    JevChoiceProvider,
    JevClassifyRequest,
    JevClassifyResponse,
    LiveCallsDisabledError,
    read_api_key_from_env,
)
from jev_choice_router.types import ChoiceInput


class FakeClassifyClient:
    def __init__(self, response: JevClassifyResponse) -> None:
        self.response = response
        self.requests: list[JevClassifyRequest] = []

    def classify(self, request: JevClassifyRequest) -> JevClassifyResponse:
        self.requests.append(request)
        return self.response


class TestJevStub(unittest.IsolatedAsyncioTestCase):
    async def test_fake_client_maps_frozen_options(self) -> None:
        client = FakeClassifyClient(
            JevClassifyResponse(
                label="deterministic",
                probabilities={"deterministic": 0.88, "tool": 0.04},
                confidence=0.88,
                action="act",
                usage={"cost_usd": 0.0},
            )
        )
        provider = JevChoiceProvider(client, enabled=True)
        result = await provider.choose(ChoiceInput(state="leftover step"))
        self.assertEqual(result.label, "deterministic")
        self.assertEqual(result.provider, "jev")
        self.assertFalse(result.abstained)
        self.assertEqual(result.probability, 0.88)
        self.assertEqual(result.cost_usd, 0.0)
        req = client.requests[0]
        self.assertEqual(req.question, FROZEN_QUESTION)
        self.assertEqual(req.options, dict(FROZEN_OPTIONS))
        self.assertIs(req.add_none, False)
        self.assertEqual(set(req.to_mcp_arguments()["options"]), set(FROZEN_OPTIONS))

    async def test_held_client_abstains_without_raising(self) -> None:
        provider = JevChoiceProvider(HeldJevClassifyClient(), enabled=True)
        result = await provider.choose(ChoiceInput(state="leftover step"))
        self.assertTrue(result.abstained)
        self.assertEqual(result.raw["reason"], "hard_usage_hold")
        self.assertEqual(result.probability, 0.0)
        self.assertEqual(result.cost_usd, 0.0)

    def test_held_client_raises_if_called_directly(self) -> None:
        with self.assertRaises(LiveCallsDisabledError):
            HeldJevClassifyClient().classify(
                JevClassifyRequest(state="x", question=FROZEN_QUESTION, options=dict(FROZEN_OPTIONS))
            )

    def test_api_key_reader_has_no_default(self) -> None:
        self.assertIsNone(read_api_key_from_env({}))
        self.assertEqual(read_api_key_from_env({"JEV_API_KEY": "not-a-real-key"}), "not-a-real-key")

    def test_no_urllib_in_jev_module(self) -> None:
        import ast

        path = PathJev()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertFalse(imported & {"urllib", "http", "requests", "socket"})


def PathJev():
    from pathlib import Path

    return Path(__file__).resolve().parents[1] / "jev_choice_router" / "providers" / "jev.py"


class TestNoLiveEnvLeak(unittest.TestCase):
    def test_choice_router_defaults_off(self) -> None:
        from jev_choice_router.flags import is_choice_router_enabled

        env = {k: v for k, v in os.environ.items() if k != "CHOICE_ROUTER"}
        self.assertFalse(is_choice_router_enabled(env))
