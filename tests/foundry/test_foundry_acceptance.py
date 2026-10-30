"""Tests for EIS-CONTRACT-FAB-001 mock foundry loop."""
import unittest

from harness.foundry_contract import (
    Conductor, ContractError, DecisionStatus, make_submission
)
from harness.mock_foundry import MockFoundryAdapter


class FoundryAcceptanceTests(unittest.TestCase):
    def test_accept_reject_conditional_and_revision_loop(self):
        adapter = MockFoundryAdapter([
            DecisionStatus.ACCEPTED,
            DecisionStatus.REJECTED,
            DecisionStatus.CONDITIONAL,
        ])
        conductor = Conductor(adapter)

        accepted = make_submission("EIS-FAB-DEMO-R001", 1, b"oasis-candidate-one")
        accepted_decision = conductor.submit(accepted)
        self.assertEqual(accepted_decision.status, DecisionStatus.ACCEPTED)
        conductor.authorize_manufacturing_release(accepted, accepted_decision)

        rejected = make_submission("EIS-FAB-DEMO-R002", 2, b"oasis-candidate-two")
        rejected_decision = conductor.submit(rejected)
        self.assertEqual(rejected_decision.status, DecisionStatus.REJECTED)
        self.assertEqual(conductor.lifecycle[rejected.submission_id].value, "REVISION_REQUIRED")
        self.assertEqual(conductor.agent_queue[0]["assigned_agent"], "photonic-layout")

        revised = make_submission("EIS-FAB-DEMO-R003", 3, b"oasis-candidate-two-fixed")
        conductor.record_revision(rejected, revised)
        conditional = conductor.submit(revised)
        self.assertEqual(conditional.status, DecisionStatus.CONDITIONAL)
        self.assertTrue(conditional.conditions)
        self.assertNotEqual(rejected.artifact.sha256, revised.artifact.sha256)
        self.assertEqual(len(adapter.calls), 3)
        self.assertEqual(len(conductor.ledger), 8)

    def test_decision_must_match_exact_artifact_hash(self):
        adapter = MockFoundryAdapter([DecisionStatus.ACCEPTED])
        conductor = Conductor(adapter)
        submission = make_submission("EIS-FAB-HASH-R001", 1, b"submitted-oasis")
        decision = adapter.submit(submission)
        tampered = make_submission("EIS-FAB-HASH-R001", 1, b"changed-after-submit")
        with self.assertRaises(ContractError):
            conductor.authorize_manufacturing_release(tampered, decision)

    def test_conditional_is_not_manufacturing_acceptance(self):
        adapter = MockFoundryAdapter([DecisionStatus.CONDITIONAL])
        conductor = Conductor(adapter)
        submission = make_submission("EIS-FAB-COND-R001", 1, b"oasis-conditional")
        decision = conductor.submit(submission)
        with self.assertRaises(ContractError):
            conductor.authorize_manufacturing_release(submission, decision)

    def test_revision_requires_new_identity_and_changed_content(self):
        adapter = MockFoundryAdapter([])
        conductor = Conductor(adapter)
        original = make_submission("EIS-FAB-REV-R001", 1, b"original")
        same_id = make_submission("EIS-FAB-REV-R001", 2, b"changed")
        with self.assertRaises(ContractError):
            conductor.record_revision(original, same_id)
        same_content = make_submission("EIS-FAB-REV-R002", 2, b"original")
        with self.assertRaises(ContractError):
            conductor.record_revision(original, same_content)


if __name__ == "__main__":
    unittest.main()
