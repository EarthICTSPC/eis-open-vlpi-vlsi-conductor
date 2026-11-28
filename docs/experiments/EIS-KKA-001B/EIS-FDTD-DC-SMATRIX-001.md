# EIS-FDTD-DC-SMATRIX-001 — Directional-Coupler Modal S-Matrix Characterization

**Status:** exploratory field evidence recorded; modal S-matrix characterization not yet performed  
**Parent context:** EIS-KKA-001B analytical SOI MZI complex-field reference and EIS-KKA-001B-TIDY3D-DC-EM-001  
**Backend:** FlexCompute / Tidy3D FDTD and local mode solver; PhotonForge is the downstream circuit-model target  
**Purpose:** turn a bounded exploratory two-waveguide FDTD model into a reproducible, port-normalized complex scattering model suitable for comparison with the EIS analytical coupler and later use as a PhotonForge component model.

## 1. Engineering decision

Do not netlist the present exploratory field result as a characterized component.

The completed simulations demonstrate that the Tidy3D workflow can construct, upload, execute, and return finite electromagnetic field data for an idealized silicon-waveguide structure. They do not yet provide a calibrated coupling coefficient, complex S-matrix, foundry process model, or Tian-device reproduction.

The next lowering step is therefore **modal port characterization**, not fitting an ideal 2×2 coupler matrix to regional field-window integrals.

The target is a passive reciprocal two-waveguide coupler with four external guided-mode ports. Define the port order once and preserve it across Tidy3D extraction, the EIS evidence record, and PhotonForge:

`[L0, L1, R0, R1]`

where L0/L1 are the left ends of the lower/upper guides and R0/R1 are their right ends. Define the full scattering matrix by

`b_i = sum_j S[i,j] a_j`

with each `a_j` and `b_i` a complex, power-normalized incident/outgoing guided-mode amplitude at its declared reference plane. Matrix rows are outgoing ports and columns are excited incident ports. Document the propagation direction associated with each port.

## 2. Evidence already obtained

### 2.1 Straight-waveguide workflow smoke tests

The EIS idealized straight silicon guide FDTD workflow completed successfully, returned field data, and supported a local mode solve. The baseline used a 450 nm × 220 nm silicon core in uniform silica at 1.55 µm. This is an EIS exploratory geometry using Tian-reported cross-section dimensions, not a complete SOI process stack.

The revised straight-guide modal-monitor run reported approximately 99.974% output/input forward fundamental-mode power at the two monitor planes. The input and output backward modal powers were also nonzero (about 12.15% and 12.16% of forward modal power, respectively). These are results for the stated finite simulation and reference planes, not a validated foundry transmission or reflection specification.

### 2.2 Single-plane directional-coupler exploration

Task `fdve-bac2992c-9cd4-4ecb-8f5c-5db31f065f5d` (`EIS-FDTD-DC-EXPLORATION-001`) completed without divergence. One transverse field plane at x = +4.5 µm showed positive signed x-directed flux in both guide windows. Integrating the two approximate 450 nm guide windows gave lower-guide 74.09% and upper-guide 25.91% of the sum of those two regional signed fluxes.

These percentages are **not** calibrated coupling efficiencies: the plane lies inside the coupling section; the source is not normalized against independent port modes at external reference planes; and the regional integration is not a modal decomposition.

### 2.3 Six-plane longitudinal exploration

Task `fdve-92d41bd2-9046-4de0-8138-1c7b52940894` (`EIS-FDTD-DC-EXPLORATION-002`) completed with `diverged=False`. All six field monitors returned finite Ex data with shape `(1, 44, 20, 1)`.

The sampled planes and regional signed-flux results were:

| x (µm) | Lower guide | Upper guide | Total monitor flux | Lower share of guide-window sum | Upper share of guide-window sum |
|---:|---:|---:|---:|---:|---:|
| -3.5 | 0.910835 | -0.089148 | 0.875158 | 110.85% | -10.85% |
| -1.5 | 0.889398 | -0.064729 | 0.876979 | 107.85% | -7.85% |
| 0.0 | 0.870724 | -0.015469 | 0.908348 | 101.81% | -1.81% |
| 1.5 | 0.787011 | 0.043538 | 0.877840 | 94.76% | 5.24% |
| 3.5 | 0.674098 | 0.154316 | 0.872284 | 81.37% | 18.63% |
| 4.5 | 0.611533 | 0.213897 | 0.852280 | 74.09% | 25.91% |

Flux was calculated from

`S_x = 1/2 Re(E_y H_z^* - E_z H_y^*)`

and integrated over approximate transverse windows y ∈ [-0.55,-0.10] µm and y ∈ [0.10,0.55] µm, and the recorded z coordinates. The signed regional integrals are not guaranteed to be positive or independently conserved. Negative upper-window values at early planes indicate net backward x-directed flux in that finite window; they are not negative optical power. The percentages are normalized to the sum of the two regional signed integrals, so they can be negative or exceed 100%.

