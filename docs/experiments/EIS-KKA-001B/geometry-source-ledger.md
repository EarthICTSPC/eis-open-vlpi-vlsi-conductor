# EIS-KKA-001B — Geometry and Source Ledger

**Status:** Gate 1 — source review performed; physical geometry is not yet simulation-ready  
**Authority:** Tian et al., *Photonic transformer chip: interference is all you need*, PhotoniX 6, 45 (2025), DOI: 10.1186/s43074-025-00182-7, including Supporting Information (SI).  
**Purpose:** distinguish source-reported facts from unknowns and EIS choices before constructing any physical model.

## Source facts

| Parameter | Source statement | Classification | Gate status |
|---|---|---|---|
| Foundry/process | CUMEC CSiP-180AL platform | `tian_reported` | Reported; process stack files not supplied |
| Device platform | Silicon photonic chip / SOI waveguide | `tian_reported` | Reported at platform level |
| Waveguide cross-section | 450 nm × 220 nm | `tian_reported` | Dimensions reported; cross-section profile and slab details not specified in cited SI text |
| MZI count | 11 MZIs; SI-3 reports 33 thermo-optic phase shifters | `tian_reported` | Reported |
| Splitter topology | MZIs employ one 1×2 MMI and one 2×2 MMI as 50:50 beam splitters | `tian_reported` | Correct physical topology; dimensions not reported in cited text |
| Heater | TiN, 200 µm long × 2 µm wide × 120 nm thick | `tian_reported` | Reported |
| Heater sheet resistance | 12 Ω/sq | `tian_reported` | Reported in main article methods |
| Heater resistance | Around 1 kΩ | `tian_reported` | Reported as measured approximate value |
| Optical source | C-band tunable laser, model TSP-400 | `tian_reported` | Band and model reported; exact operating wavelength not specified |
| Polarization | Input passes through a polarization controller | `tian_reported` | Controller reported; selected state (TE/TM) not specified |
| Chip temperature | 25 ± 0.2 °C using TEC/thermistor feedback | `tian_reported` | Reported |
| Input/output coupling | Edge coupler for input; output grating array and fiber array | `tian_reported` | Reported; coupling geometry and reference planes not specified |
| Output detection | Paired grating-coupler outputs measured by optical power meters for the passive prototype | `tian_reported` | Reported |

## Explicit unknowns — do not fill by convention

| Parameter | Current value | Classification | Evidence needed |
|---|---|---|---|
| Silicon device-layer thickness beyond stated 220 nm waveguide height | Unknown | `source_unknown` | Foundry stack/process documentation or authors' clarification |
| Silicon waveguide width interpretation/profile, sidewall angle, etch depth and slab | 450 nm nominal width is reported; profile details unknown | `source_unknown` | Cross-section drawing or process design manual |
| BOX thickness, handle substrate and buried-layer details | Unknown | `source_unknown` | CSiP-180AL stack |
| Top cladding material and thickness | Unknown | `source_unknown` | Process stack |
| Material refractive-index dispersion and absorption for Si, oxide/cladding, TiN | Unknown | `source_unknown` | Process-specific measured or foundry data with temperature and wavelength range |
| Exact laser wavelength(s) used for the reported calibration | C-band only | `source_unknown` | Raw experiment log or supplementary detail |
| Polarization state / modal family | Polarization controller used; TE/TM not identified | `source_unknown` | Experiment log, mode images, or authors' clarification |
| 1×2 and 2×2 MMI length, width, access taper, port spacing and transition geometry | Unknown | `source_unknown` | Layout/GDS, dimensions, or complex S-parameter measurement |
| MMI reference planes and de-embedding convention | Unknown | `source_unknown` | Layout and measurement definition |
| Arm lengths, bends, crossings and routing | Unknown | `source_unknown` | Layout/GDS or dimensioned schematic |
| Heater-to-waveguide offset, heater stack, metal contacts and thermal boundary | Heater dimensions reported; placement/stack unknown | `source_unknown` | Layout/process stack |
| Optical power normalization and complex input-field reference planes | Unknown | `source_unknown` | Measurement definition |
| Device-level complex S-parameters | Not supplied in the source data reviewed | `source_unknown` | Measurement or independently generated EM model |

## Model distinction

The current 001B Python implementation is an **ideal analytical two-coupler MZI** using a declared real reciprocal lossless 2×2 coupler matrix. It is not a geometrical reconstruction of Tian's MMI-based MZI. Retain it as a transparent algebraic reference. Do not relabel its couplers as Tian MMIs or assign fabricated-device dimensions to it.

The physical simulation model must represent the source-reported 1×2 and 2×2 MMI topology, or use independently sourced complex scattering matrices for those components. A generic directional coupler is not an acceptable substitute for a source-faithful Tian geometry.

## EIS assumptions register

No EIS-assumed physical value is authorized at this gate. If a later exploratory model needs an illustrative value, it must be labelled `eis_assumed`, justified, sensitivity-tested, and kept separate from the Tian reproduction model. It cannot be silently promoted to `tian_reported`.

## Source references

- Main article, Methods — Chip fabrication and package; experimental measurements.
- Supporting Information, SI-3 — KKA Chip test (PDF pages 7–9): 450 × 220 nm² waveguide cross-section; TiN heater dimensions; heater sweep and thermal phase-shifter calibration.
- Main article, Methods — identifies CUMEC CSiP-180AL, one 1×2 and one 2×2 MMI, and optical packaging.
- Supporting Information, SI-4 — scalar KKA calibration model and Table S1. Those fitted scalar coefficients are not complex-field material or geometry parameters.

**Gate 1 decision:** PARTIAL / NOT PASSED. Topology and several device facts are known; stack, wavelength, polarization, MMI dimensions and field reference planes remain open. No Tidy3D device job is authorized by this ledger.
