# eis-open-vlpi-vlsi-conductor

**Earth ICT, SPC — Open enabling technical disclosure for Very Large Photonic Infrastructure (VLPI)**

> **Here is the architecture. Here are the contracts. Here are the interfaces. Here are the implementation rules. Here is the verification path. Here is the physical artifact. Make your own.**

This repository is the open technical-disclosure layer of the Earth ICT, SPC (EIS) VLPI project.

It is deliberately organized differently from a research article. The **Research Article** records scientific questions, evidence, results, interpretation, and limits. This repository is intended to provide an **enabling technical disclosure** from which a technically skilled person can understand, reproduce, adapt, and independently implement compatible physical-computation systems.

It is not itself a patent and does not provide legal advice.

## What is being disclosed?

EIS is developing an open framework for physical computation in which the primary object is a **Replicable Unit (RU)**: a bounded, composable physical transformation with an explicit state model, contract, physical realization, verification path, and replication evidence.

The central working abstraction is:

[
S_{RU}=(H,T,R,B,G,C)
]

where:

- **H** — physical field/state space
- **T** — physical transformation mapping
- **R** — constraint-reduction operator
- **B** — state-boundary acceptance
- **G** — state-to-field regeneration
- **C** — machine-checkable contract

The abstraction does not assume that photonic computation is inherently a Boolean gate, electronic MAC, or conventional matrix-vector operation.

## The "make your own" principle

The repository is intended to support independent implementation.

An implementation may use a different foundry, material stack, simulator, packaging technology, or toolchain, provided that it satisfies the published contracts and interfaces.

The open repository therefore separates:

- **architecture and contracts** — openly disclosed;
- **technology interfaces** — openly specified;
- **reference implementations** — openly reproducible where possible;
- **controlled technology** — proprietary PDKs, process rules, models, credentials, and other material that EIS is not authorized to publish.

The objective is not to create a black-box EIS chip.

The objective is to create an **open physical-computation architecture that others can implement**.

## GitHub versus the Research Article

### Research Article

The Research Article asks:

> **What do we know, what did we demonstrate, and what remains a hypothesis?**

It is evidence-led scientific communication.

### This repository

This repository asks:

> **What would someone skilled in the art and science need in order to make an independent implementation?**

It therefore emphasizes:

- definitions;
- contracts;
- interfaces;
- schemas;
- implementation rules;
- verification;
- physical-design artifacts;
- test vectors;
- evidence manifests;
- reproducibility.

A repository artifact does not become experimentally demonstrated merely because it is published.

## From physical principle to infrastructure

The intended disclosure chain is:

```text
Physical principle
      ↓
Physical state
      ↓
Transformation
      ↓
RU contract
      ↓
Physical primitives
      ↓
Composition
      ↓
Technology mapping
      ↓
CRC
      ↓
Physics simulation
      ↓
PVR
 ├── PDR
 ├── PCT
 └── PTV
      ↓
OASIS
      ↓
Foundry review
      ↓
Fabrication
      ↓
BIST / State Boundary measurement
      ↓
Replication
      ↓
Useful computational service
      ↓
VLPI
```

The physical artifact is therefore part of the evidence chain, not merely a downstream drawing.

## Why VLPI?

EIS asks a system-level question:

> **Can physical computation and physical information movement be co-designed as one scalable, verifiable photonic infrastructure?**

The project is not simply about putting an optical bus around an otherwise electronic accelerator.

EIS is investigating whether some computational state can remain within a photonic physical substrate while it is transformed, selected, routed, and communicated, thereby reducing unnecessary electronic state-boundary crossings.

At larger scale, this makes the following first-class engineering concerns:

- physical transformation;
- optical information movement;
- state preservation;
- state boundaries;
- replication;
- thermal behavior;
- electrical interfaces;
- packaging;
- fabrication;
- verification;
- measurement;
- yield;
- wafer-scale composition;
- stacked-wafer composition.

## Replicable Units

An RU is **not merely a photonic standard cell**.

An RU is defined by the physical transformation it performs, the state on which it operates, the contract that accepts that transformation, its realization, and the evidence supporting it.

Conceptually:

```text
                 RU Definition
       transformation + state + contract
                       │
                       ▼
                  RU Instance
            specific realization
                       │
                       ▼
                 RU Composition
                       │
                       ▼
                Wafer / Stack / VLPI
```

Geometry is an implementation property.

The contract is the invariant.

## Constraint Reduction Calculus

**Constraint Reduction Calculus (CRC)** is used to reduce the physical search space before expensive physics simulation.

The objective is not to replace physics simulation.

It is to test whether unsuitable candidates can be rejected earlier:

```text
Design space
     ↓
CRC constraints
     ├── reject impossible candidates
     ├── reject contract-incompatible candidates
     └── retain plausible candidates
                  ↓
               EM/FDTD
                  ↓
           physical evidence
```

A central metric is:

[
eta_{CRC}=1-rac{N_{FDTD,CRC}}{N_{FDTD,baseline}}
]

Solution-quality preservation is evaluated separately.

## Evidence discipline

EIS distinguishes evidence states rather than treating all repository artifacts as equivalent.

| State | Meaning |
|---|---|
| `draft` | Incomplete or exploratory material |
| `specified` | Behavior and acceptance conditions explicitly defined |
| `formally-verified` | Logical property machine-checked under stated assumptions |
| `computationally-demonstrated` | Supported by a documented computational experiment |
| `experimentally-demonstrated` | Supported by physical experimental demonstration |
| `measured` | Measurement record exists for the identified artifact and condition |
| `proposed-hypothesis` | Research hypothesis or design target not yet demonstrated |
| `derived-metric` | Metric/framework derived from defined inputs |

**Formal verification is not fabrication. Simulation is not measurement. A design target is not a result.**

