"""Reference model for EIS-CONTRACT-FAB-001.

This module models the Conductor-side contract boundary. It does not implement
or emulate proprietary foundry DRC/LVS/DFM rules.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Callable, Dict, List, Optional


CONTRACT_ID = "EIS-CONTRACT-FAB-001"
CONTRACT_VERSION = "0.1.0"


class DecisionStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CONDITIONAL = "CONDITIONAL"
    INCONCLUSIVE = "INCONCLUSIVE"


class LifecycleStatus(str, Enum):
    PREPARED = "PREPARED"
    PREFLIGHT_PASSED = "PREFLIGHT_PASSED"
    SUBMITTED = "SUBMITTED"
    FAB_RECEIVED = "FAB_RECEIVED"
    FAB_UNDER_REVIEW = "FAB_UNDER_REVIEW"
    FAB_ACCEPTED = "FAB_ACCEPTED"
    FAB_REJECTED = "FAB_REJECTED"
    FAB_CONDITIONAL = "FAB_CONDITIONAL"
    FAB_INCONCLUSIVE = "FAB_INCONCLUSIVE"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    MANUFACTURING_RELEASED = "MANUFACTURING_RELEASED"


@dataclass(frozen=True)
class Artifact:
    format: str
    file_name: str
    content: bytes
    top_cell: Optional[str] = None
    dbu_um: Optional[float] = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content).hexdigest()

    @property
    def size_bytes(self) -> int:
        return len(self.content)


@dataclass(frozen=True)
class Submission:
    submission_id: str
    revision: int
    artifact: Artifact
    foundry_name: str
    process: str
    requested_stage: str = "technical-review"
    pdk_identity: Optional[str] = None
    pdk_version: Optional[str] = None
    source_commit: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    message: str
    rule_ref: Optional[str] = None
    cell: Optional[str] = None
    layer: Optional[str] = None
    coordinates: Optional[tuple] = None
    assigned_agent: Optional[str] = None


@dataclass(frozen=True)
class FoundryDecision:
    status: DecisionStatus
    authority: str
    submission_id: str
    artifact_sha256: str
    decided_at: str
    report_ref: Optional[str] = None
    conditions: tuple = ()
    findings: tuple = ()


class ContractError(ValueError):
    """Raised when a submission or foundry response violates the contract."""


def make_submission(submission_id: str, revision: int, content: bytes,
                    foundry_name: str = "MOCK_FOUNDRY",
                    process: str = "MOCK_PROCESS",
                    requested_stage: str = "technical-review") -> Submission:
    if not submission_id or revision < 1:
        raise ContractError("submission_id must be non-empty and revision >= 1")
    artifact = Artifact("OASIS", "candidate.oas", content)
    return Submission(submission_id, revision, artifact, foundry_name,
                      process, requested_stage)


def preflight(submission: Submission) -> None:
    """Check package integrity only; this is not foundry sign-off."""
    if submission.artifact.format != "OASIS":
        raise ContractError("artifact format must be OASIS")
    if not submission.artifact.file_name:
        raise ContractError("artifact file_name must be non-empty")
    if not submission.artifact.content:
        raise ContractError("OASIS artifact content must not be empty")
    if not submission.foundry_name or not submission.process:
        raise ContractError("foundry_name and process are required")
    if submission.requested_stage not in {
        "technical-review", "manufacturing-acceptance", "mask-data-preparation"
    }:
        raise ContractError("unsupported requested_stage")


def validate_decision(submission: Submission, decision: FoundryDecision) -> None:
    """Bind the foundry's response to the exact submitted artifact."""
    if decision.authority != "FOUNDRY":
        raise ContractError("decision authority must be FOUNDRY")
    if decision.submission_id != submission.submission_id:
        raise ContractError("decision submission_id does not match")
    if decision.artifact_sha256 != submission.artifact.sha256:
        raise ContractError("decision artifact hash does not match submitted OASIS")
    if decision.status == DecisionStatus.CONDITIONAL and not decision.conditions:
        raise ContractError("CONDITIONAL decision requires explicit conditions")
    if decision.status == DecisionStatus.REJECTED and not decision.findings:
        raise ContractError("REJECTED decision requires at least one finding")
    if decision.status == DecisionStatus.ACCEPTED and decision.conditions:
        raise ContractError("ACCEPTED decision cannot carry unresolved conditions")


