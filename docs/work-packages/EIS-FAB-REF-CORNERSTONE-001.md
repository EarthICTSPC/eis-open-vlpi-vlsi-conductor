# EIS-FAB-REF-CORNERSTONE-001 — CORNERSTONE Si220 Evidence Assessment

**Parent specification:** [EIS-FAB-REQ-001](../EIS-FAB-REQ-001.md)  
**Status:** Read-only source and package audit; no PDK installation or solver run authorized  
**Reference platform:** CORNERSTONE Photonics / University of Southampton; open Si220 SOI PDK ecosystem.  
**Package examined:** `cspdk` wheel 2.1.0 source and metadata, plus public CORNERSTONE/gdsfactory documentation. Exact wheel hash and environment should be added to the machine-readable evidence manifest when available.

## 1. Purpose

CORNERSTONE Si220 is an independent open-SOI reference for EIS. It is useful because it exposes process-oriented technology definitions, layout cells, and wavelength-dependent circuit models. It is not the EIS specification, is not Tian's CSiP-180AL process, and does not establish a KKA-ready or foundry-qualified device set.

The current assessment is based on read-only inspection of the wheel source supplied/extracted in the EIS notebook and public documentation. No package installation, GDS generation, Tidy3D upload, or FDTD execution is represented here.

## 2. What the open PDK provides

The public CORNERSTONE/gdsfactory package documents a family of process variants, including `cspdk.si220` for 220 nm SOI strip/rib waveguides, and provides SAX circuit models. The public documentation identifies the package as an open reference and the platform as an accessible prototyping route. Package releases and dependencies change; pin the exact package version and dependencies for any executable reproduction.

Inspected Si220 source includes:

- technology defaults and process/layer-stack constructors;
- strip and rib cross-section definitions;
- directional-coupler model functions;
- coupling-amplitude lookup tables in NetCDF format;
- straight-waveguide compact models;
- S-bend geometry calculation;
- MZI layout generators and a heater-loop circuit model;
- component and circuit-model registration.

These are valuable engineering assets. They do not by themselves demonstrate a fabricated KKA cell or provide every measured process parameter required by EIS-FAB-REQ-001.

## 3. Inspected technology defaults

The inspected `get_layer_stack` constructor exposes these defaults:

| Layer/model item | Source default | Interpretation and caveat |
|---|---:|---|
| Silicon core thickness | 220 nm | Si220 core datum |
| Silicon slab thickness | 100 nm | Partial-etch slab datum |
| Grating thickness | 150 nm | Grating-layer datum |
| Core z-min | 0 | Source coordinate convention |
| Core sidewall angle | 10° | Confirm angle convention and whether referenced from vertical |
| Core width-to-z | 0.5 | Geometry extrusion parameter; meaning must follow source implementation |
| Heater | TiN, 150 nm, z-min 1.1 µm | Layer-stack constructor default |
| Metal | Al, 220 nm | Layer-stack constructor computes z-min as `zmin_metal + thickness_metal`; inspect semantics before interpreting physical vertical placement |
| BOX / upper cladding / substrate | Not fully specified by this constructor | Must not infer a complete physical stack from this function alone |

The constructor's exposed defaults are not a complete process stack. In particular, the inspected function does not, by itself, establish BOX thickness, upper-cladding thickness/material, substrate treatment, or dispersion data. EIS must inspect all callers and material definitions before building an FDTD model.

The inspected `Tech` defaults include:

| Parameter | Strip/default | Rib/default | Notes |
|---|---:|---:|---|
| General radius | 10 µm | — | Not necessarily the S-bend radius produced by the S-bend helper |
| Minimum radius | 5 µm | — | Design parameter; confirm applicability per cell |
| Cross-section width | 0.45 µm | 0.45 µm | Source defaults |
| C-band width | 0.45 µm | — | Source default |
| O-band width | 0.40 µm | — | Source default |
| Slab width | 5 µm | — | Source default |
| Heater width | 2.5 µm | — | Source default |
| Metal width | 10 µm | — | Source default |
| Coupler gap | 0.27 µm | 0.27 µm | Source default |
| Coupler length | 14.5 µm | 20 µm | Strip/rib differ |
| Coupler dx / dy | 10 / 4 µm | 16 / 3.5 µm | Used by S-bend geometry helper |
| Minimum gap | 0.20 µm | — | Source default; not a guaranteed process tolerance |

These values are **CORNERSTONE source defaults**, not Tian dimensions, not EIS requirements, and not proof of fabricated distributions.

## 4. S-bend geometry audit

The inspected `_sbend_geometry(gap, cross_section, band)` helper selects:

- strip: (dx=10\,\mu m), (dy=4\,\mu m);
- rib: (dx=16\,\mu m), (dy=3.5\,\mu m).

It then calculates:

\[
offset=\frac{dy-gap-width_{band}}{2}
\]

\[
\theta=2\arctan\left(\frac{offset}{dx}\right),
\qquad
R=\frac{dx}{2\sin\theta}.
\]

For the inspected strip C-band defaults (gap=0.27\,\mu m), (width=0.45\,\mu m), (dx=10\,\mu m), and (dy=4\,\mu m):

- offset = 1.64 µm;
- θ ≈ 0.3251 rad;
- helper-derived equivalent radius ≈ 15.65 µm.

This calculated radius is not the same as the separate `TECH.radius_strip=10` default. The geometry helper and the general radius field must not be conflated.

The directional-coupler model computes an S-bend path-length term:

\[
L_{sbend}=2R\arccos\left(1-\frac{offset}{2R}\right)
\]

and uses a straight-waveguide arm model with length:

\[
L_{arm}=\frac{L_{coupler}}{2}+L_{sbend}.
\]

The source then multiplies the coupling-region S coefficients by the arm transfer functions. This is a compact-model construction, not a full 3D electromagnetic solution.

## 5. Straight-waveguide phase and loss model

The inspected source calls a straight-waveguide compact model with these inputs:

| Cross-section | Loss | Reference wavelength | Effective index | Group index |
|---|---:|---:|---:|---:|
| Strip | 3 dB/cm | 1.55 µm | 2.38 | 4.30 |
| Rib | 3 dB/cm | 1.55 µm | 2.54 | 3.87 |

The source passes `wl`, `length`, `loss_dB_cm`, `wl0`, `neff`, and `ng` to `sm.straight`. These are compact-model parameters. Before EIS reuses them, inspect and pin the exact `sm.straight` implementation and dependency version so the phase convention, wavelength dependence, and amplitude attenuation formula are not guessed.

For a conventional uniform waveguide, the expected physical structure is propagation phase plus attenuation, often represented as a complex field transfer (t(L,\lambda)=a(L,\lambda)e^{i\beta(\lambda)L}). That generic form is explanatory only; EIS must derive the exact convention and formula from the pinned implementation rather than treating this sentence as a source-verified equation.

The stated 3 dB/cm values are model defaults, not evidence that every fabricated CORNERSTONE die achieves exactly that loss.

## 6. Directional-coupler model and lookup tables

The inspected Si220 source includes `directional_coupler_strip.nc` and `directional_coupler_rib.nc` lookup tables.

Both tables have dimensions:

- wavelength: 21 points;
- gap: 15 points;
- radius: 5 points;
- coupling length: 25 points;
- vertical offset: 5 points;
- total: 196,875 scalar samples per table.

Inspected coordinate ranges:

| Coordinate | Range |
|---|---:|
| Wavelength | 1.50–1.60 µm |
| Gap | 0.05–0.75 µm |
| Radius | 5–85 µm |
| Coupling length (`length_x`) | 0–96 µm |
| Vertical offset (`v_offset`) | 5–85 µm |

The NetCDF variables are real float64 coupling amplitudes, not complex measured field samples. The inspected strip table has a reported range approximately 0.00014415 to 0.9999999983; the rib table approximately 0.00003966 to 0.9999999990. Their source descriptions identify coupling amplitudes derived from coupled-mode theory / supermode calculations and explicitly state that they are **not validated by the foundry**.

The SAX model interpolates κ and constructs a reciprocal complex coupling model using:

\[
\tau=\sqrt{1-\kappa^2}
\]

with through coefficient τ and cross coefficient (i\kappa), followed by propagation phase/loss in the full directional-coupler model. Therefore the correct description is:

**A wavelength-dependent complex S-parameter surrogate derived from a real-valued coupling-amplitude lookup table.**

It is not a measured complex-field table.

Important model-audit items:

1. Confirm the exact port ordering and phase convention.
2. Test reciprocity and passivity across the entire in-domain table and interpolated points.
3. Verify interpolation reproduces table nodes and does not overshoot κ outside [0,1], which would make the square root invalid.
4. Test exact boundary and out-of-domain behavior.
5. Compare strip and rib table surfaces.
6. Inspect whether the `width` function argument actually influences interpolation. In the inspected function body it appears in the signature/documentation but is not passed to the table interpolator; record this as a source-audit issue, not an assumed width dependency.
7. Keep coupling-region-only `directional_coupler_no_phase` distinct from the full model that includes S-bend and straight-arm phase/loss.

The coordinate ranges are model-table coverage, not fabrication tolerances or process-corner distributions.

## 7. MZI and active-device coverage

The inspected package includes MZI layout generators and an MZI heater-loop circuit model. The layout cell constructs a splitter, combiner, bends, and waveguides. The heater-loop model uses a compact heater-phase relationship and composes the arm and coupler models.

