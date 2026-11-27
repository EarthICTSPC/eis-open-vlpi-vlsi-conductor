# EIS-KKA-001B-TIDY3D-DC-EM-001 — SOI Directional-Coupler Electromagnetic Evidence Gate

**Status:** specification prepared; simulation BLOCKED pending geometry, stack, material, and budget inputs  
**Purpose:** obtain a converged complex optical S-matrix for one passive SOI directional coupler, then compare it with the ideal analytical coupler convention used by EIS-KKA-001B.  
**Backend:** Tidy3D cloud FDTD; use a mode-solver stage for port modes and normalization before the 3D run.  
**Separation:** this work package is independent of Tian SI-4 scalar fitting (001A), the analytical MZI model (001B), and the SiEPIC OpenEBL workflow-proxy runbook.

## 1. Gate decision

Do not submit an EM job until all required inputs in §3 are either:
- supported by an identified source/PDK and version, or
- explicitly marked `eis_assumed` for a bounded exploratory study and approved by EIS.

A reported waveguide cross-section is not a complete SOI stack. Do not infer BOX thickness, silicon thickness beyond the reported value, top cladding, substrate, sidewall angle, etch depth, slab geometry, material dispersion, or process corner from the phrase “SOI”.

No numeric gap, interaction length, taper length, wavelength, or sweep bounds are prescribed by this document. Obtain them from the target PDK/source or have EIS explicitly approve an exploratory range. Do not copy tutorial dimensions or optimization bounds.

## 2. Evidence target

The target is a passive two-waveguide directional coupler with two input and two output guided modes. The EM result must provide a complex, port-normalized 2×2 transmission matrix and, where the simulation domain supports them, reflection and radiation/leakage accounting.

Use a declared port order:
`[in_0, in_1, out_0, out_1]`.

For the forward transmission block, record:
`T[out_index, in_index]`.

The analytical comparison convention is:
[
C(\kappa)=
\begin{bmatrix}
\sqrt{1-\kappa} & \sqrt{\kappa}\\
\sqrt{\kappa} & -\sqrt{1-\kappa}
\end{bmatrix},
]
where `kappa` is the cross-coupled power fraction in the declared EIS analytical convention. The simulated device is not required to have this exact phase convention. First extract its complex S-parameters; only then compare after an explicitly documented port ordering, reference-plane, and phase-gauge transformation. Never silently rotate phases to force a match.

## 3. Input register — required before submission

| Parameter | Current status | Required evidence |
|---|---|---|
| Silicon core width | 450 nm reported in Tian source; verify source context before adopting | source citation or target PDK |
| Silicon core thickness | 220 nm reported in Tian source; verify source context before adopting | source citation or target PDK |
| BOX thickness | unknown | PDK/source value |
| Buried oxide material model | unknown | dispersive material source/model |
| Top cladding and thickness | unknown | PDK/source value |
| Substrate material and extent | unknown | PDK/source value |
| Etch depth / rib-slab geometry | unknown | PDK/source value |
| Sidewall angle / corner rounding | unknown | PDK/source value or declared idealization |
| Waveguide gap | unknown | source/PDK or EIS-approved exploratory range |
| Coupling interaction length | unknown | source/PDK or EIS-approved exploratory range |
| Access waveguide length and port planes | unknown | explicit geometry/reference-plane definition |
| Tapers / transitions | unknown | source/PDK or explicitly excluded |
| Wavelength / frequency band | unresolved for this work package | source/PDK or EIS-approved target |
| Polarization and mode | unresolved | TE/TM and mode index |
| Silicon / oxide dispersion | unknown | Tidy3D material model and provenance |
| Temperature | unknown | declared nominal condition |
| Process corners | unknown | target PDK or explicitly out of scope |
| Mesh override / resolution | not set | convergence study, not arbitrary fixed cell count |
| Boundary conditions and domain padding | not set | simulation design record |
| FlexCredit estimate | not obtained | estimate from actual candidate before submission |

The 450 nm × 220 nm cross-section is a source-reported starting datum only. It does not identify a complete foundry stack or establish that the target foundry uses the same geometry.

