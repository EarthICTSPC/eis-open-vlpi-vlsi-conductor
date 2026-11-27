# EIS-FAB-REF-SIEPIC-001 — SiEPIC EBeam Evidence Assessment

**Parent specification:** [EIS-FAB-REQ-001](EIS-FAB-REQ-001.md)  
**Status:** Read-only environment and source inventory; no new installation or simulation authorized  
**Reference:** [SiEPIC EBeam PDK](https://github.com/SiEPIC/SiEPIC_EBeam_PDK), SiEPIC-Tools / KLayout ecosystem, and [PhotonForge SiEPIC workflow documentation](https://docs.flexcompute.com/projects/photonforge/en/latest/quick_start/passive.html).  
**Inspected package:** `siepic-forge` 1.2.2; PhotonForge 1.5.1 in the EIS notebook environment.

## 1. Purpose

SiEPIC EBeam is a useful open workflow and technology reference. It provides a practical example of how a silicon photonics PDK can expose layers, port specifications, components, geometry, and simulation models to layout and verification tools.

It is **not** assumed to be the EIS target process, a Tian process replica, or a KKA implementation. Its value is as a tertiary reference for tooling, component interfaces, layout conventions, and reproducible device-model workflows.

## 2. Environment evidence

The inspected EIS notebook environment reported:

| Package/tool | Observed state |
|---|---|
| PhotonForge | 1.5.1, import available |
| Tidy3D | 2.12.0.dev2 in the later inventory cell; earlier notebook state reported 2.11.2, so version drift must be resolved in manifests |
| `siepic-forge` | 1.2.2, import available |
| `cspdk` | Not installed |
| GDSFactory | Not installed |
| SAX | Not installed as a direct import in the inventory cell |
| KLayout / SiEPIC-Tools | Not found as installed modules in the inventory cell |

The SiEPIC technology factory `siepic_forge.ebeam()` returned a PhotonForge `Technology` named **SiEPIC EBeam Si**, version 1.2.2. It was inspected explicitly rather than silently activated as the default technology.

The environment result is specific to the notebook session and must not be treated as a universal installation statement.

## 3. Technology inventory

The inspected technology exposes 61 layer names, 12 port specifications, and 23 component names.

Representative layer groups include:

- silicon waveguide layer `Si` (1,0);
- partial-etch slab `Si Slab` (2,0);
- heater and metal-routing layers;
- bond-pad opening and doping layers;
- pin-recognition, device-recognition, text, error, and reserved/admin layers.

The 61 layer names are not 61 fabricated optical process layers. Some are administrative, recognition, text, or DRC layers and must be classified separately from physical process layers.

Representative port specifications include:

- `TE_1550_500`: TE, 1550 nm, 500 nm strip;
- `Rib_TE_1550_500`: TE, 1550 nm, 500 nm rib with 90 nm slab;
- additional 1310 nm, TM, and slot-waveguide specifications.

The inspected component inventory did not expose a clearly named KKA component or a source-matched Tian dual-MZI KKA cascade. Component presence must be evaluated by behavior and model evidence, not name matching alone.

## 4. Technology defaults and material conventions

The inspected SiEPIC EBeam factory exposed defaults including:

| Parameter | Source default | EIS interpretation |
|---|---:|---|
| Silicon thickness | 0.22 µm | SiEPIC process datum; coincidentally same nominal thickness as Tian's reported waveguide thickness, but no process equivalence follows |
| Silicon slab thickness | 0.09 µm | SiEPIC partial-etch datum |
| Bottom oxide thickness | 2.0 µm | SiEPIC technology default |
| Top oxide thickness | 2.2 µm | SiEPIC technology default |
| Passivation oxide | 0.3 µm | SiEPIC technology default |
| Heater thickness | 0.2 µm | SiEPIC technology default |
| Router metal thickness | 0.6 µm | SiEPIC technology default |
| Sidewall angle | 0° | Source default; confirm angle convention |
| Silicon optical material | `cSi_Li1993_293K` | Material model identifier |
| SiO2 optical material | `SiO2_Palik_LowLoss` | Material model identifier |
| Heater / router material | Tungsten / gold model identifiers in inspected defaults | Optical and electrical material assignments are model conventions; inspect exact properties before EM use |

These are SiEPIC defaults, not Tian or CORNERSTONE values. The fact that the nominal silicon thickness is 220 nm in both SiEPIC and Tian does not make the process stacks interchangeable.

## 5. Directional coupler component inspection

A candidate component `ebeam_bdc_te1550` was instantiated using the explicit SiEPIC technology object.

Observed properties:

- four optical ports P0–P3;
- TE 1550 nm, 500 nm strip port specifications;
- left and right port groups with the expected opposing directions;
- an active PhotonForge Tidy3D model attached;
- layout structures for silicon geometry plus pin/device-recognition records;
- labels describing the component as a 50:50 broadband splitter and citing a 2015 Optics Express reference.

The “50:50 broadband splitter” text is a component label, not a measured result from this EIS inspection. The component's attached Tidy3D model is a simulation route, not proof of foundry-measured complex S parameters.

The local geometry was extruded using the technology's optical extrusion rules. The extrusion completed and a local simulation object was constructed and passed the Tidy3D pre-upload validation method. No cloud simulation was uploaded or executed.

The inspected provisional simulation grid contained approximately:

- Nx = 3,328;
- Ny = 426;
- Nz = 176;
- 249,520,128 grid points;
- minimum spacing approximately 0.0167 µm;
- reported computational-complexity estimate approximately 14.97 billion.

These are software-generated estimates for that specific provisional model and mesh. They are not a cost quote, measured memory consumption, runtime, or universal property of SiEPIC. They demonstrate why EIS requires geometry and resource preflight before cloud upload or FDTD execution.

## 6. What SiEPIC provides to EIS

| Capability | Evidence | Assessment |
|---|---|---|
| PDK technology object | `siepic_forge.ebeam()` returns a PhotonForge technology | SUPPORTED for this integration/version |
| Layer and port definitions | 61 layer names, 12 port specifications inspected | SUPPORTED as technology metadata; physical/admin layer classification required |
| Component library | 23 component names inspected | SUPPORTED as library inventory; KKA behavior not established |
| Directional coupler | Four-port `ebeam_bdc_te1550` component with Tidy3D model | PARTIAL; no EIS-run S-matrix or measured comparison |
| 3D geometry conversion | Local optical extrusion completed | SUPPORTED as local geometry-conversion test |
| Simulation construction | Local Tidy3D simulation object constructed | SUPPORTED as local construction test |
| Pre-upload validation | `validate_pre_upload` passed | SUPPORTED for API validation only |
| FDTD execution | No upload or solver execution | NOT PERFORMED |
| Foundry measurement | Not established by this inspection | NOT ASSESSED |
| KKA cell / dual-MZI topology | No source-matched KKA cell identified in inspected component inventory | GAP |
| Amplitude–phase coupling | Not established by inspected coupler component | GAP / NOT ASSESSED |
| Dense thermal-crosstalk data | Not established by inspected technology inventory | GAP |
| Integrated BPD calibration | Not established by inspected component inventory | GAP |
| 64×64 KKA tile | Not present in inspected evidence | NOT SUPPORTED by current evidence |

## 7. EIS-specific gaps and questions

1. Does the SiEPIC EBeam model provide measured complex S-parameters or simulation-derived S-parameters for each relevant device?
2. What are the exact reference planes, port conventions, mode normalization, and wavelength/polarization limits?
3. Can the directional coupler be compared against independent measured data and a common EIS complex-field acceptance test?
4. What heater efficiency, phase range, settling, drift, and thermal-crosstalk measurements are available?
5. Are there reusable MZI, MZM, photodetector, balanced-detector, and electrical-interface models with calibrated data?
6. What are the process-corner and dimensional-variation distributions for critical waveguide and coupler features?
7. Which parts of the SiEPIC EBeam technology are directly supported by PhotonForge and which require separate KLayout/SiEPIC-Tools workflows?
8. Can the community provide a compact, low-resource reference test case to benchmark geometry, extrusion, mesh, and S-parameter convergence across tools?

## 8. Resource-gating lesson

The provisional 249.5-million-grid-point model is an important engineering finding, but it does not imply that SiEPIC is inherently too large or that another PDK automatically solves the problem. Mesh size depends on the geometry, simulation domain, vertical stack, wavelength, material contrast, source/monitor placement, boundary conditions, and mesh policy.

EIS should therefore apply the same preflight contract to all reference platforms:

- geometry and bounding-box review;
- material and vertical-stack review;
- source/monitor/reference-plane review;
- mesh and convergence policy;
- grid-point and computational-complexity estimate;
- memory/runtime estimate where supported;
- current credit/cost estimate;
- explicit authorization before any cloud upload or solver execution.

The goal is not to minimize grid count at the expense of physical fidelity. The goal is the least expensive model that can answer the stated acceptance question.

## 9. Requirement mapping

| EIS-FAB-REQ-001 IDs | SiEPIC evidence contribution | Assessment |
|---|---|---|
| FAB-001, FAB-002 | Technology defaults, layer stack, strip/rib port specs | PARTIAL; process-specific and not transferable |
| FAB-003 | Tidy3D-backed component model path | NOT YET ASSESSED by simulation/measurement |
| FAB-004, FAB-005 | Four-port coupler component and device library | PARTIAL; S-matrix evidence not executed |
| FAB-006 | No identified KKA cell/cascade | GAP |
| FAB-007, FAB-008 | Heater layer and component support | PARTIAL; no KKA amplitude–phase calibration evidence |
| FAB-009 | No thermal interaction matrix in this audit | GAP / NOT ASSESSED |
| FAB-010 | Detector capability requires further inventory | NOT ASSESSED |
| FAB-011, FAB-016 | Ports and component structures available | PARTIAL; wafer-level test/measurement not demonstrated here |
| FAB-017 | PhotonForge Tidy3D model integration | PARTIAL; model fidelity and measurement correlation open |
| FAB-018 | Local extrusion and pre-upload validation; large estimated mesh | SUPPORTED for preflight lesson, not solver evidence |
| FAB-019 | PhotonForge technology integration | SUPPORTED for SiEPIC EBeam 1.2.2 / PhotonForge 1.5.1 inspection |
| FAB-020 | Local JSON/evidence capture possible | PARTIAL; complete traceability and measured data remain open |

## 10. Community collaboration opportunities

EIS can contribute back by:

- publishing generic KKA acceptance interfaces without disclosing controlled foundry material;
- providing a source-independent complex-field test suite for four-port couplers and MZIs;
- reporting reproducible PhotonForge/Tidy3D preflight findings, including resource estimates and failure modes;
- asking for measured coupler and heater datasets with reference planes and uncertainty;
- proposing a small open KKA-oriented test coupon or benchmark circuit;
- sharing a backend-neutral device contract that can be lowered into SiEPIC, CORNERSTONE, and other PDK workflows.

**EIS position:** SiEPIC is a valuable open workflow and technology reference. The inspected environment proves useful integration and local model-construction steps, not physical qualification or KKA capability. Its gaps are invitations to collaborate, not grounds for dismissing the platform.
