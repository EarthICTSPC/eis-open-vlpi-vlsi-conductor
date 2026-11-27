# EIS-FAB-REQ-001 — Photonic Fabrication Platform Requirements

**Status:** Draft — authoritative EIS requirements baseline; open for technical review  
**Owner:** Earth ICT, SPC (EIS)  
**Repository:** `EarthICTSPC/eis-open-vlpi-vlsi-conductor`  
**Scope:** Foundry/process capabilities and the device, control, test, and evidence interfaces required to investigate and implement EIS Tian-style KKA / photonic-transformer computing.

> **Governing rule:** EIS defines the requirements. Tian, CORNERSTONE, SiEPIC, commercial foundries, and other community platforms are evidence sources and reference implementations against those requirements. None of them, by itself, defines the EIS specification.

This document is the requirements authority for EIS fabrication-platform evaluation. It is not a claim that any candidate foundry already satisfies the requirements, nor a process design kit (PDK), tape-out package, or fabrication release. Numerical limits remain explicitly open where they must be derived from the accepted KKA workload, optical error budget, system energy boundary, yield model, and cost per accepted useful transformation.

## 1. Purpose and research position

EIS is investigating whether a photonic modulator–interferometer cascade can implement the relevant KKA attention transformations through controlled optical interference, avoiding the conventional electronic SoftMax path used in standard attention. The objective is not to claim that interference itself is new, or that every attention architecture can eliminate SoftMax. Interference, MZIs, balanced detection, and optical matrix operations are established fields. The EIS research question is whether the **specific KKA mapping, physical cascade, encoding, normalization/selection behavior, calibration, and acceptance contract** can be reproduced and extended as a useful computing primitive.

The primary technical reference is:

- Tian et al., “Photonic Transformer Chip: Interference Is All You Need,” *PhotoniX* 6, 45 (2025), DOI: [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).

The first engineering objective is a faithful, source-led 10×1 computational baseline and a separately identified SOI device reference. Scaling targets may follow only when the 10×1 computation, device transfer functions, and system-level energy accounting are independently accepted.

EIS welcomes critical review and collaboration. A gap in a reference PDK is not a criticism of its designers; it is a useful, specific question for the community: can the missing interface, model, device, test structure, or evidence be contributed?

## 2. Requirement tiers and interpretation

Every requirement has three tiers:

- **Minimum viable (M):** enough capability to build and evaluate a bounded, reproducible KKA demonstrator.
- **Target (T):** the preferred capability for a credible multi-cell engineering platform and a scalable development path.
- **Stretch (S):** a capability that materially improves density, energy, calibration, manufacturing, or system integration.

The tiers describe EIS requirements, not claims about existing PDK capabilities. A tier may be marked **TBD** where a numerical value must be derived or agreed. TBD is deliberate: EIS will not invent process limits and then mistake them for measured or foundry-supported facts.

Requirement states used in evidence records:

- `REQUIRED`: EIS requirement.
- `SOURCE-REPORTED`: stated by a paper, PDK, or vendor.
- `MODELLED`: produced by a documented analytical or compact model.
- `SIMULATED`: produced by a specified numerical simulation.
- `MEASURED`: measured on an identified physical artifact.
- `FOUNDRY-CONFIRMED`: confirmed in writing by the relevant foundry.
- `OPEN`: not yet established.

A requirement is not satisfied merely because a PDK contains a cell with a similar name.

## 3. Authoritative requirements matrix

