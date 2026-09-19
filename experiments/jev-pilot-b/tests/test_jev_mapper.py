"""jev_check verdict mapping and optional uncertain abstention."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from jev_pilot_b.providers.jev import (
    HttpJevCheckClient,
    JevCheckRequest,
    JevCheckResponse,
    JevProvider,
    MissingApiKeyError,
    map_check_verdict,
    read_api_key_from_env,
    verdict_from_probability,
)
from jev_pilot_b.types import DecideInput


class FakeCheckClient:
    def __init__(self, response: JevCheckResponse) -> None:
        self.response = response
        self.requests: list[JevCheckRequest] = []

    def check(self, request: JevCheckRequest) -> JevCheckResponse:
        self.requests.append(request)
        return self.response


class TestJevMapper(unittest.TestCase):
    def test_uncertain_maps_to_needs_review(self) -> None:
        decision, abstained = map_check_verdict(
            {"verdict": "uncertain", "probability_yes": 0.51}
        )
        self.assertEqual(decision, "needs_review")
        self.assertFalse(abstained)

    def test_yes_pass_no_fail(self) -> None:
        self.assertEqual(map_check_verdict({"verdict": "yes", "probability_yes": 0.9}), ("pass", False))
        self.assertEqual(map_check_verdict({"verdict": "no", "probability_yes": 0.1}), ("fail", False))

    def test_uncertain_can_abstain_when_configured(self) -> None:
        decision, abstained = map_check_verdict(
            {"verdict": "uncertain", "probability_yes": 0.5},
            abstain_on_uncertain=True,
        )
        self.assertEqual(decision, "needs_review")
        self.assertTrue(abstained)

    def test_probability_bands(self) -> None:
        self.assertEqual(verdict_from_probability(0.7), "yes")
        self.assertEqual(verdict_from_probability(0.3), "no")
        self.assertEqual(verdict_from_probability(0.5), "uncertain")


class TestJevProvider(unittest.IsolatedAsyncioTestCase):
    async def test_provider_maps_mcp_response(self) -> None:
        client = FakeCheckClient(
            JevCheckResponse(verdict="uncertain", probability_yes=0.44)
        )
        provider = JevProvider(client)
        result = await provider.decide(
            DecideInput(
                artifact="diff",
                question="Does ISC 1 hold?",
                yes_means="criterion is met",
                no_means="criterion is violated",
            )
        )
        self.assertEqual(result.decision, "needs_review")
        self.assertEqual(result.provider, "jev")
        self.assertFalse(result.abstained)
        self.assertEqual(result.p, 0.44)
        self.assertEqual(client.requests[0].question, "Does ISC 1 hold?")
        self.assertEqual(client.requests[0].to_mcp_arguments()["yes_means"], "criterion is met")

    async def test_provider_abstains_on_uncertain_when_configured(self) -> None:
        client = FakeCheckClient(
            JevCheckResponse(verdict="uncertain", probability_yes=0.55)
        )
        result = await JevProvider(client, abstain_on_uncertain=True).decide(
            DecideInput(artifact="x", question="q")
        )
        self.assertTrue(result.abstained)
        self.assertEqual(result.decision, "needs_review")


class TestKeyHandling(unittest.TestCase):
    def test_reads_jev_api_key_then_typesafe(self) -> None:
        self.assertEqual(read_api_key_from_env({"JEV_API_KEY": "abc"}), "abc")
        self.assertEqual(read_api_key_from_env({"TYPESAFE_API_KEY": "xyz"}), "xyz")
        self.assertIsNone(read_api_key_from_env({}))

    def test_http_client_refuses_missing_key(self) -> None:
        client = HttpJevCheckClient()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(MissingApiKeyError):
                client.check(JevCheckRequest(state="s", question="q?"))