## 4. Simulation sequence

### Stage A — cross-section and mode preflight
1. Instantiate only the declared cross-section.
2. Solve the selected guided mode(s) at the declared wavelength(s).
3. Record effective index, mode profile, mode area or equivalent normalization metric, and solver convergence.
4. Verify that each port supports the intended mode and that the port planes are outside the coupling interaction region.
5. Stop if the intended mode is not guided or if material/geometry inputs are incomplete.

### Stage B — directional-coupler FDTD
1. Construct two parallel waveguides with declared gap and interaction length.
2. Add access sections and tapers only if specified in the input register.
3. Use mode sources and mode monitors at fixed reference planes.
4. Simulate excitation from each input port, or use a validated multi-port extraction workflow.
5. Extract complex transmission and reflection coefficients, not just field intensity.
6. Record radiated/leaked power or an explicit residual power balance where available.

### Stage C — convergence and sweep
1. Perform mesh refinement until complex S-parameter changes meet a predeclared tolerance.
2. Check domain padding and boundary-condition sensitivity.
3. Sweep only approved geometry variables (at minimum gap and interaction length once bounds are supplied).
4. Preserve every candidate's exact geometry, material IDs, solver settings, job ID, and raw S-parameter result.
5. Do not optimize until a reproducible baseline and a cost estimate exist.

## 5. Required outputs

For every run:
- immutable input manifest with provenance labels (`tian_reported`, `foundry_pdk`, `eis_assumed`, `simulated`);
- Tidy3D and PhotonForge versions;
- material model identifiers and dispersion provenance;
- wavelength/frequency and polarization;
- geometry dimensions and reference planes;
- mesh, boundary conditions, simulation time and convergence evidence;
- complex S-parameters with explicit input/output indexing;
- power balance, reflection, excess loss and cross-coupled power;
- cloud task/job identifier and actual credit cost;
- raw data location and checksum.

The reduced comparison record should include:
- `kappa_power = |T[out_1,in_0]|^2` under the declared port mapping;
- through/cross amplitudes and phases;
- reciprocity residual where the simulated model and port normalization support that test;
- energy/power balance including radiation and absorption where measurable;
- complex difference from the analytical coupler only after the phase/reference-plane mapping is stated.

## 6. Acceptance gates

| Gate | Acceptance |
|---|---|
| G0 Inputs | all required geometry/material/frequency inputs sourced or explicitly approved as exploratory assumptions |
| G1 Mode | intended port modes exist and are normalized consistently |
| G2 Baseline EM | complex S-matrix extracted with fixed reference planes and port order |
| G3 Convergence | mesh and domain sensitivity within predeclared tolerances |
| G4 Physical checks | reciprocity and power accounting assessed; unexplained excess power is a failure |
| G5 Sweep | approved gap/length sweep is reproducible and fully provenance-tagged |
| G6 Cross-backend | PhotonForge/Tidy3D complex S comparison uses the same frequency, ports, normalization, and reference planes |

Numerical tolerances must be declared before the relevant run. Do not choose tolerances after inspecting the result.

## 7. Cost and authorization gate

Before cloud submission:
- run the Tidy3D cost estimate on the actual proposed simulation;
- record expected credits, run count, mesh size, simulation time and storage;
- obtain explicit EIS approval for the estimated spend;
- verify account balance/limits and data-handling permissions.

No cloud submission is authorized by this document. No GlobalFoundries NDA-restricted PDK material may be uploaded to Tidy3D, PhotonForge, or an LLM/agent unless the applicable NDA, service terms and EIS authorization permit that use.

## 8. Current disposition

**BLOCKED — INPUTS REQUIRED.** The current source record supplies a reported 450 nm × 220 nm waveguide cross-section, but not the complete stack, coupler gap/length, wavelength/polarization, material dispersion, or approved sweep bounds needed for a defensible Tian-oriented SOI coupler simulation.

The next engineering action is to populate the input register from an authorized target PDK/source or explicitly approve an exploratory stack and geometry. Until then, do not invent a nominal device, submit a cloud job, or describe any generated field plot as physical evidence.