| ID / domain | Requirement | Minimum viable | Target | Stretch | Acceptance evidence / open questions |
|---|---|---|---|---|---|
| FAB-001 Process definition | Complete, versioned SOI process stack and design rules | Documented silicon thickness, BOX, top cladding, substrate, etch depths, sidewall assumptions, materials, and layer map for one process | Foundry-confirmed stack, process corners, layer-purpose map, DRC and optical design rules | Statistical process distributions and calibrated corner models | Foundry process document; stack file; layer map; DRC deck/version; explicit provenance for every parameter |
| FAB-002 Waveguide platform | Single-mode optical routing suitable for the chosen KKA wavelength and polarization | At least one characterized strip-waveguide cross-section | Strip and rib options with characterized TE operation and documented transition rules | Multiple bands/polarizations and optimized low-loss routing | Mode/effective-index data, group index, propagation loss, bend loss, polarization behavior, dimensional tolerances |
| FAB-003 Waveguide loss | Quantified propagation and bend loss | Source-reported or simulated model with clear evidence label; physical test structures planned | Foundry- or wafer-measured loss distributions across relevant lengths and bends | Low-loss process options and wafer-level statistical maps | Cut-back or equivalent measurement; wavelength, polarization, length, wafer/die, uncertainty |
| FAB-004 Directional couplers | Controlled complex through/cross transfer | Reproducible coupler geometry and a documented complex S-parameter or field model | Characterized coupling ratio, phase, excess loss, bandwidth, and process sensitivity | Tunable or multi-geometry coupler library with calibrated compact models | Complex S data, port convention, reference planes, reciprocity/passivity checks, measured-vs-model residuals |
| FAB-005 MZI primitive | Composable two-arm interferometer with explicit phase and amplitude behavior | One MZI with documented splitter/combiner, arm, port, and phase conventions | Characterized MZI family with tunable splitting and calibrated phase response | Dense, low-crosstalk MZI arrays and wafer-level calibration | Full complex transfer matrix, port mapping, insertion loss, extinction, phase range, repeatability |
| FAB-006 KKA cascade | Physical modulator–interferometer cascade that implements the specified KKA operation | One source-led KKA cell with explicit data encoding, reference plane, field convention, and detector output | Cascadable KKA tile with independently testable cell-to-cell interfaces | Larger tiled arrays with partitioned calibration and fault isolation | Tian 10×1 baseline; EIS contract; complex-field model; measured cell/tile transfer; accepted-workload error |
| FAB-007 Amplitude–phase control | Controlled mapping from electrical control to optical field amplitude and phase | Characterize the available modulator/phase-shifter response; do not assume independent control | Calibrated (E(V)) and θ(V) or multi-control response, including coupling and hysteresis where present | Closed-loop amplitude/phase control with per-device calibration | Measured complex field versus control; operating range; linearity; bandwidth; drift; uncertainty |
| FAB-008 Phase shifters | Repeatable phase control for all required KKA phase degrees of freedom | Demonstrate required phase range for a single MZI/cell | Calibrated phase range, resolution, power, settling, and repeatability for a tile | Low-power, fast, dense control with reduced thermal interaction | Δφ versus electrical input; power; settling; drift; control noise; lifetime |
| FAB-009 Thermal interaction | Quantify thermal cross-coupling among neighboring actuators | Measure a small actuator interaction matrix | Characterized thermal influence matrix for representative tile density and operating states | Low-crosstalk layout/process plus model-based compensation and closed-loop control | Measure Δφ = HΔP (or validated nonlinear extension); spatial/temporal response; uncertainty |
| FAB-010 Detector interface | Detection compatible with the KKA output observable | Defined detector interface and an externally measurable output for the demonstrator | Integrated balanced photodetection or foundry-supported detector integration with calibrated responsivity and bandwidth | Low-noise, high-bandwidth, low-energy detector/readout co-design | Responsivity, bandwidth, common-mode rejection, noise, saturation, offset, gain, calibration, reference plane |
| FAB-011 Optical interfaces | Defined coupling and test access | Edge/grating or equivalent optical I/O for a single-device test | Repeatable wafer-level optical access and reference structures | High-density fiber/package interface and automated optical test | Port definitions, insertion loss, alignment tolerance, polarization, test plan |
| FAB-012 Electrical/RF interfaces | Electrical access to actuators and detectors | Pads and routing for the minimum demonstrator | Characterized electrical parasitics and control/readout interfaces for a tile | Co-designed driver/readout integration and dense interconnect | Pad map, resistance/capacitance, RF response, crosstalk, voltage/current limits |
| FAB-013 Packaging | Stable optical, electrical, and thermal operating environment | Package or probe configuration sufficient for repeatable characterization | Repeatable package with thermal management and optical/electrical access | Scalable multi-die, fiber-array, or heterogeneous package | Package loss, thermal resistance, stability, alignment, reliability, serviceability |
| FAB-014 Calibration | Recover a valid KKA operating point after fabrication | Manual calibration procedure for one cell | Automated calibration for a tile with stored coefficients and uncertainty | In-field recalibration, drift tracking, fault detection, and recovery | Calibration time, convergence, residual error, repeatability, recalibration interval |
| FAB-015 Process variation | Tolerance of fabrication variation | Identify critical dimensions and perform sensitivity analysis | Foundry process corners and measured distributions propagated through KKA acceptance | Yield-aware robust optimization and per-die adaptation | Width/gap/etch/sidewall/thickness distributions; Monte Carlo or measured wafer maps; accepted yield |
| FAB-016 Design-for-test | Structures that isolate process and device errors | Dedicated waveguide, bend, coupler, MZI, phase-shifter, and detector test structures | Wafer-level test plan and device-to-model traceability | Automated statistical characterization across wafer and lots | Test-structure GDS/OASIS, measurement procedures, calibration artifacts, raw data and metadata |
| FAB-017 PDK model quality | Models support complex-field composition, not only layout generation | Documented compact models with port order, phase convention, wavelength domain, and provenance | Validated complex S-parameter models with uncertainty and process corners | Hierarchical compact models correlated to measured devices and arrays | Model source, version, domain, interpolation behavior, passivity/reciprocity, residuals, license |
| FAB-018 Simulation readiness | Simulation inputs are bounded before expensive EM/FDTD runs | Geometry, stack, materials, source, boundaries, monitors, and mesh policy explicit | Mesh convergence and resource estimate before solver execution | Automated contract-driven resource gating and adaptive model fidelity | Preflight manifest; grid points/complexity; estimated memory/runtime/cost; convergence report |
| FAB-019 Multi-backend lowering | One backend-neutral device/contract description can be lowered to multiple tools | One reference lowerer and one independent comparison path | Shared IR and acceptance tests across PhotonForge, GDSFactory/SAX, Tidy3D, and other suitable backends | Portable lowering across foundry PDKs and simulation engines | Pinned schemas/tool versions; deterministic lowering; cross-backend comparison; no PDK-specific assumptions in the canonical contract |
| FAB-020 Metrology and evidence | Every result is traceable to its physical or computational source | Machine-readable evidence manifest for each test | End-to-end traceability from requirement to layout, simulation, wafer/die, measurement, and acceptance | Foundry/partner data exchange with controlled access and reproducible audit trail | Provenance tags, hashes, instrument calibration, raw data, uncertainty, reviewer, date |
| FAB-021 Reliability | Devices remain within contract over intended operating conditions | Basic repeatability and short-duration stability characterization | Thermal cycling, operating-life, and environmental characterization appropriate to the use case | Reliability models and accelerated qualification for production deployment | Defined conditions, sample size, drift/failure statistics, failure analysis |
| FAB-022 Yield and economics | Optimize cost per accepted useful KKA transformation, not wafer price alone | Identify cost drivers and collect demonstrator cost data | Estimate cost per accepted cell/tile and per accepted workload block using yield and calibration | Production economics including wafer utilization, test, packaging, power, and lifecycle | Transparent cost model, yield assumptions, test/calibration time, scrap/rework, system energy boundary |
| FAB-023 Scale and tiling | Cell composition scales without hidden calibration or routing collapse | Demonstrate a small multi-cell composition | Defined tile architecture and measured interconnect/calibration overhead | 64×64-class tile path with partitioned calibration and fault containment | Scaling model tied to measured cell data; crosstalk, loss, routing, yield, and accepted workload |
| FAB-024 Open collaboration | Publish reusable, non-confidential interfaces and gap reports | Public contracts, test vectors, and non-proprietary findings | Community-reviewed reference adapters and reproducible examples | Shared multi-foundry benchmark suite and contributed implementations | License review; public provenance; contributor attribution; no NDA or restricted data leakage |

