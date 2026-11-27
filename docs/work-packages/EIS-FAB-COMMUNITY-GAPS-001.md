# EIS-FAB-COMMUNITY-GAPS-001 — Photonic Community Gap and Contribution Register

**Parent specification:** [EIS-FAB-REQ-001](EIS-FAB-REQ-001.md)  
**Related assessments:**
- [EIS-FAB-REF-TIAN-001](EIS-FAB-REF-TIAN-001.md)
- [EIS-FAB-REF-CORNERSTONE-001](EIS-FAB-REF-CORNERSTONE-001.md)
- [EIS-FAB-REF-SIEPIC-001](EIS-FAB-REF-SIEPIC-001.md)

**Status:** Initial public collaboration register; open for correction and contributions  
**Owner:** Earth ICT, SPC (EIS)

## 1. Purpose

This register converts the gaps identified by EIS-FAB-REQ-001 and the three reference assessments into specific questions and contribution opportunities for the photonics community.

It is not a ranking of PDKs or a criticism of existing projects. Each reference platform has different goals, process assumptions, licenses, and validation boundaries. The purpose is to make the next research and engineering questions concrete enough that maintainers, researchers, foundries, and device engineers can answer them or contribute evidence.

## 2. Research framing

EIS is investigating the Tian KKA approach: use runtime-programmable optical interference and amplitude–phase coupling as the computational primitive for the specified attention path, with the objective of avoiding the conventional SoftMax operation in that KKA formulation.

Interference, MZIs, optical modulation, balanced detection, and photonic neural-network components are established. The contribution sought is not a claim that EIS invented optical interference. The research question is whether the specific KKA mathematical mapping, physical modulator–interferometer cascade, control/calibration behavior, and acceptance contract can be independently reproduced, characterized, and extended.

The community is invited to challenge this proposition as well as help implement it. A result showing that a proposed mapping fails under a particular device, process, workload, or error budget is a valuable contribution.

## 3. Gap register