Failure is also useful disclosure when the input, assumptions, toolchain, result, and failure mode are recorded.

## Open / Controlled / Verified

### Open

Examples:

- schemas;
- contracts;
- architecture;
- reference algorithms;
- non-proprietary primitives;
- verification methodology;
- evidence schemas;
- reproducibility tooling;
- public physical artifacts.

### Controlled

Examples:

- NDA foundry PDK contents;
- proprietary process rules;
- proprietary compact models;
- credentials;
- private simulation environments;
- pre-release fabrication artifacts;
- confidential packaging information.

The open repository describes the interface to controlled technology without reproducing controlled contents.

### Verified

Evidence produced by an identified verification or measurement process.

A file existing in GitHub is not, by itself, physical verification.

## Schema foundation

The repository is schema-first.

```text
schema/
├── ru/
│   └── ru.schema.yaml
├── contract/
│   └── contract.schema.yaml
├── evidence/
│   └── evidence.schema.yaml
└── design-context/
    └── design-context.schema.yaml
```

**DesignContext** is the integration boundary for heterogeneous physical systems, including:

- photonic PDK identity;
- electronic PDK identity;
- electro-photonic interface;
- package/carrier context;
- optical interfaces;
- RF/electrical constraints;
- thermal constraints;
- verification context.

## RU-001 and RU-002

### RU-001

RU-001 is the first reference physical transformation unit used to establish the EIS RU/contract/PVR/evidence architecture.

Its implementation status must be read from its machine-readable contract and evidence artifacts rather than inferred from diagrams or prose.

### RU-002

RU-002 is the candidate heterogeneous optical-computation unit for the current EIS LLM architecture.

The working transformation composition is:

[
T_{RU-002}
=
T_{attention}
circ
T_{select}
circ
T_{KKA-cache}
]

with a state progression conceptually represented as:

[
H_{QKV}
ightarrow H_{similarity}
ightarrow H_{selected}
ightarrow H_{attention}.
]

A central research question is:

> **Can optical similarity states be ranked, selected, and routed without first becoming electronic data?**

This is a research hypothesis, not a claim that photonic top-k or fully optical attention has already been experimentally demonstrated by EIS.

## Physical design and OASIS

The intended realization path is:

```text
RU contract
   ↓
technology mapping
   ↓
physical layout
   ↓
PVR
   ↓
OASIS
   ↓
foundry review
   ↓
fabrication
   ↓
BIST
```

An image of a layout is explanatory.

Where publication is permitted, the machine-readable OASIS artifact is the physical-design disclosure.

## Independent implementation

An independent implementation should be able to follow:

```text
1. Select an appropriate technology
2. Instantiate an RU contract
3. Select physical primitives
4. Map primitives to the technology
5. Apply CRC
6. Run physics simulation
7. Run PVR
8. Generate a physical artifact
9. Generate an evidence manifest
10. Fabricate through the appropriate controlled process
11. Measure / run BIST
12. Compare evidence with the contract
```

Where proprietary tools or PDKs are required, the repository should identify the controlled boundary rather than pretending that proprietary material is open.

## Repository structure

The repository will grow toward:

```text
eis-open-vlpi-pdk/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
│   ├── 00-overview/
│   ├── 01-architecture/
│   ├── 02-physical-transformations/
│   ├── 03-replicable-units/
│   ├── 04-crc/
│   ├── 05-pvr/
│   ├── 06-bist/
│   ├── 07-packaging/
│   ├── 08-vlpi/
│   └── 09-reproduction/
├── schema/
│   ├── ru/
│   ├── contract/
│   ├── evidence/
│   └── design-context/
├── technology/
│   ├── reference/
│   └── adapters/
├── primitives/
├── ru/
│   ├── RU-001/
│   └── RU-002/
├── verification/
│   ├── PDR/
│   ├── PCT/
│   └── PTV/
├── agents/
├── examples/
└── tests/
```

## Contribution standard

A contribution is complete when another technically skilled person can understand:

1. what was done;
2. why it was done;
3. what assumptions were made;
4. what technology was used;
5. what evidence exists;
6. what remains unverified;
7. how to reproduce or independently implement it.

EIS does not seek a single universal verification tool.

It seeks a formally explicit evidence chain in which domain-specific tools produce domain-specific evidence and higher-level contracts establish the logical relationship among those evidence records.

## Independent LLM review

The repository is intended to be independently reviewable by external LLMs and technical collaborators.

For a review that starts from the current frozen GitHub2VLPI-002 evidence and EIS-SWARM-001-A disagreement analysis, use:

[`docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md`](docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md)

That guide provides the canonical review order, evidence boundary, questions, and non-claims. It deliberately does **not** provide an expected ontology or agent population.

## Disclosure doctrine

The repository's governing document is:

[`docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md`](docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md)

Read that document before treating repository contents as a complete implementation specification.

## Lean 4 formalization

The machine-checkable formal model is maintained as a dedicated Lean 4 / Lake project at [`formal/lean4/`](formal/lean4/). This keeps formal definitions and proofs separate from the Python execution harness while enabling independent CI checks. The initial project proves a synthetic 228 ps serial-latency example exceeds a 200 ps budget; it is a formal arithmetic baseline, not measured physical performance or yet a cross-language orchestrator regression.

See [`formal/lean4/README.md`](formal/lean4/README.md) for setup and scope. GitHub Actions builds the project when its files change.

## Status

This is an evolving open technical disclosure.

It should be read together with the evidence state attached to each artifact.

**Do not infer fabrication, foundry acceptance, measured performance, or infrastructure-scale validation from an architecture diagram, schema, simulation, or design target.**

---

**Earth ICT, SPC (EIS)**  
*Open physical-computing infrastructure for an Earth-first ICT future.*
