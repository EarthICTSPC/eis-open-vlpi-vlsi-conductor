# EIS-TIDY3D-LEAN-001 — Lean4-to-Tidy3D SOI directional-coupler workflow

**Status:** Draft engineering work package  
**Initial physical object:** two-arm SOI directional coupler  
**Simulation:** 3D FDTD with modal input/output ports  
**Interchange:** Lean4-emitted JSON, schema version 0.1

## Objective

Establish a reproducible, auditable path from an EIS Lean4 specification to a native Tidy3D simulation and back to machine-readable numerical evidence.

This work package deliberately separates:
- **Lean4:** typed parameter contract, unit convention, well-formedness predicates and JSON emission;
- **Python adapter:** strict schema/value validation, explicit nm-to-µm conversion and Tidy3D object construction;
- **Tidy3D:** numerical eigenmode/FDTD solver;
- **EIS acceptance:** provenance, independent numerical checks and Lean acceptance predicates.

Lean4 does not prove the accuracy of an FDTD discretization or physical fidelity of an assumed material stack. Tidy3D output does not become a measurement merely because the solver completed.

## Initial geometry

The illustrative baseline is:
- wavelength center: 1550 nm; sweep: 1500–1600 nm, 31 samples;
- silicon core: 450 nm wide × 220 nm high;
- nominal parallel-arm gap: 200 nm;
- parallel coupling length: 8 µm;
- access/taper length: 4 µm on each side;
- BOX: 2 µm; silicon substrate placeholder: 2 µm;
- oxide cladding and BOX, silicon core and substrate.

The two waveguides are widely separated in access regions and approach the nominal gap only over the declared coupling section. A smoothstep centerline is used for the first layout hypothesis. It is a parameterized geometric approximation, not an optimized low-loss bend.

All values in the initial example are tagged `assumed` and `illustrative_not_foundry_PDK`. The permittivities are approximate teaching inputs. They are not a representation of any specific GF, TSMC, AMF or other foundry process. Replace them only with authorized, versioned process information. Do not publish NDA PDK data or send it to an unapproved cloud environment.

## Input/output convention

The lower arm is excited by a mode source at the left access section. The input mode plane is restricted to that arm so the upper arm is not intentionally excited as a two-waveguide supermode.

Two output mode monitors are placed at the right access section:
- `through`: lower-arm output;
- `cross`: upper-arm output.

The retained evidence must include complex modal amplitudes, not only squared magnitudes. Phase is required for EIS complex transfer and later `κ_A` analysis. Absolute modal power comparisons require explicit confirmation of the Tidy3D mode normalization and monitor conventions.

## Build and run

From the repository root:

```bash
lake exe eis-tidy3d-spec > examples/tidy3d/eis_soi_dc_spec.json
python -m pip install -r requirements-tidy3d.txt
python -m pytest tests/tidy3d -q
```

Open `notebooks/tidy3d/EIS-SOI-Directional-Coupler-FDTD.ipynb`. The notebook builds and plots the simulation without submitting it. Cloud execution is gated by `RUN_CLOUD = False`; changing it to `True` is an explicit user action and may consume FlexCredits.

## Acceptance gates

1. Lean project builds with warnings as errors; `illustrativeSOI_wellFormed` is checked and executable emits valid JSON.
2. Python rejects missing fields, unsupported schema versions, invalid phasor convention and invalid geometry values.
3. Python constructs a native Tidy3D simulation with one mode source, two modal output monitors and explicit waveguide structures.
4. A reviewed Tidy3D run returns complex through/cross modal amplitudes over the wavelength sweep.
5. A separate evidence manifest records Lean spec hash, Python/Tidy3D versions, solver task ID, grid settings, monitor normalization and evidence classification.
6. Independent Python post-processing checks power balance and extracts complex transfer; Lean acceptance is added only after its assumptions and numerical tolerances are reviewed.

## Not claimed

This work package does not yet establish:
- foundry-qualified SOI geometry or material dispersion;
- fabrication tolerance, sidewall angle, roughness or wafer variability;
- heater/EPS/IPS drive response, thermal crosstalk or electrical energy;
- experimentally measured coupling, insertion loss or phase;
- an MZI, KKA activation, `κ_A` device result or 64×64 tile performance.

## Next extension

After this baseline is built and its numerical output reviewed, add:
1. dispersive silicon/oxide material models from an authorized source;
2. mesh convergence and domain/PML convergence checks;
3. bend/taper parameter sweeps and process perturbations;
4. a compact complex scattering/transfer export with provenance;
5. a balanced MZI composition using the EIS detector polarity and normalization contract.