| Gap ID | Requirement IDs | Evidence gap / question | Requested contribution | Suggested contributor | Evidence that would close or refine the gap | Priority |
|---|---|---|---|---|---|---|
| GAP-001 | FAB-006, FAB-017 | Independent source-faithful reproduction of Tian KKA computation, including SI-13 details and unresolved aggregation notation | Reproducible code, derivation, or independent implementation review | Tian authors, ML researchers, photonic-computing groups | Versioned code, exact configs, known-answer outputs, documented differences | Critical |
| GAP-002 | FAB-004, FAB-005, FAB-006 | Mapping between main-paper real cross-term and SI-1 quadrature BPD observable | Independent circuit derivation and port/reference-plane review | Integrated photonics researchers, circuit-model developers | Derivation plus executable complex-field test vectors and explicit detector convention | Critical |
| GAP-003 | FAB-001, FAB-002 | Complete vertical stack and process assumptions for open SOI references | Clarify BOX, cladding, substrate, sidewall, etch, and material conventions | CORNERSTONE maintainers, foundry process engineers | Versioned stack files, material data, process documentation, uncertainty/provenance | High |
| GAP-004 | FAB-004, FAB-017 | CORNERSTONE directional-coupler tables are real-valued κ surfaces used to construct complex S models; source marks them not foundry-validated | Explain derivation, model domain, interpolation, phase convention, and available measured correlation | CORNERSTONE maintainers, compact-model researchers | Source explanation, interpolation tests, complex measured S data or model residuals | High |
| GAP-005 | FAB-003, FAB-017 | Straight-waveguide compact-model phase/loss equation and dependency conventions need pinning | Confirm exact model equation, phasor sign, wavelength dependence, and parameter meaning | CORNERSTONE model maintainers, SAX developers | Pinned source and dependency, equation, tests, measured cut-back data | High |
| GAP-006 | FAB-004, FAB-005 | Cross-platform coupler and MZI S-parameter conventions differ or may be undocumented | Agree a common port order, reference-plane, mode-normalization, and complex-S test suite | SiEPIC, CORNERSTONE, PhotonForge, SAX, academic groups | Shared test vectors and cross-tool comparison report | Critical |
| GAP-007 | FAB-007, FAB-008 | Calibrated complex amplitude–phase response is not available in a common reusable form | Share (E(V)), θ(V), and coupled-control measurements with uncertainty | Modulator and phase-shifter researchers, foundries | Measured complex field versus control, device conditions, repeatability, bandwidth | Critical |
| GAP-008 | FAB-009 | Dense heater-array thermal interaction and operating-state dependence need characterization | Provide thermal influence matrices and measurement methods | Thermal-photonics researchers, PDK maintainers, foundries | Measured Δφ versus multi-heater power/state, time response, uncertainty | Critical |
| GAP-009 | FAB-010 | Balanced detector/readout acceptance interface is not yet common across references | Provide detector models and calibration data, including gain, offset, noise, bandwidth, CMRR | Detector and readout specialists | Calibrated responsivity/noise/bandwidth and reference-plane definition | High |
| GAP-010 | FAB-011, FAB-016 | KKA-oriented test structures and wafer-level measurement plan are not yet defined | Propose minimal waveguide, coupler, MZI, heater, detector, and cascade test coupons | PDK maintainers, test engineers, university cleanrooms | Layout, test protocol, raw data schema, calibration structures | High |
| GAP-011 | FAB-015, FAB-021 | Process variation and yield impact on complex-field transfer and calibration are under-specified | Share dimensional distributions and propagate them into KKA error/yield | Foundries, process-integration engineers, statistical-modeling researchers | Process-corner data, wafer maps, Monte Carlo model, measured yield | High |
| GAP-012 | FAB-018 | Full 3D FDTD can create very large meshes before solver execution | Share validated reduced-order modeling, mesh strategies, EME/FDTD boundaries, convergence practices | EM solver developers, PDK modelers, photonic designers | Reproducible benchmark with grid/memory/runtime/cost and accuracy comparison | High |
| GAP-013 | FAB-019 | No common backend-neutral KKA lowering contract currently demonstrated across the reference PDKs | Contribute adapters and common acceptance tests | GDSFactory, SAX, PhotonForge, SiEPIC, open-source EDA developers | Working adapters, pinned versions, deterministic tests, provenance manifests | High |
| GAP-014 | FAB-014, FAB-023 | Calibration and fault isolation for tiled KKA arrays are open | Develop partitioned calibration, drift detection, and recovery methods | Control-system and photonic-array researchers | Tile-level calibration algorithm, convergence and fault-injection results | High |
| GAP-015 | FAB-022 | Cost per accepted KKA workload block is not yet supported by measured process, test, calibration, and system-energy data | Help define a fair system boundary and cost model | Foundries, packaging providers, data-center/AI systems researchers | Transparent model with measured inputs, yield, utilization, test and energy accounting | High |
| GAP-016 | FAB-024 | Community needs a clear public/private contribution boundary | Review reusable schemas, licensing, and controlled-data interfaces | Open PDK maintainers, legal/IP specialists, research collaborators | Contribution guide, license review, provenance and disclosure policy | Medium |

## 4. First collaboration wave

EIS should begin with four bounded requests rather than asking the community to solve the entire platform at once.

### A. Tian KKA reproduction and interpretation

**Question:** Can independent groups reproduce the Tian 10×1 computational baseline and validate the relationship between the paper's general interference operator, SI-1 BPD circuit, and SI-13 training pseudocode?

Requested outputs:
- source-faithful implementation and known-answer tests;
- explicit real-versus-quadrature cross-term conventions;
- documented assumptions and unresolved pseudocode interpretations;
- matched comparison with standard self-attention.

### B. Open SOI complex-field model benchmark