## 4. KKA-specific acceptance boundary

The fabrication platform is being evaluated to implement a computational contract, not merely to produce optical interference.

For each KKA primitive, the contract must identify at least:

1. **Input state and encoding:** what information is encoded in field amplitude, phase, wavelength, time, or another physical degree of freedom.
2. **Reference plane:** where the input field is defined and where the output is accepted.
3. **Complex-field convention:** phasor sign convention, port ordering, polarization, normalization, and reference phase.
4. **Interference observable:** whether the required output is a real or quadrature cross-term, and how the physical circuit/detector produces it.
5. **Amplitude–phase transfer:** the measured or modeled mapping from controls to complex optical field.
6. **Calibration:** how process variation, thermal coupling, drift, and detector offsets are corrected.
7. **Acceptance metric:** error and energy per accepted useful transformation or workload block, including system boundaries.

The general interference identity is not by itself the KKA implementation. The physical cascade, encoding, normalization, and detector/readout behavior must jointly satisfy the KKA contract. The Tian SI-1 quadrature expression and the main paper's general real cross-term must not be silently treated as the same detector convention; the algebraic relationship and physical phase/reference mapping must be explicit.

**SoftMax claim discipline:** EIS will test whether the Tian KKA formulation and its physical realization remove the conventional SoftMax operation from the specified attention path while preserving the required task-level behavior. This is a workload- and formulation-specific claim. It must be demonstrated against a matched electronic baseline and a clearly specified KKA reference. Do not claim universal elimination of SoftMax from all attention systems.

