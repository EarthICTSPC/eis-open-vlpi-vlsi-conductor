"""Deterministic mock foundry for EIS-CONTRACT-FAB-001 tests and demo.

The adapter returns scripted decisions. It does not run DRC, LVS, DFM or
simulate any real foundry's process or acceptance behavior.
"""
from datetime import datetime, timezone
from typing import Iterable

from foundry_contract import (
    DecisionStatus, Finding, FoundryAdapter, FoundryDecision, Submission
)


class MockFoundryAdapter(FoundryAdapter):
    def __init__(self, decisions: Iterable[DecisionStatus]):
        self.decisions = list(decisions)
        self.calls = []

    def submit(self, submission: Submission) -> FoundryDecision:
        if not self.decisions:
            raise RuntimeError("mock decision script exhausted")
        status = self.decisions.pop(0)
        self.calls.append(submission)
        common = {
            "authority": "FOUNDRY",
            "submission_id": submission.submission_id,
            "artifact_sha256": submission.artifact.sha256,
            "decided_at": datetime.now(timezone.utc).isoformat(),
            "report_ref": "mock://reports/" + submission.submission_id,
        }
        if status == DecisionStatus.ACCEPTED:
            return FoundryDecision(status=status, **common)
        if status == DecisionStatus.REJECTED:
            return FoundryDecision(
                status=status,
                findings=(Finding(
                    finding_id="MOCK-DRC-001",
                    severity="ERROR",
                    message="Illustrative spacing rule violation; no real geometry was checked.",
                    rule_ref="MOCK-RULE-SPACING",
                    cell="TOP",
                    layer="WG",
                    coordinates=(10.0, 20.0),
                    assigned_agent="photonic-layout",
                ),),
                **common,
            )
        if status == DecisionStatus.CONDITIONAL:
            return FoundryDecision(
                status=status,
                conditions=("Provide the missing packaging interface-control document.",
                            "Confirm the requested handoff stage with foundry engineering."),
                **common,
            )
        return FoundryDecision(
            status=DecisionStatus.INCONCLUSIVE,
            conditions=("Mock evidence package is incomplete.",),
            **common,
        )