This is useful as an MZI reference, but it does not establish a Tian-equivalent KKA cell. In particular, the inspected package does not yet establish:

- Tian's exact SI-1 dual-MZI I/W topology and detector observable;
- a KKA-specific modulator–interferometer cascade with frozen encoding and reference planes;
- calibrated complex amplitude–phase transfer for the relevant device and control range;
- dense heater-array thermal interaction and calibration behavior;
- integrated detector response and BPD calibration;
- measured cascade accuracy under KKA workloads.

Do not interpret the existence of an MZI or heater-loop cell as proof that these system-level capabilities are present.

## 8. PhotonForge integration status

Current PhotonForge documentation lists SiEPIC EBeam as an installable PDK and lists CORNERSTONE as a platform requiring contact for integration. The public CORNERSTONE `cspdk` package is a GDSFactory/SAX ecosystem package with a substantial dependency stack; it must not be assumed to register a native PhotonForge technology.

EIS's inspected environment has PhotonForge 1.5.1 and Tidy3D available, while `cspdk` and GDSFactory were not installed at the time of inventory. The cspdk 2.1.0 wheel was inspected without installation. No compatibility claim should be made until a separately approved integration test is run in an isolated environment.

## 9. Requirement mapping

| EIS-FAB-REQ-001 IDs | CORNERSTONE evidence | Assessment |
|---|---|---|
| FAB-001 | Layer-stack constructor and technology defaults | PARTIAL — BOX/cladding/substrate and full process-corner evidence incomplete |
| FAB-002 | Strip/rib cross-sections and C/O-band variants | PARTIAL — verify mode/cross-section data and exact package revision |
| FAB-003 | Straight and bend compact-model parameters | MODELLED / SOURCE-REPORTED; not equivalent to EIS measured loss |
| FAB-004 | Wavelength-dependent coupler κ tables and SAX S model | MODELLED; source says not foundry-validated |
| FAB-005 | MZI layout and circuit model | PARTIAL — KKA-specific complex-field acceptance not established |
| FAB-006 | No identified KKA-specific cell or source-matched cascade | NOT SUPPORTED by inspected evidence |
| FAB-007, FAB-008 | Heater-loop model and heater-related layout | PARTIAL — calibrated complex field and control response not established |
| FAB-009 | No inspected dense thermal interaction matrix | NOT ASSESSED / gap |
| FAB-010 | Detector model/cell coverage needs further audit | NOT ASSESSED |
| FAB-011, FAB-016 | Optical I/O and test structures need source-specific audit | PARTIAL / OPEN |
| FAB-017 | SAX compact models, including couplers and waveguides | PARTIAL — model provenance and foundry validation vary by component |
| FAB-018 | Models and layout can support simulation workflows | PARTIAL — no EIS-approved mesh/resource gate evidence |
| FAB-019 | GDSFactory/SAX backend is available as an independent route | PARTIAL — integration and common IR/acceptance tests not done |
| FAB-020 | Public source and model provenance available | PARTIAL — EIS evidence manifest and hashes still required |

## 10. Required next audits

1. Pin the exact wheel hash, package version, source revision, and dependencies.
2. Inspect all callers of `get_layer_stack`, the material catalogue, and the complete vertical stack definition.
3. Inspect the exact `sm.straight` source and derive its complex transfer equation and sign convention.
4. Run table integrity and interpolation tests in an isolated, approved environment.
5. Verify full directional-coupler S matrices for reciprocity, passivity, port mapping, and out-of-domain behavior.
6. Audit MZI, heater, detector, grating, and test-structure models separately.
7. Request clarification from CORNERSTONE maintainers on model provenance, foundry-validation scope, and any missing stack definitions.
8. Only then prepare a reduced, local FDTD geometry and mesh preflight. Any cloud cost-estimation upload or solver run requires separate explicit approval and a current credit/cost check.

## 11. Community questions and contribution opportunities

- Can CORNERSTONE maintainers clarify the full BOX/cladding/substrate stack and the z-coordinate convention in the layer-stack constructor?
- Can they confirm the exact straight-waveguide phase/loss equations and model conventions for the pinned dependency version?
- Can they clarify why the coupler `width` parameter is present if it is not used in the inspected lookup path?
- Are measured complex S-parameters available for the directional couplers, MMIs, MZIs, and bends represented by compact models?
- What validation scope applies to each model, and which models are derived from measured foundry data versus coupled-mode/supermode simulations?
- Are thermal-crosstalk matrices, heater efficiency data, and detector models available?
- Would maintainers welcome an open KKA-oriented test coupon or a shared complex-field benchmark?

**EIS position:** CORNERSTONE is a valuable open computational reference. Its model gaps are useful collaboration opportunities. EIS will not relabel an analytical or semi-analytical compact model as foundry-measured truth.
