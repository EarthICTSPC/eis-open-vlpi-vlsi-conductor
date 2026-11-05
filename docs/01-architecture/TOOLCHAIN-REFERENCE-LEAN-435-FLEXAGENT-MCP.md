# Toolchain references: Lean 4.35.0 and FlexAgent MCP

**Project:** Earth ICT, SPC (EIS)  
**Status:** reviewed references; adoption and live integration not yet verified  
**Purpose:** record two relevant upstream capabilities and their implications for the EIS formal-contract → Python adapter → photonics-agent workflow.

## 1. Lean 4.35.0

**Primary source:** https://lean-lang.org/doc/reference/latest/releases/v4.35.0/#release-v4___35___0  
**Release date shown by upstream:** 12 October 2026.

### Relevant upstream changes

The release notes identify these changes as especially relevant to EIS verification:

- **`lake check`** builds default project targets, exports them, replays the export through Lean's kernel, and rejects non-standard axioms. It is designed to check a project as untrusted input. The sandbox described in the release notes is currently Linux-only.
- **`lake check --paranoid`** additionally invokes the external checkers bundled with the release, accepting only if all of them accept.
- **`lake comparator`** compares named theorem statements in a challenge module with a solution module, checks the permitted axiom set, and kernel-checks the result. This may support a future EIS separation between normative theorem statements and implementation/proof modules.
- **`vcgen`** is the newer, more general successor to `mvcgen`, with support for deeply embedded languages and generalized assertion languages. The release notes explicitly mark it experimental; EIS must not make it a required trusted-path dependency without a separate evaluation.
- Other changes include improved `grind` support for bit-vectors/fixed-width integer arithmetic and `lake build --fail-fast`.

### EIS application — proposed, not yet adopted

1. Inventory the repositories' pinned Lean toolchains before changing versions.
2. Test `lake check` and, where the Linux environment and build permit, `lake check --paranoid` in a dedicated CI job. Preserve the existing project build and tests; this is an additional verification layer, not a replacement.
3. Evaluate `lake comparator` for high-value normative acceptance theorems (for example, dispatch authorization, evidence-level boundaries, and units/conformance decisions). Pin the permitted axiom list explicitly.
4. Treat `vcgen` as an experiment behind a separate job until its experimental status and compatibility with the EIS toolchain are reviewed.
5. Record Lean version, Lake version, dependency revisions, command line, exit status, logs, and exported artifacts in the evidence ledger.

A successful `lake check` establishes kernel acceptance under its stated conditions; it does not prove that a Python adapter, external simulation, PDK, physical device, or run ledger corresponds to the theorem's model. A theorem comparison likewise establishes statement/proof correspondence within the configured comparison—not physical truth.

## 2. FlexAgent MCP

**Primary source:** https://hs.flexcompute.com/blog/learn-about-flexagent  
**Publication date shown by upstream:** 3 November 2025.

### What the source explicitly documents

The article says the FlexAgent MCP is part of FlexCompute's `flexagent-services` API and exposes one tool, `search_flexcompute_docs`, to search documentation for Tidy3D, PhotonForge, Flow360, and external libraries including `gdstk`. It describes use through Cursor/VS Code agent integrations and Tidy3D extensions, including workflows for learning, troubleshooting, customizing/building simulation setups, and analyzing results.

The article also says an agent may need an explicit instruction such as “Use flexagent to …” or repository-level `AGENTS.md` guidance to promote use of the MCP. It warns that MCP tool/context proliferation can confuse an agent and that MCP-provided context can pose a security risk.

**Important scope distinction:** the documented `search_flexcompute_docs` tool is a documentation-search interface. The article's broader description of agent-assisted simulation workflows does not, by itself, establish that this MCP tool submits simulation jobs, checks their status, or retrieves completed results. Those execution capabilities must be independently discovered and verified in the actual EIS runtime.

### EIS application — proposed integration contract

Keep the following roles separate:

- **Lean4:** normative admissibility and evidence-acceptance rules.
- **Python adapter:** typed request validation, authorized dispatch, job reconciliation, result capture, and provenance.
- **FlexAgent MCP:** documented knowledge retrieval unless the live tool inventory proves additional capabilities.
- **Simulation provider/API:** the actual job-submission and result service, identified and version-pinned.
- **EIS conductor/evidence ledger:** persistent state, budgets, retries, run IDs, and evidence classification.

The minimum EIS execution adapter contract should map to verified provider capabilities for:

1. submitting a supported simulation and receiving a durable provider job ID;
2. querying that same job's status, including queued/running/unknown/failure/completion states;
3. retrieving the result associated with that job ID.

These are **EIS adapter capability names**, not claims that FlexAgent MCP already exposes tools with those names. If the configured MCP exposes only documentation search and no separate supported execution endpoint is configured, report `BLOCKED`; do not manufacture a simulation result.

### First acceptance test

The first integration test should be a small, low-cost, real supported operation with an auditable trace:

- request ID and idempotency key;
- contract and candidate hashes;
- provider/tool name and pinned version;
- PDK identity and revision, where applicable;
- provider job ID;
- submission, status-reconciliation, and result-retrieval records;
- raw result/artifact hash and explicit evidence class;
- final machine-checkable acceptance or rejection with reasons.

Timeouts remain unknown/in-flight until reconciled against the same provider job ID. A timeout must not be interpreted as proof that no job exists or trigger a blind duplicate dispatch. Simulation evidence must never be promoted to physical-measurement evidence.

## 3. Combined EIS decision

Use the sequence:

`English intent → Lean4 contract → canonical typed plan → Python adapter → verified provider interface → evidence ledger → Lean4 acceptance`

FlexAgent can help interpret and construct photonics workflows, but it is not the source of truth for EIS authorization. The contract and evidence gate remain authoritative. Do not begin compiler design or claim a Photonic DeepSeek result as part of this integration reference.

## Evidence status

- **Source review:** the two upstream pages linked above.
- **Repository implementation:** this document only.
- **Lean 4.35 adoption:** not performed by this change.
- **FlexAgent live capability discovery:** not performed by this change.
- **Real simulation dispatch/result:** not performed by this change.
- **Physical measurement:** none claimed.
