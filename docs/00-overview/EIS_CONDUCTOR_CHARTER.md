# EIS Conductor Charter

**Owner:** Earth ICT, SPC (EIS)  
**Status:** Initial operating charter — proposed for review  
**Applies to:** Public EIS engineering repository and authorized connected agents/tools

## 1. Purpose

The EIS Conductor is the coordinating authority for a versioned, evidence-controlled engineering process. Its purpose is to let EIS and authorized agents retrieve and reuse engineering history without requiring Art Scott to repeatedly teach the same source interpretations, contract boundaries, tool lessons, and acceptance rules.

The Conductor is not an autonomous engineer with authority to redefine EIS objectives. It is the system that remembers, plans, delegates, verifies, records, and escalates.

## 2. Engineering chain

The Conductor maintains traceability across this chain:

```text
Need / requirement
      ↓
Source and prior-art interpretation
      ↓
Mathematical abstraction / formal contract
      ↓
Backend-neutral representation and RU
      ↓
Backend-specific lowering
      ↓
Execution (test / simulation / layout / measurement)
      ↓
Independent verification against the contract
      ↓
Evidence record and decision
      ↓
Approved next action
```

A link is not presumed to exist because two artifacts are related by topic. Each link must be explicit, versioned, and supported by an identified source, contract, artifact, or decision.

EIS distinguishes mathematical lifting from engineering lowering. Preserve the vocabulary and ownership boundaries used by the relevant workstream.

## 3. Roles and decision rights

| Role | Responsibility | Authority boundary |
|---|---|---|
| EIS engineering authority | Sets objectives, risk tolerance, budgets, IP/disclosure policy, acceptance and consequential decisions | Retains human authority |
| EIS Conductor | Maintains project state, traceability, task orchestration, evidence ledger, approval gates and decision history | Cannot change EIS intent or self-authorize gated work |
| Source/lifting agent | Retrieves and analyzes publications, supplementary information, and formal abstractions | May propose interpretations; source ambiguity remains visible |
| Lowering agent | Produces backend-specific implementations and executes bounded tool workflows | Must preserve the approved contract; cannot redefine it |
| Verification agent | Independently checks artifacts and evidence against acceptance criteria | Must be independent of the claim being checked where practicable |
| Evidence agent | Validates provenance, hashes, schemas, logs and immutable references | Records facts; does not invent missing evidence |
| External tool/simulator/foundry | Produces tool-specific output or authoritative process/measurement evidence within its remit | Its output is not automatically an EIS acceptance decision |

## 4. Persistent engineering memory

GitHub is the public, versioned system of record for material authorized for disclosure. It stores:
- source manifests and interpretation decisions;
- requirements, mathematical contracts, Lean definitions and proofs;
- RU and backend-neutral representations;
- lowering specifications, adapters, notebooks and pinned toolchains;
- experiment inputs, outputs, logs, tests and hashes;
- evidence classifications, verification findings and acceptance decisions;
- unresolved gaps, rejected approaches, and decision history.

The Conductor is the system of action that reads and updates this record through reviewed changes. MCP is a transport/integration mechanism, not the source of EIS semantics or governance.

The memory must be useful to a cold-start agent. A new agent should be able to answer:
1. Where did this requirement or design decision come from?
2. Which source and interpretation support it?
3. Which contract and revision define intended behavior?
4. Which lowering and toolchain produced the artifact?
5. What evidence supports the result, and who independently checked it?
6. What remains assumed, unresolved, blocked, or not run?

## 5. Evidence and provenance are separate dimensions

A single status field must not conflate provenance with validation.

For example, `tian_fitted` describes the origin/class of a value; `computationally-demonstrated` describes the kind of evidence produced by an execution. Neither implies the other.

Retain established repository taxonomies, including `eis.ledger.v0.1` where used, and the evidence states in the repository's disclosure doctrine and evidence schema. New schemas must be additive or explicitly versioned; do not silently reinterpret existing fields.

A result is accepted only after the Conductor applies the relevant contract-specific checks. The result of that gate is:
- `ACCEPT`: all required evidence and checks pass;
- `REJECT`: evidence contradicts a requirement or violates the task/contract;
- `INCONCLUSIVE`: evidence is missing, ambiguous, insufficient, or not independently verified.

## 6. Autonomy levels

### Routine — bounded execution

Agents may inspect repository material, summarize, draft on a branch, run deterministic local tests, validate schemas, calculate declared metrics, and prepare reports within an approved task.

### Engineering judgment — approval required

Human review is required before changing physical assumptions, selecting among competing device models, changing tolerances, revising canonical abstractions, or changing the interpretation of source evidence.

### Consequential — explicit authorization required

Human authorization is required for spending, paid/external compute, foundry or partner disclosure, NDA data use, PDK transfers, fabrication/MPW, procurement, IP/legal decisions, public performance claims, contract acceptance, and merging.

## 7. Public and controlled memory

The public repository may contain public sources, EIS-owned abstractions/contracts, authorized interfaces, sanitized evidence manifests, hashes, reproducible tests, and approved results.

Controlled environments must retain NDA PDKs, proprietary process rules, restricted compact models, credentials, confidential raw data, and any artifact not authorized for public or agent processing. Public metadata may identify a controlled dependency only when disclosure is permitted.

## 8. GitHub operating rules

- `main` is the reviewed public baseline.
- Agents work through task branches and pull requests.
- PRs are proposals until reviewed and merged by an authorized maintainer.
- Do not close, merge, retarget, or rewrite unrelated open work as part of a memory refresh.
- Preserve the history of failed, superseded, and unresolved work; link it rather than erasing it.
- Evidence records should be append-only in meaning. Corrections create a superseding record with a link to the prior record.

## 9. Initial implementation sequence

1. Establish this charter, cold-start instructions, and a navigable engineering memory index.
2. Add a versioned task/result envelope that binds each agent invocation to a contract revision, input hashes, tool identity, scope, approval state, and required evidence.
3. Validate the envelope and evidence independently; reject malformed, stale, mismatched, or self-certified results.
4. Demonstrate one source → contract → lowering → execution → verification → evidence chain.
5. Connect GitHub first, then authorized specialist agents/tools such as Lean, Python, PhotonForge, and Tidy3D.
6. Add dashboards or automation only after the records and acceptance rules are stable.

## 10. Initial acceptance test

A cold-start agent with access to this repository, but not the originating chat, must be able to reconstruct one selected workstream's source basis, current contract, active lowering, evidence status, open gaps, and next authorized action using the memory index and linked records.

The Conductor succeeds when it reduces repetitive human briefing while preserving human judgment and evidence integrity.
