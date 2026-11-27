# EIS-KKA-001B-SIEPIC-OPT-001 — Open-PDK Optimization Pipeline Test

**Status:** prepared for execution; cloud submission not yet performed
**Purpose:** validate the PhotonForge → Tidy3D design-space optimization workflow while the GlobalFoundries PDK/NDA handshake is pending.
**Reference workflow:** FlexCompute PhotonForge 2.x MMI Optimization with Tidy3D Design Plugin.

## Decision: use SiEPIC OpenEBL as a workflow proxy, not as Tian's process

Use the public SiEPIC OpenEBL PDK (siepic-forge, technology initialized with siepic_forge.ebeam()) for the first optimization pipeline test. FlexCompute's published workflow explicitly uses this PDK for a 1×2 MMI, parameter sweep, Bayesian optimization and adjoint refinement.

This validates that EIS can express an optimization problem, execute a bounded search, collect S-matrix evidence and preserve candidate provenance in the FlexCompute stack.

**It does not reproduce Tian's KKA PTC process.** The SiEPIC EBeam technology is a 220-nm SOI platform with its own layer stack and rules. Tian's paper reports a 450 nm × 220 nm waveguide cross-section and TiN heater geometry. A SiEPIC result must not be presented as Tian-device evidence, a Tian PDK, or GlobalFoundries process qualification.

Do not alter SiEPIC's PDK parameters to force a visual match to Tian. Do not label a SiEPIC PDK cell as tianReported.

## Why not fabricate a mock Tian PDK first?

A mock EIS PDK is useful later for architecture integration, but without a validated stack, material models, foundry rules, component models and thermal/electrical models it would mostly test EIS's own assumptions. The SiEPIC workflow provides an independently maintained public technology and a documented FlexCompute optimization example. It is the cleaner first test of the optimization machinery.

After this workflow test, create a separate EIS-TIAN-KKA-EXPLORATORY custom technology only when each non-source stack parameter is explicitly marked eisAssumed and the purpose is clearly exploratory.

## Scope of the first run

Optimize **one passive 1×2 MMI splitter** in SiEPIC OpenEBL. Do not attempt the whole MZI or the 10-output chip in this first cloud run.

The initial run should follow the published PhotonForge notebook structure:

1. Load siepic_forge.ebeam() and set it as PhotonForge's default technology.
2. Construct a parametric 1×2 MMI with fixed external port reference planes.
3. Define the objective from the simulated S-matrix. Include output transmission, imbalance and reflection/leakage in the recorded metrics; do not use transmission alone as a proxy for all MZI requirements.
4. Run a small reproducible design-space sweep and Bayesian search.
5. Estimate FlexCredit cost before starting the full run. Upload-only/preflight is preferred if cost cannot be estimated.
6. Refine only after the global search and only if the adjoint workflow is available and the budget is approved.
7. Re-simulate the selected candidate at the higher mesh refinement and over the specified wavelength band.
8. Save the complete candidate manifest, PDK version, PhotonForge/Tidy3D versions, seed, bounds, S-matrix, objective definitions, job IDs and credit costs.

The public tutorial demonstrates a workflow using Bayesian optimization (initial_iter=4, n_iter=6, fixed seed) followed by local adjoint refinement. Those iteration counts are a suggested smoke-test pattern, not a guaranteed credit budget. The tutorial's sample geometric spans and optimum values are **not** EIS or foundry-approved bounds and must not be copied into the EIS Tian design-space manifest.

## Acceptance criteria for this workflow test

- PDK identity and version are recorded.
- All optimized variables have finite bounds and provenance.
- Search seed and algorithm settings are fixed and recorded.
- The cloud job is submitted only after a cost estimate and explicit budget approval.
- Candidate result includes S-matrix over the required band and reference planes.
- DRC / port connectivity and component geometry are checked.
- Re-running with the same inputs and seed produces a reproducible or explainably version-dependent result.
- No claim is made that the result validates Tian KKA, heater behavior, the shared-B broadcast architecture, or GlobalFoundries manufacturability.

## EIS integration boundary

This run is a **toolchain qualification experiment**, not a source of physical parameters for the Tian MZI. The resulting SiEPIC MMI may be registered as a SiEPIC component in a test registry. It must not be substituted for the EIS/Tian MMI cell.

The EIS MZI analytical complex-field model remains independent. The Tian SI-4 calibration reference (001A) remains read-only. The KKA voltage-to-complex-field adapter remains a separate workstream.

## Execution prerequisites and current blocker

The current ChatGPT execution environment has no FlexCompute/Tidy3D account connector, no PhotonForge runtime and no Tidy3D cloud credentials exposed to the task. Therefore this document is **prepared but not submitted**. Actual cloud submission must occur in the authenticated FlexCompute/Tidy3D notebook or local PhotonForge environment.

Before running:

- install photonforge and siepic-forge;
- install the Tidy3D design plugin dependencies required by the current PhotonForge tutorial;
- confirm td.web.test() succeeds;
- inspect account limits and FlexCredit balance;
- run the documented cost estimate for the actual candidate simulation;
- obtain approval for the estimated spend.

Do not paste GlobalFoundries NDA-restricted PDK files, rule decks, models or derived confidential data into the public SiEPIC test or any external service unless the NDA and FlexCompute terms explicitly permit it.

## Official workflow references

- PhotonForge 2.x MMI optimization notebook: https://docs.flexcompute.com/photonforge/latest/notebooks/MMI_Optimization_With_Tidy3d_Design_Plugin/
- PhotonForge PDK overview and open PDK install: https://docs.flexcompute.com/photonforge/latest/
- Tidy3D cloud submission API: https://docs.flexcompute.com/projects/tidy3d/en/stable/api/submit_simulations.html