## 5. Reference evidence tracks

The following platforms are comparison evidence, not normative specifications.

| Reference track | What it can teach EIS | What it does not establish | Planned use |
|---|---|---|---|
| **Tian KKA / SOI reference** | Source architecture, KKA computation, reported SOI waveguide dimension (450 nm × 220 nm), MZI/interference formulation, reported numerical and experimental results | Complete transferable foundry process stack, EIS target process, all device transfer functions, or EIS-scale yield | Primary computational and architecture reference; reproduce 10×1 before extrapolation |
| **CORNERSTONE Si220** | Open SOI PDK, strip/rib cells, layer stack and design rules, compact circuit models, directional-coupler and MZI examples | Foundry validation of every compact model; equivalence to Tian's process or KKA topology | Independent open-PDK reference; audit models, geometry, stack, S-parameters, and gaps |
| **SiEPIC EBeam / SiEPIC ecosystem** | Open PDK workflow, layout/verification conventions, device library, optical port conventions, simulation and measurement examples | SOI process equivalence to Tian or CORNERSTONE; direct KKA implementation; complete dense thermal-control solution | Workflow and tooling reference; compare device models and identify missing KKA-specific interfaces |
| **Commercial foundry platforms (including GF and other eligible partners)** | Actual process capability, manufacturing controls, process corners, foundry models, wafer data, and commercial path | Permission to disclose or upload confidential data beyond written authorization | Evaluate against EIS requirements under the applicable NDA, license, export, and data-handling rules |

### Evidence handling rules

- Keep Tian-reported parameters separate from EIS assumptions.
- Keep CORNERSTONE process defaults separate from Tian's reported geometry.
- Keep SiEPIC process defaults separate from both.
- A compact model derived from coupled-mode or supermode calculations is a model, not a measurement.
- A component label such as “50:50” is not a measured 50:50 result.
- A successful layout or local geometry extrusion is not an FDTD result.
- A successful FDTD run is not foundry qualification or physical measurement.
- A foundry statement must be recorded with source, date, scope, and any confidentiality restrictions.

## 6. How EIS will evaluate each reference

Each reference adapter or evidence package should map to the requirement IDs above and report one of:

- `SUPPORTED` — evidence satisfies the requirement at the stated tier and scope.
- `PARTIAL` — some elements are supported; list what is missing.
- `NOT_SUPPORTED` — the reference does not provide the capability.
- `NOT_ASSESSED` — not yet inspected or insufficient evidence.
- `NOT_APPLICABLE` — explain why.

Every assessment must include:

- source URL or controlled source identifier;
- exact package, PDK, process, model, and tool version;
- source revision or commit where available;
- parameter values and units;
- evidence state (`SOURCE-REPORTED`, `MODELLED`, `SIMULATED`, `MEASURED`, or `FOUNDRY-CONFIRMED`);
- known assumptions and exclusions;
- reproducible test or inspection procedure;
- unresolved questions for the community or foundry.

The initial comparison should not rank PDKs by the number of cells. It should evaluate whether each platform can provide the complex-field behavior, calibration, metrology, and cost evidence required by the KKA contract.

## 7. Engineering gates

1. **G0 — Requirements review:** agree on requirement wording, tiers, and the evidence needed to close each item.
2. **G1 — Reference inventory:** complete read-only audits of CORNERSTONE, SiEPIC, and Tian source evidence. No process values are silently substituted across tracks.
3. **G2 — Contract and workload freeze:** freeze the 10×1 computational baseline, complex-field conventions, reference planes, and matched electronic comparator.
4. **G3 — Device-model verification:** verify coupler/MZI/modulator/detector models and their composition; identify which values are assumed, modeled, simulated, or measured.
5. **G4 — Simulation preflight:** apply geometry, material, mesh, convergence, memory, runtime, and cost gates before uploading or executing expensive simulations.
6. **G5 — Test-coupon definition:** define the minimum structures needed to measure the missing transfer functions and thermal interaction.
7. **G6 — Foundry feasibility review:** ask candidate foundries to respond against the same requirements matrix, including customization, engineering NRE, wafer cost, test, yield, and IP/data boundaries.
8. **G7 — Physical acceptance:** compare measured devices and assembled tiles against the frozen KKA contract and accepted workload.