class FoundryAdapter:
    """Transport-neutral adapter protocol; real implementations replace submit()."""

    def submit(self, submission: Submission) -> FoundryDecision:
        raise NotImplementedError


class Conductor:
    def __init__(self, adapter: FoundryAdapter):
        self.adapter = adapter
        self.ledger: List[dict] = []
        self.agent_queue: List[dict] = []
        self.lifecycle: Dict[str, LifecycleStatus] = {}

    def submit(self, submission: Submission) -> FoundryDecision:
        preflight(submission)
        self.lifecycle[submission.submission_id] = LifecycleStatus.PREFLIGHT_PASSED
        self._record("PREFLIGHT_PASSED", submission, "Conductor package checks only")
        self.lifecycle[submission.submission_id] = LifecycleStatus.SUBMITTED
        self._record("SUBMITTED", submission, "Handed to configured adapter")
        decision = self.adapter.submit(submission)
        validate_decision(submission, decision)
        self._record("FOUNDRY_DECISION", submission, decision)
        mapping = {
            DecisionStatus.ACCEPTED: LifecycleStatus.FAB_ACCEPTED,
            DecisionStatus.REJECTED: LifecycleStatus.FAB_REJECTED,
            DecisionStatus.CONDITIONAL: LifecycleStatus.FAB_CONDITIONAL,
            DecisionStatus.INCONCLUSIVE: LifecycleStatus.FAB_INCONCLUSIVE,
        }
        self.lifecycle[submission.submission_id] = mapping[decision.status]
        if decision.status == DecisionStatus.REJECTED:
            self.lifecycle[submission.submission_id] = LifecycleStatus.REVISION_REQUIRED
            for finding in decision.findings:
                self.agent_queue.append({
                    "submission_id": submission.submission_id,
                    "finding_id": finding.finding_id,
                    "assigned_agent": finding.assigned_agent or "design-triage",
                    "message": finding.message,
                    "status": "OPEN",
                })
        return decision

    def record_revision(self, previous: Submission, revised: Submission) -> None:
        if revised.submission_id == previous.submission_id:
            raise ContractError("revision must receive a new submission_id")
        if revised.revision <= previous.revision:
            raise ContractError("revision number must increase")
        if revised.artifact.sha256 == previous.artifact.sha256:
            raise ContractError("revision must change artifact content")
        self._record("REVISION_CREATED", revised, {
            "supersedes": previous.submission_id,
            "previous_sha256": previous.artifact.sha256,
        })

    def authorize_manufacturing_release(self, submission: Submission,
                                       decision: FoundryDecision) -> None:
        validate_decision(submission, decision)
        if decision.status != DecisionStatus.ACCEPTED:
            raise ContractError("only exact-submission FOUNDRY ACCEPTED can pass this gate")
        # This records a gate result only; commercial/operational release remains fab-owned.
        self.lifecycle[submission.submission_id] = LifecycleStatus.FAB_ACCEPTED
        self._record("ACCEPTANCE_GATE_SATISFIED", submission,
                     "Foundry acceptance recorded; manufacturing release remains separate")

    def _record(self, event: str, submission: Submission, detail) -> None:
        self.ledger.append({
            "contract_id": CONTRACT_ID,
            "contract_version": CONTRACT_VERSION,
            "event": event,
            "submission_id": submission.submission_id,
            "revision": submission.revision,
            "artifact_sha256": submission.artifact.sha256,
            "at": datetime.now(timezone.utc).isoformat(),
            "detail": detail if isinstance(detail, str) else (
                asdict(detail) if isinstance(detail, FoundryDecision) else detail
            ),
        })
