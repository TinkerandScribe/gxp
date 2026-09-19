"""Named incomplete_evidence path runs before Jev; fail-border is documented."""

from __future__ import annotations

import unittest

from jev_pilot_b.cascade import cascade
from jev_pilot_b.predisposition import (
    DEFAULT_FAIL_BORDER_MID,
    DEFAULT_NO_AT_OR_BELOW,
    FAIL_BORDER_HANDOFF,
    INCOMPLETE_EVIDENCE_PATH,
    apply_fail_border_handoff,
    apply_incomplete_evidence_path,
)
from jev_pilot_b.providers.jev import JevCheckResponse, JevProvider
from jev_pilot_b.providers.rules import RulesProvider
from jev_pilot_b.types import DecideInput, DecideResult


class RecordingJev:
    name = "jev"

    def __init__(self) -> None:
        self.calls = 0

    async def decide(self, input: DecideInput) -> DecideResult:
        self.calls += 1
        _ = input
        return DecideResult(
            decision="fail",
            provider="jev",
            latency_ms=1.0,
            abstained=False,
            p=0.12,
        )


class FakeCheckClient:
    def __init__(self, response: JevCheckResponse) -> None:
        self.response = response
        self.calls = 0

    def check(self, request) -> JevCheckResponse:
        self.calls += 1
        _ = request
        return self.response


class TestIncompleteEvidencePath(unittest.IsolatedAsyncioTestCase):
    def test_path_name_is_stable(self) -> None:
        self.assertEqual(INCOMPLETE_EVIDENCE_PATH, "incomplete_evidence")

    def test_predisposition_fires_before_any_provider(self) -> None:
        inp = DecideInput(
            artifact={"evidence_complete": False, "body": "redacted traction"},
            question="The packet includes a countable proof-of-product with N and a dated window.",
        )
        early = apply_incomplete_evidence_path(inp)
        self.assertIsNotNone(early)
        assert early is not None
        self.assertEqual(early.decision, "needs_review")
        self.assertEqual(early.provider, "rules")
        self.assertFalse(early.abstained)
        self.assertEqual(early.raw["path"], INCOMPLETE_EVIDENCE_PATH)

    def test_predisposition_abstains_on_plain_string(self) -> None:
        self.assertIsNone(
            apply_incomplete_evidence_path(
                DecideInput(artifact="doc", question="q")
            )
        )

    async def test_cascade_does_not_reach_jev_when_path_fires(self) -> None:
        jev = RecordingJev()
        result = await cascade(
            [RulesProvider(), jev],
            DecideInput(
                artifact={"evidence_pack": []},
                question="Evidence names at least one measured conversion count with identifiers.",
            ),
        )
        self.assertEqual(jev.calls, 0)
        self.assertEqual(result.provider, "rules")
        self.assertEqual(result.decision, "needs_review")
        self.assertEqual(result.raw["path"], INCOMPLETE_EVIDENCE_PATH)
        self.assertFalse(result.abstained)


class TestFailBorderHandoff(unittest.IsolatedAsyncioTestCase):
    def test_band_constants_are_documented_defaults(self) -> None:
        self.assertEqual(DEFAULT_NO_AT_OR_BELOW, 0.3)
        self.assertEqual(DEFAULT_FAIL_BORDER_MID, 0.5)
        self.assertEqual(FAIL_BORDER_HANDOFF, "fail_border_handoff")

    def test_fail_inside_open_band_routes_needs_review(self) -> None:
        raw_fail = DecideResult(
            decision="fail",
            provider="jev",
            latency_ms=1.0,
            abstained=False,
            p=0.41,
            raw={"verdict": "no"},
        )
        out = apply_fail_border_handoff(raw_fail)
        self.assertEqual(out.decision, "needs_review")
        self.assertTrue(out.raw["fail_border_handoff"])
        self.assertEqual(out.raw["path"], FAIL_BORDER_HANDOFF)

    def test_confident_fail_stays_fail(self) -> None:
        raw_fail = DecideResult(
            decision="fail",
            provider="jev",
            latency_ms=1.0,
            abstained=False,
            p=0.2,
        )
        out = apply_fail_border_handoff(raw_fail)
        self.assertEqual(out.decision, "fail")

    def test_endpoints_of_open_interval_do_not_handoff(self) -> None:
        low = DecideResult(
            decision="fail",
            provider="jev",
            latency_ms=0.0,
            abstained=False,
            p=0.3,
        )
        high = DecideResult(
            decision="fail",
            provider="jev",
            latency_ms=0.0,
            abstained=False,
            p=0.5,
        )
        self.assertEqual(apply_fail_border_handoff(low).decision, "fail")
        self.assertEqual(apply_fail_border_handoff(high).decision, "fail")

    async def test_jev_provider_applies_fail_border_by_default(self) -> None:
        client = FakeCheckClient(
            JevCheckResponse(verdict="no", probability_yes=0.44)
        )
        result = await JevProvider(client).decide(
            DecideInput(artifact="x", question="q")
        )
        self.assertEqual(result.decision, "needs_review")
        self.assertEqual(result.p, 0.44)
        self.assertTrue(result.raw["fail_border_handoff"])

    async def test_jev_provider_can_disable_fail_border(self) -> None:
        client = FakeCheckClient(
            JevCheckResponse(verdict="no", probability_yes=0.44)
        )
        result = await JevProvider(client, fail_border_handoff=False).decide(
            DecideInput(artifact="x", question="q")
        )
        self.assertEqual(result.decision, "fail")
