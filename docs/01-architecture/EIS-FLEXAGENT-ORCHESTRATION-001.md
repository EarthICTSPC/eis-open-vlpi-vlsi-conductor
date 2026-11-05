# EIS-FLEXAGENT-ORCHESTRATION-001 — Execution-path preflight

**Owner:** Earth ICT, SPC (EIS)  
**Status:** prototype preflight; execution endpoint not yet verified  
**Evidence class:** source-level implementation and unit tests; not a FlexCompute simulation  
**Purpose:** prove that the EIS control path can make a deterministic, fail-closed decision about whether a configured FlexAgent/FlexCompute provider is actually dispatchable.

## Acceptance question

Can the EIS conductor distinguish documentation/knowledge access from an executable simulation interface, block when the interface is absent, and avoid recording a run that did not happen?

## Required execution capabilities

The preflight requires an explicitly configured endpoint and the following capabilities:

- `submit_simulation`: submit a real supported simulation request and receive a provider job identifier.
- `get_job_status`: reconcile queued, running, completed, failed, and unknown/in-flight jobs.
- `get_job_result`: retrieve the result and provider-reported status for the same job.

These are EIS adapter capability names, not claims that FlexAgent MCP currently exposes tools with these exact names. A provider-specific adapter must map real documented tools/APIs to these capabilities and preserve request/job identity.

The provider and PDK identity/revision must be pinned. Documentation search (including a tool such as `search_flexcompute_docs`) does not satisfy any execution capability.

## State and claim boundaries

- `BLOCKED`: no dispatch authorization; record reason codes and missing capabilities.
- `READY_TO_DISPATCH`: preflight only. This is permission to attempt a real dispatch, not proof a dispatch occurred.
- `SIMULATION_DISPATCHED`: may be recorded only after a real provider submission returns a durable provider job ID and the EIS run ledger records the request/configuration.
- `IN_FLIGHT`, `TIMED_OUT_UNKNOWN`, `FAILED`, `COMPLETED`: must be reconciled against the same provider job ID. A timeout is not evidence that no job exists and must not cause a blind duplicate dispatch.
- Simulation results never count as physical measurements.

## Test coverage

The unit tests verify that:
1. documentation-search-only capability is blocked and names the missing execution tools;
2. an absent endpoint is blocked even if tool names are declared;
3. a complete profile only authorizes an attempt and cannot authorize a simulation claim; and
4. unpinned provider/PDK identity is blocked.

The tests use synthetic provider profiles and make no network calls. They validate the EIS preflight logic, not FlexCompute service availability, actual MCP tool discovery, simulator execution, PDK compatibility, or physical performance.

## Current integration status

In the ChatGPT execution environment used to prepare this artifact, the available connected tools expose GitHub operations but no callable FlexAgent/FlexCompute simulation endpoint. Therefore no real FlexAgent discovery, submission, or simulation has been performed in this turn. The missing integration is a configured provider endpoint plus a verified adapter mapping to actual submission, status/reconciliation, and result-retrieval interfaces. If the installed FlexAgent MCP offers only documentation search, the correct status is `BLOCKED`, not a simulated success.