**Question:** Can CORNERSTONE, SiEPIC, and other open-PDK communities compare directional coupler and MZI models using one common complex-field interface?

Requested outputs:
- port and reference-plane conventions;
- complex S-parameters or field-transfer data;
- reciprocity/passivity and interpolation tests;
- measured-versus-modeled residuals where physical data are available.

### C. Amplitude–phase and thermal calibration

**Question:** What device/control structures are required to characterize the amplitude–phase coupling and thermal interaction that KKA relies on?

Requested outputs:
- (E(V)) and θ(V) data;
- heater efficiency, settling, drift, and hysteresis;
- thermal interaction matrix;
- calibration algorithm and uncertainty.

### D. Low-cost simulation and test vehicle

**Question:** What is the smallest useful test coupon and lowest-cost simulation/measurement path that can answer the KKA acceptance questions?

Requested outputs:
- reduced device coupon;
- simulation fidelity ladder (analytic, compact model, eigenmode/EME, FDTD);
- mesh/resource preflight;
- measurement plan and cost boundary.

## 5. Suggested public invitation

The following wording is suitable for a community post, project page, or direct invitation:

> **Earth ICT, SPC is opening a collaborative photonics research effort around Tian et al.'s Photonic Transformer Chip and KKA attention architecture.**
>
> We are developing an EIS requirements baseline and comparing it with open reference platforms including CORNERSTONE Si220 and SiEPIC EBeam. Our aim is to reproduce and rigorously test the use of programmable optical interference and amplitude–phase coupling in the KKA attention path, including the reported omission of conventional SoftMax in that formulation.
>
> We are not asking the community to accept a predetermined conclusion. We are looking for independent reproductions, complex-field device models, measured modulator and phase-shifter data, thermal-crosstalk characterization, detector interfaces, test-coupon designs, simulation methods, and critical reviews.
>
> Gaps are welcome: an unavailable model, incompatible port convention, uncertain process parameter, failed reproduction, or negative result helps define the engineering problem. We intend to publish reusable, non-confidential contracts, tests, and evidence so that multiple PDKs and fabrication partners can participate.
>
> Researchers, PDK maintainers, foundries, device engineers, and open-source photonic EDA developers are invited to review the requirements and propose contributions.

## 6. Contribution format

A useful contribution should include:

1. Gap ID(s) addressed.
2. Source, process, device, and tool version.
3. Exact geometry and operating conditions.
4. Model or measurement method.
5. Data and uncertainty.
6. Reproducible test or analysis.
7. Evidence state: source-reported, modeled, simulated, measured, or foundry-confirmed.
8. License and disclosure permissions.
9. Known limitations and follow-up work.

Contributions need not be positive. A reproducible incompatibility or negative result is valuable.

## 7. Open versus controlled boundary

Public contributions may include generic contracts, test vectors, open-PDK models, public measurements, non-confidential geometry, and public process information consistent with the applicable licenses.

Do not publish or upload confidential foundry PDK contents, proprietary process rules, controlled compact models, credentials, or restricted data. A foundry NDA does not automatically authorize use in external cloud simulation or LLM workflows; obtain written authorization for each relevant service and data path.

## 8. Immediate actions

1. Invite independent review of the Tian source interpretation and computational baseline.
2. Ask CORNERSTONE maintainers the specific stack, coupler-table, and straight-waveguide model questions in EIS-FAB-REF-CORNERSTONE-001.
3. Ask SiEPIC maintainers which measured device and thermal datasets can be used in a common complex-field benchmark.
4. Draft a backend-neutral complex-field device interface and known-answer test suite.
5. Select one small coupler/MZI test coupon only after geometry, stack, simulation resource, and measurement requirements are bounded.

**Community principle:** EIS owns the requirements and acceptance criteria; the photonics community can help improve the evidence, implementations, and even the requirements themselves. The goal is an open, multi-platform path to test and develop KKA—not a closed EIS-only PDK.
