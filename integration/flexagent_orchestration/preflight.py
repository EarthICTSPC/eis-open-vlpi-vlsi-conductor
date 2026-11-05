"""Fail-closed capability preflight for the EIS FlexAgent integration.

This module does not invoke a simulator. It decides whether the configured
provider has the minimum declared interface needed for an actual execution
attempt. Documentation search is knowledge access, not simulation dispatch.
"""
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class GateStatus(str, Enum):
    READY_TO_DISPATCH = "READY_TO_DISPATCH"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ProviderProfile:
    """Capabilities observed from a configured provider, not inferred from its name."""

    endpoint_configured: bool
    tool_names: FrozenSet[str]
    provider_id: str | None = None
    provider_version: str | None = None
    pdk_id: str | None = None
    pdk_revision: str | None = None


@dataclass(frozen=True)
class PreflightResult:
    status: GateStatus
    reason_codes: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    dispatch_authorized: bool = False
    simulation_claim_permitted: bool = False


REQUIRED_EXECUTION_CAPABILITIES = frozenset(
    {"submit_simulation", "get_job_status", "get_job_result"}
)


def evaluate_provider(profile: ProviderProfile) -> PreflightResult:
    """Check the minimum interface needed before an execution attempt.

    This deliberately does not treat documentation search as execution and
    never claims a simulation occurred. READY_TO_DISPATCH is only permission
    to attempt a real dispatch, not evidence of a completed run.
    """
    reasons: list[str] = []
    missing: list[str] = []

    if not profile.endpoint_configured:
        reasons.append("PROVIDER_ENDPOINT_NOT_CONFIGURED")

    missing.extend(sorted(REQUIRED_EXECUTION_CAPABILITIES - profile.tool_names))

    if not profile.provider_id:
        reasons.append("PROVIDER_ID_UNPINNED")
    if not profile.provider_version:
        reasons.append("PROVIDER_VERSION_UNPINNED")
    if not profile.pdk_id:
        reasons.append("PDK_IDENTITY_MISSING")
    if not profile.pdk_revision:
        reasons.append("PDK_REVISION_MISSING")

    if missing:
        reasons.append("EXECUTION_INTERFACE_INCOMPLETE")
    if "search_flexcompute_docs" in profile.tool_names and missing:
        reasons.append("DOCUMENTATION_SEARCH_IS_NOT_EXECUTION")

    blocked = bool(reasons or missing)
    return PreflightResult(
        status=GateStatus.BLOCKED if blocked else GateStatus.READY_TO_DISPATCH,
        reason_codes=tuple(sorted(set(reasons))),
        missing_capabilities=tuple(missing),
        dispatch_authorized=not blocked,
        # Preflight can never establish that a simulation has run.
        simulation_claim_permitted=False,
    )
