# EIS-CONTRACT-FAB-001 — Foundry Acceptance Contract

**Version:** 0.1.0  
**Status:** Proposed / executable reference  
**Authority:** Earth ICT, SPC (EIS)  
**Scope:** Foundry-neutral submission, independent acceptance, feedback and iteration contract.

## 1. Purpose

Define the boundary between design orchestration and manufacturing authority. The EIS Conductor prepares and tracks a candidate physical-design submission. The foundry independently evaluates that exact submission under its own process, PDK, rule decks and controlled procedures.

**The designer designs. The Conductor coordinates. The foundry decides.**

This contract does not require a foundry to expose an MCP server. An approved portal, secure file exchange, API, MCP endpoint or human-mediated process may implement the transport. Transport does not change the authority model.

## 2. Non-delegable foundry authority

The Conductor's preflight is not foundry sign-off. Designer, agent, third-party EDA and Conductor PASS results cannot override a foundry finding.

The foundry owns:
- applicable process and acceptance criteria;
- proprietary DRC, LVS, DFM and process checks;
- interpretation of its own reports;
- waiver approval;
- acceptance for a specifically identified handoff stage;
- authorization for mask preparation, wafer start or other manufacturing release.

A foundry ACCEPTED decision applies only to the exact submission ID, artifact checksum, process identity and handoff stage named in that decision. ACCEPTED does not automatically mean manufacturing has started or is authorized.

## 3. Submission identity and manifest

Every submission is immutable and uniquely identified. Its manifest binds:
- submission ID and revision;
- OASIS file name, byte size and SHA-256;
- top-cell and database-unit metadata when known;
- foundry and process identity;
- PDK identity/version where disclosure is permitted;
- source revision and design context;
- evidence references and tool provenance;
- requested handoff stage.

The Conductor must not fabricate missing PDK details, infer a foundry PASS from its own checks, or label an unrun check as PASS.

## 4. Decision vocabulary

| Decision | Meaning |
|---|---|
| ACCEPTED | Foundry's stated acceptance requirements for the named handoff stage are satisfied. |
| REJECTED | One or more mandatory foundry requirements are not satisfied. |
| CONDITIONAL | The foundry identifies explicit conditions or approvals that remain outstanding. |
| INCONCLUSIVE | The foundry cannot determine acceptance from the available checks or evidence. |

Transport/processing states such as SUBMITTED, RECEIVED and UNDER_REVIEW are lifecycle states, not acceptance decisions.

A decision must identify the exact submission ID and SHA-256 it evaluates. A decision for one revision cannot be carried forward to a later revision.

## 5. Feedback and iteration

For REJECTED, CONDITIONAL or INCONCLUSIVE outcomes, the Conductor records findings and routes them to the responsible design, PDK, verification, packaging or submission agent.

A revision creates a new submission ID and checksum. Previous submissions, reports, findings, decisions and waivers remain in the audit history.

The mock implementation demonstrates:
1. an ACCEPTED outcome;
2. a REJECTED outcome with findings routed to an agent;
3. a revised immutable submission;
4. a CONDITIONAL outcome with explicit open conditions.

The mock is a protocol test fixture, not a foundry model and not evidence of manufacturability.

## 6. Waivers

A waiver is valid only when explicitly approved by an authorized foundry authority for a named finding, artifact revision, process and scope. Agent suggestions or Conductor state changes are not waivers. Original findings remain in the record.

## 7. Security and confidentiality

The Conductor uses only foundry-authorized channels and credentials. Proprietary PDK contents, process rules, compact models and reports remain subject to the foundry's access and confidentiality controls. The contract does not require disclosure of proprietary rule decks.

Agent access is scoped to the minimum authorized information and action. A foundry may require checks to run entirely inside its controlled environment.

## 8. Acceptance criteria for this reference implementation

- A submission is bound to a content hash.
- A mock foundry decision is bound to the exact submitted ID and hash.
- ACCEPTED, REJECTED and CONDITIONAL are exercised by automated tests.
- Rejected findings are assigned to a responsible agent.
- A revision receives a new ID and hash.
- A decision for an old hash cannot accept a changed artifact.
- CONDITIONAL does not silently become ACCEPTED or manufacturing release.
- The complete interaction is reproducible without TSMC, GlobalFoundries or any privileged foundry access.

## 9. Future adapter boundary

Implementations may provide:
- MCP adapter, if explicitly supported and authorized by the foundry;
- REST/API adapter;
- secure file-exchange adapter;
- human-mediated portal adapter.

All adapters normalize responses to the same contract decision and finding model. No adapter is permitted to synthesize a foundry decision that the foundry did not issue.

## 10. Foundational rule

**The Conductor coordinates. The designer designs. The foundry decides.**
