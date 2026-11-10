# FlexCompute handoff — EIS-PTC-MZI-001 v0.1

## Purpose

This package defines a technology-independent three-heater MZI model contract and a transparent first-order non-ideal reference. It is suitable for review and model-extension planning in PhotonForge/Tidy3D. It is not a foundry layout or a calibrated device model.

## What FlexCompute should review

1. Verify the ideal MZI equations against Tian et al. (2025), SI-1, with particular attention to signed amplitude and phase conventions.
2. Review the parameterized loss/coupler/heater abstraction and identify which parameters can be mapped to PhotonForge primitives or Tidy3D simulations.
3. Propose a staged calibration plan:
   - passive waveguide propagation and loss;
   - 1×2/2×2 coupler split ratio, phase and excess loss;
   - each heater's R(T), P-to-phase response and dynamic response;
   - 3×3 thermal coupling matrix;
   - full MZI transfer over wavelength, temperature and drive.
4. Identify the smallest useful simulation set and distinguish analytical, compact-model, EM/FDTD and measured inputs.
5. Recommend a data format for exporting simulated/measured calibration curves back into the evidence manifest.

## Required output from review

- A model audit with equations, assumptions, and missing parameters.
- A mapping of each model term to an available PhotonForge/Tidy3D object or a documented unsupported gap.
- A simulation plan with mesh/domain/convergence requirements only where needed.
- A parameter table that labels every input SOURCE_REPORTED, SIMULATED, FITTED, MEASURED, ASSUMED or UNKNOWN.
- No foundry-specific layout, NDA material, or proprietary PDK data in the public EIS repository.

## Current boundary

The package has no selected process, layer map, mask geometry, DRC/LVS deck, or physical calibration. Do not infer any of these from the logical port map. The port map is a functional interface; it is not a claim that the complementary output geometry is implemented.

## Suggested staged work

A. Review the model and test cases without launching simulations.
B. Identify parameters that can be characterized analytically or from public source data.
C. Propose minimal simulations to fill only the gaps that affect acceptance.
D. Return simulation outputs with solver version, mesh, boundary conditions, convergence, raw data, and hashes.