The trend is consistent with progressive redistribution of forward-propagating field toward the upper guide, but it does not by itself establish a coupling efficiency, coupling phase, reflection coefficient, or loss.

### 2.4 Exact exploratory model boundary

The coupler exploration used:
- silicon core dimensions: 450 nm width × 220 nm thickness;
- two parallel guides with 200 nm edge gap and 650 nm center separation;
- interaction section from x = -6 µm to +6 µm (12 µm);
- uniform silica background with relative permittivity 1.444²;
- silicon relative permittivity 3.48²;
- wavelength 1.55 µm;
- one mode source centered on the lower guide at x = -4.5 µm;
- six transverse field monitors at x = [-3.5, -1.5, 0, 1.5, 3.5, 4.5] µm.

The 450 nm × 220 nm dimensions are Tian-reported starting dimensions. Gap, interaction length, uniform background, material constants, and remaining idealizations are EIS exploratory assumptions. The source plane is inside the nominal interaction-section x extent, and the field-monitor planes are not four external port reference planes. No complete SOI BOX/cladding/substrate stack, foundry PDK, process corner, or measured device data is represented.

The six-plane task was uploaded with a maximum estimated cost of 0.025 FlexCredits and explicitly approved before launch. The actual billed cost for this task has not yet been recorded in this work package; retrieve it from the provider task record before closing the cost ledger.

## 3. Why the regional-flux result is not an S-matrix

The current post-processing integrates local Poynting flux over geometric y-windows. It does not project the field onto normalized guided eigenmodes. In a coupled structure, the finite windows can include:
- evanescent fields and overlapping modal tails;
- interference between local supermodes;
- backward-propagating fields;
- radiation and fields outside the selected windows;
- truncation error from finite monitor apertures and grid sampling.

Consequently, the regional integrals cannot be substituted for `|S_ij|²`. Do not infer coupling phase from intensity or signed regional flux.

A component model for PhotonForge requires complex modal amplitudes at declared ports, with reference-plane phase and normalization controlled. That is the objective of this work package.

## 4. Required lowering sequence

### Stage A — external access geometry and port definition

1. Preserve the exploratory geometry as an immutable baseline; do not silently overwrite it.
2. Add straight access sections on both sides of the coupling region so all four modal reference planes lie outside the interaction region and outside significant near-field overlap.
3. Ensure the source and monitor apertures capture the full intended guided mode, including relevant evanescent tails.
4. Declare the physical port order `[L0, L1, R0, R1]`, each port plane, outward normal, and incident/outgoing direction.
5. Verify adequate distance from sources, PML boundaries, discontinuities, and coupling region. A geometric clearance check is necessary but not sufficient; test boundary sensitivity.
6. Keep all new dimensions not supplied by Tian or an authorized PDK explicitly tagged `eis_assumed`.

### Stage B — port eigenmodes and normalization

1. Solve the guided eigenmodes at each port cross-section at the declared frequency.
2. Record effective index, mode profile, polarization fractions, mode area, and mode-solver settings/version.
3. Establish a consistent power normalization for each port mode. Verify the normalization using the solver's documented modal-flux or mode-amplitude convention.
4. Verify that the selected mode is guided and that the mode-monitor plane is in a uniform access section.
5. Use a declared mode-selection policy; do not depend on deprecated implicit polarization filtering.
6. Inspect actual returned `ModeData.amps` dimensions, direction labels, frequency coordinates, and normalization before calculating S.

### Stage C — independent port excitations and complex S extraction

For a full four-port S-matrix, run one independent excitation per incident port unless a documented solver method provides an equivalent validated multiport extraction. For each excitation:
1. inject the selected normalized mode at one port;
2. record outgoing modal amplitudes at all four ports;
3. distinguish incident and outgoing directions at the excited port;
4. preserve complex amplitudes, not only magnitudes or powers;
5. record residual radiation/absorption/power not captured by the four guided modes.

Assemble columns by incident port and rows by outgoing port. Verify index ordering with deterministic synthetic vectors before populating the matrix. If a reduced two-excitation approach is later used, justify it from a verified reciprocity and symmetry contract; do not assume symmetry merely because the drawn geometry looks symmetric.

### Stage D — physical and numerical checks

Assess the following with tolerances declared before evaluating results:

- **Finiteness:** all complex S entries finite.
- **Reciprocity:** compare the appropriately power-normalized S matrix with its transpose, accounting for the declared port basis and reference planes.
- **Passivity:** for a passive model, test the largest singular value of S against 1 within numerical tolerance. If material absorption or radiation channels are excluded from S, do not mistake a subunitary guided-port matrix for a failure.
- **Power balance:** for each incident port, account for guided outputs, reflected modes, radiation, and absorption where the simulation supports it. Record unaccounted residual explicitly.
- **Convergence:** repeat at progressively refined meshes and, where relevant, increased simulation time/domain padding. Compare complex S entries, not only power ratios.
- **Reference-plane stability:** shift port planes within uniform access sections and verify the expected propagation-phase change; de-embed to a declared common reference plane before comparing devices.
- **Boundary sensitivity:** verify that PML/domain changes do not materially alter the extracted S matrix.

Do not use an arbitrary post hoc tolerance. Set numerical thresholds in the run manifest before the corresponding jobs.

### Stage E — PhotonForge component lowering

1. Create a PhotonForge component with the same four-port order, mode/polarization, frequency convention, and reference planes.
2. Import the complex Tidy3D S data without fitting away unexplained discrepancies.
3. Compare PhotonForge component response with the source Tidy3D data at matching frequencies.
4. Test reciprocity, passivity/contractivity, port permutation, and deterministic known-answer vectors.
5. Label the model `simulated` and `exploratory`; do not label it measured, foundry-qualified, or Tian-reproduced.
6. Only after the component-level contract passes should it be connected into the separate analytical MZI/KKA circuit model.

## 5. Required machine-readable evidence record

Each simulation candidate must retain a manifest with at least:

- work-package ID and immutable candidate ID;
- source geometry and all EIS assumptions;
- port IDs, port-plane coordinates, outward directions, and reference-plane convention;
- material identifiers, dispersion provenance, and temperature assumption;
- wavelength/frequency, polarization, selected mode index, and mode-selection policy;
- solver and Python package versions;
- grid specification, grid point count, mesh-convergence sequence, domain and boundary settings;
- source definition, incident-power normalization, monitor definitions, and run time;
- raw complex modal amplitudes for each excitation;
- assembled complex S matrix and explicit row/column ordering;
- reciprocity, passivity, power-balance, convergence, and reference-plane residuals;
- Tidy3D task IDs, estimated and actual FlexCredit costs, timestamps, and raw-data checksums;
- evidence labels: `source_reported`, `foundry_pdk`, `eis_assumed`, `simulated`, `fitted`, `measured`, or `foundry_confidential`.

Never copy a value from one evidence class into another without a traceable derivation.

## 6. Acceptance gates

| Gate | Acceptance condition |
|---|---|
| G0 — geometry | Four external access ports defined; every non-source dimension sourced or explicitly EIS-approved as an assumption |
| G1 — modes | Port modes solved, guided, consistently normalized, and independently reproducible |
| G2 — extraction | Four independent incident-port cases (or a justified validated equivalent) produce a finite complex 4×4 S matrix |
| G3 — numerical validity | Reciprocity, passivity, power balance, convergence, and reference-plane behavior evaluated against predeclared tolerances |
| G4 — backend consistency | PhotonForge reproduces the imported complex S response within predeclared tolerance at matching frequencies |
| G5 — circuit integration | Characterized coupler can be connected to the separate EIS-KKA-001B analytical MZI model without changing its mathematical contract |

Passing G0–G4 characterizes this simulated exploratory component only. It does not establish foundry qualification, fabrication yield, Tian circuit reproduction, thermal performance, or transformer-level computational equivalence.

## 7. Cost and authorization gate

For every cloud run:
1. construct and validate the candidate locally in the notebook;
2. report grid points, estimated complexity, simulation time, number of excitations, storage/monitor load, and Tidy3D version;
3. upload only to obtain a provider estimate;
4. show the maximum estimated FlexCredit cost and projected remaining balance;
5. obtain explicit EIS approval before calling `job.start()`;
6. after completion, record provider-reported actual cost.

The prior 0.025 FlexCredit approval applied to the six-plane longitudinal task only. It does not authorize any new mode or S-matrix job. Keep the experiments small and bounded; use local mode solves and inexpensive preflight checks before cloud FDTD where possible.

Do not upload GlobalFoundries NDA-restricted PDK data or other confidential foundry inputs to FlexCompute, PhotonForge, or LLM/agent services unless the applicable agreements and service terms expressly permit that use and EIS authorizes it.

## 8. Current disposition and next action

**Current status: G0 NOT MET for S-matrix extraction; exploratory field run PASS as a workflow smoke test.**

The next notebook action is a bounded geometry/port-preflight revision:
- add sufficiently long straight access sections on both sides;
- place four candidate mode-monitor planes in uniform guide sections;
- run local mode solves at all four ports;
- verify source/monitor separation, port orientation, mode normalization, and grid estimate;
- do not upload or start a new cloud job until the actual candidate is preflighted, cost-estimated, and separately approved.

The existing six-plane data remain valid as a record of the stated exploratory simulation. They must not be relabeled as modal S-parameters or a calibrated coupling ratio.