Passing one gate does not imply passing a later gate.

## 8. Foundry engagement questions

EIS should ask each candidate foundry or fabrication partner to respond requirement-by-requirement, including:

1. Which requirements are supported by the standard process today?
2. Which require a custom module, mask layer, process option, or design-rule exception?
3. Which compact models are measured, calibrated, simulated, or purely analytical?
4. Can the foundry provide complex S-parameters or field data with reference planes and uncertainty?
5. What are the process distributions for critical waveguide, gap, etch, sidewall, and film parameters?
6. What phase-shifter and modulator options are available, and what measured amplitude–phase transfer data can be supplied?
7. What thermal-crosstalk and calibration structures can be included in a test vehicle?
8. What detector, electrical/RF, packaging, and wafer-level optical-test options exist?
9. What is the least-cost engineering path to a characterized KKA test coupon and then a multi-cell tile?
10. What data may be used in external simulators, cloud services, or AI/LLM-assisted workflows, and what requires written authorization?
11. What are the NRE, wafer, test, packaging, yield, and schedule assumptions?
12. What can be openly published or contributed back to the photonics community?

The economic comparison is **cost per accepted useful KKA transformation/workload block**, with a declared system boundary—not wafer price or TOPS/W in isolation.

## 9. Community collaboration invitation

EIS intends to share the Tian KKA research direction with the wider photonic community and invite technically specific contributions. We welcome:

- independent review of the KKA mathematical and physical interpretation;
- source-faithful reproduction of the Tian 10×1 computational baseline;
- complex-field models for couplers, MZIs, modulators, and detector interfaces;
- measured amplitude–phase and thermal-interaction data;
- open test structures and calibration methods;
- multi-backend PDK adapters and cross-tool verification;
- critique of the SoftMax-elimination claim and matched workload methodology;
- suggestions for process options, test vehicles, and fabrication partners.

A useful contribution can be a negative result, a missing model, an incompatible port convention, an unmodeled thermal interaction, or a demonstrated limitation. These are valuable because they make the engineering problem more precise.

**We are not asking the community to endorse an EIS conclusion. We are inviting the community to help test, reproduce, challenge, and improve the requirements and the evidence.**

## 10. Initial open issues

The following are intentionally unresolved and should be converted into measurable sub-requirements only after the relevant workload and evidence are available:

- numerical optical error budget per KKA cell, tile, and accepted workload;
- allowable insertion loss and phase error by stage and cascade depth;
- required amplitude and phase ranges, resolution, and control bandwidth;
- detector noise, bandwidth, and dynamic range;
- thermal interaction limits and recalibration interval;
- minimum demonstrator size and scaling sequence beyond the Tian 10×1 baseline;
- process-corner and yield targets;
- numerical grid, memory, runtime, and simulation-credit budgets;
- packaging and system-level energy boundary;
- target cost per accepted transformation and workload block.

No numerical requirement should be frozen without a traceable derivation, source, measurement, or explicit EIS decision.

## 11. Change control

This document is the authoritative EIS fabrication-platform requirements baseline once reviewed and adopted. Reference audits, PDK adapters, simulation notebooks, and foundry responses must map back to its requirement IDs; they must not silently redefine them.

Changes should record:

- requirement ID and revision;
- reason for change;
- evidence or engineering decision motivating it;
- impact on existing reference assessments and acceptance tests;
- approver and date.

The document may evolve as evidence improves. A reference PDK finding does not automatically change an EIS requirement; it may instead expose a gap, motivate a design alternative, or generate a community contribution request.

## 12. Initial source register

1. Tian et al., *PhotoniX* 6, 45 (2025), [DOI 10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7). Primary KKA research reference.
2. CORNERSTONE Si220 open PDK, [gdsfactory/cspdk](https://github.com/gdsfactory/cspdk) and [CORNERSTONE Photonics](https://www.cornerstonephotonics.com/). Reference process and compact-model evidence; each model's validation status must be checked individually.
3. SiEPIC-Tools and EBeam ecosystem, [SiEPIC](https://github.com/SiEPIC). Reference workflow, PDK, and device evidence; process equivalence must not be assumed.
4. EIS Conductor repository evidence packages under `docs/work-packages/`, `experiments/`, and `evidence/`. These are implementation and audit records subordinate to this requirements baseline.

---

**Earth ICT, SPC (EIS)**  
*Open physical-computing infrastructure for an Earth-first ICT future.*
