import unittest

from integration.flexagent_orchestration.preflight import (
    GateStatus,
    ProviderProfile,
    evaluate_provider,
)


class FlexAgentPreflightTests(unittest.TestCase):
    def test_docs_only_mcp_is_blocked_and_names_missing_execution_tools(self):
        result = evaluate_provider(
            ProviderProfile(
                endpoint_configured=True,
                tool_names=frozenset({"search_flexcompute_docs"}),
                provider_id="flexagent-mcp",
                provider_version="observed-docs-only",
                pdk_id="LIGENTEC_AN800_TFLN",
                pdk_revision="not-yet-pinned",
            )
        )
        self.assertEqual(result.status, GateStatus.BLOCKED)
        self.assertIn("submit_simulation", result.missing_capabilities)
        self.assertIn("get_job_status", result.missing_capabilities)
        self.assertIn("get_job_result", result.missing_capabilities)
        self.assertIn("DOCUMENTATION_SEARCH_IS_NOT_EXECUTION", result.reason_codes)
        self.assertFalse(result.dispatch_authorized)
        self.assertFalse(result.simulation_claim_permitted)

    def test_missing_endpoint_is_blocked_even_if_tool_names_are_present(self):
        result = evaluate_provider(
            ProviderProfile(
                endpoint_configured=False,
                tool_names=frozenset({
                    "submit_simulation", "get_job_status", "get_job_result"
                }),
                provider_id="provider",
                provider_version="1.0",
                pdk_id="test-pdk",
                pdk_revision="rev1",
            )
        )
        self.assertEqual(result.status, GateStatus.BLOCKED)
        self.assertIn("PROVIDER_ENDPOINT_NOT_CONFIGURED", result.reason_codes)
        self.assertFalse(result.dispatch_authorized)
        self.assertFalse(result.simulation_claim_permitted)

    def test_complete_profile_only_authorizes_attempt_not_a_simulation_claim(self):
        result = evaluate_provider(
            ProviderProfile(
                endpoint_configured=True,
                tool_names=frozenset({
                    "submit_simulation", "get_job_status", "get_job_result"
                }),
                provider_id="provider",
                provider_version="1.0",
                pdk_id="test-pdk",
                pdk_revision="rev1",
            )
        )
        self.assertEqual(result.status, GateStatus.READY_TO_DISPATCH)
        self.assertTrue(result.dispatch_authorized)
        self.assertFalse(result.simulation_claim_permitted)

    def test_unpinned_provider_or_pdk_is_blocked(self):
        result = evaluate_provider(
            ProviderProfile(
                endpoint_configured=True,
                tool_names=frozenset({
                    "submit_simulation", "get_job_status", "get_job_result"
                }),
            )
        )
        self.assertEqual(result.status, GateStatus.BLOCKED)
        self.assertIn("PROVIDER_VERSION_UNPINNED", result.reason_codes)
        self.assertIn("PDK_IDENTITY_MISSING", result.reason_codes)
        self.assertIn("PDK_REVISION_MISSING", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
