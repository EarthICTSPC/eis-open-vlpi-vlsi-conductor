# Example: PTC electronic–photonic co-design

**Status:** explanatory walkthrough; not a working chip implementation or completed Lean4 proof.

This example defines the intended shape of a minimal reproducible demonstration: a workload contract, electronic interface, photonic reference model, conductor actions, and evidence record. It does not claim that all artifacts below have already been implemented.

## Scenario

A host sends a bounded input/configuration payload to a PTC control interface, requests one transformation, waits for completion, and checks the result against a reference model. The first prototype may use standard RISC-V plus MMIO; DMA or custom instructions are separate optimizations justified by profiling, not prerequisites.

## Intended artifacts

1. `contract.md` — inputs, outputs, units, legal operations, timing, error metric, and energy boundary.
2. `reference_model.py` — executable software reference for the explicitly chosen transformation.
3. `interface_trace.json` — a small legal transaction trace and one intentionally illegal trace.
4. `tests/` — checks for ordering, timeout/error handling, input/output conformance, and malformed traces.
5. `lean/` — Lean4 definitions and proofs for selected trace invariants and refinement obligations.
6. `evidence.json` — status, tool/version, input hashes, result, and links for each check.
7. `next_experiment.md` — the highest-value unresolved uncertainty and proposed next check.

Only files actually implemented and executed should be marked complete. Until then, these are planned artifacts, not claimed deliverables.

## Conductor walkthrough

```text
1. Read task + contract + DesignContext
2. Check required fields and PDK identity
3. Run cheap schema and reference-model tests
4. Run implemented Lean4 checks
5. Stop and report any contract or preflight failure
6. Request authorization before paid or externally consequential simulation
7. Run only the authorized tool action
8. Record raw outputs, versions, hashes, and evidence labels
9. Compare results with acceptance thresholds
10. Recommend the next discriminating experiment
```

The conductor coordinates tools; it does not make an invalid result valid, replace independent checks, or infer a physical pass from missing evidence.

## Example evidence record

```json
{
  "artifact_id": "EIS-PTC-IO-EXAMPLE-001",
  "status": "draft",
  "claim": "Host transactions conform to the proposed interface contract",
  "evidence_class": "NOT-RUN",
  "tool": null,
  "tool_version": null,
  "input_hashes": [],
  "result": null,
  "limitations": [
    "No hardware measurement is implied",
    "No PDK-bound physical implementation is included",
    "No end-to-end Lean4 proof is claimed"
  ]
}
```

## Success criteria for a future executable version

- A clean environment can run the reference tests using documented commands.
- An illegal trace is rejected for the intended reason.
- Lean4 builds and the listed theorems are discharged without placeholders for claimed properties.
- Every conductor action and result is traceable to a task, contract version, tool, and evidence record.
- The documentation distinguishes `FORMAL`, `SIMULATED`, `MEASURED`, `ASSUMED`, and `NOT-RUN`.

Until those checks are implemented and executed, this is an architecture walkthrough, not an executable demonstration.