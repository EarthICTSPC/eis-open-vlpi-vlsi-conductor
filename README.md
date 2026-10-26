# eis-open-vlpi-vlsi-conductor

**Earth ICT, SPC (EIS) — Open technical disclosure for Very Large Photonic Infrastructure (VLPI)**

> **EIS is pursuing photonic computation as a potential replacement for energy-intensive electronic accelerator workloads. The path is joint electronic–photonic co-design, formal contracts, physical validation, and system-level evidence.**

Here is the architecture. Here are the contracts and interfaces. Here is the verification path. Here is the evidence needed to judge whether a physical implementation meets its claims.

## Start here

- [PTC and the GPU-replacement hypothesis](docs/01-architecture/PTC_AND_GPU_REPLACEMENT_HYPOTHESIS.md) — what Photonic Transformer Chips are, what published research supports, and what remains a hypothesis.
- [Electronic–photonic interface contract](docs/01-architecture/ELECTRONIC_PHOTONIC_INTERFACE_CONTRACT.md) — a draft boundary for host control, input encoding, optical computation, readout, state, timing, and energy accounting.
- [PTC co-design walkthrough](examples/ptc-electronic-photonic-codesign/README.md) — a deliberately small example plan showing how a contract, tests, Lean4 obligations, conductor actions, and evidence fit together.
- [Independent LLM review guide](docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md) — canonical review order and evidence boundaries.
- [Open VLPI disclosure doctrine](docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md) — how to interpret the repository and its claims.

**Status note:** the new PTC and electronic–photonic pages are design documentation. The walkthrough is explicitly not yet a reproducible executable demonstration. Do not infer a completed Lean4 proof, a fabricated 512 × 512 PTC, or measured GPU-replacement performance from these documents.

## What is a PTC?

A Photonic Transformer Chip (PTC) explores using optical interference in a photonic circuit to perform parts of transformer-related computation. Rather than treating optics only as a communication bus around an electronic accelerator, EIS investigates whether the computational transformation and information movement can be co-designed within a photonic substrate.

The research of Tian et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025), DOI [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7), is an important reference. It should not be read as evidence that a 512 × 512 or 4K × 4K PTC, complete production LLM, or general-purpose GPU replacement has already been demonstrated. Separate measured results from ideal-model results, projections, and future work.

## Why electronic–photonic co-design?

A useful PTC is more than an optical core. The system boundary includes electronic input preparation, electrical-to-optical conversion, photonic transformation, optical detection, readout, configuration, calibration, synchronization, state boundaries, packaging, and thermal overheads.

The interface must define representations, units, port ordering, field normalization, timing, legal transactions, errors, numerical tolerance, and energy-accounting boundaries. The optical model and electronic interface should evolve together as PDK and physical constraints become clearer.

## Why Lean4?

Lean4 can make mathematical definitions, legal interface traces, state transitions, invariants, and refinement obligations precise—and machine-check properties that follow from those definitions and assumptions. It cannot by itself prove that an analog driver, detector, PDK model, or fabricated device behaves as specified. Such links need appropriate tests, validated models, simulation, measurement, or other explicit evidence.

## What is the agentic conductor?

The conductor coordinates a contract-governed engineering loop. It reads requirements and design context, checks completeness, runs inexpensive schema and reference-model tests, invokes implemented Lean4 checks, stops on failed gates, requests authorization before paid or consequential simulation, records tool versions and results, classifies evidence, and recommends the next experiment.

MCP is a tool-integration mechanism, not a guarantee of correctness or authorization. The conductor must not turn missing evidence into a pass or present an unexecuted action as complete.

## Evidence discipline

| Label | Meaning |
|---|---|
| `FORMAL` | A completed machine-checked proof under stated assumptions |
| `SIMULATED` | A result from a named computational or physical model |
| `MEASURED` | A result from an identified physical artifact and measurement process |
| `ASSUMED` | A provisional assumption not independently established |
| `NOT-RUN` | The required check has not been executed |

**Formal verification is not fabrication. Simulation is not measurement. A design target is not a result.** Claims should link to their contracts, assumptions, tool versions, inputs, results, and limitations.

## The first 512 × 512 milestone

The initial target is a jointly defined, Lean4-formalized, PDK-bound, testable **design proposition** for a 512 × 512 PTC/VLPI system and its electronic I/O—not a claim that such a physical chip already exists. The team must first specify what “512 × 512” counts, define the reference transformation and error metric, agree interface and system-level acceptance criteria, and identify the PDK and parameter provenance.

## Repository principles

- **Open:** contracts, schemas, reference algorithms, non-proprietary primitives, verification methods, reproducibility tooling, and publishable physical artifacts.
- **Controlled:** NDA PDK contents, proprietary process rules and models, credentials, confidential packaging information, and other material EIS is not authorized to publish.
- **Evidence-led:** a repository artifact does not become experimentally demonstrated merely because it is published.
- **Implementation-neutral:** alternative technologies may be used if they satisfy the published contracts and interfaces.

## Existing architecture

The repository's broader framework defines a Replicable Unit (RU) as a bounded physical transformation with an explicit state model, contract, physical realization, verification path, and replication evidence. Constraint Reduction Calculus (CRC) is intended to screen unsuitable candidates before expensive physics simulation; it does not replace physics simulation.

See the existing [disclosure doctrine](docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md) and [independent review guide](docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md) for the repository's governing interpretation and review workflow.

## Contributing

A useful contribution explains what was done, why, assumptions, technology, evidence, unresolved questions, and how to reproduce the result. Keep planned artifacts distinct from implemented artifacts and mark every check with its actual status.

**Earth ICT, SPC (EIS)**  
*Open physical-computing infrastructure for an Earth-first ICT future.*