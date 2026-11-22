# EIS-KKA-001B — Tidy3D Optical Evidence Gate

**Status:** Planned; no Tidy3D solver job submitted  
**Prerequisite:** Gate 1 geometry/source ledger must be completed for the selected model scope.  
**Optimizer:** prohibited.  
**001A:** read-only; no edits, refits, coefficient imports or write-back.

## Objective

Generate independently reviewable optical evidence for the SOI MZI component chain, with the source-reported Tian topology represented accurately where source geometry is available:

1. SOI waveguide supported-mode calculation.
2. 1×2 MMI component model.
3. 2×2 MMI component model.
4. MZI assembled from those component responses, with explicit port/reference-plane conventions.

The current 001B ideal directional-coupler model remains an analytical comparison reference. It is not the physical geometry template for Tian's MMI splitters.

## Entry criteria

Do not launch a cloud solver until each item below is either sourced or explicitly excluded from the scope:

- Device layer, BOX, substrate and cladding stack.
- Waveguide cross-section including etch/slab profile and sidewall assumptions.
- Material dispersion and loss over the chosen wavelength range and at the selected temperature.
- Exact wavelength or explicitly bounded wavelength sweep.
- Polarization / mode family to solve.
- MMI body dimensions, access waveguides, tapers, port spacing and layout.
- Arm lengths, bends and MZI connectivity for full-MZI stage.
- Simulation domain, boundary conditions, port planes and de-embedding convention.
- Mesh convergence plan and monitor placement.
- Cloud job estimate and user-approved compute budget.

If any source-critical geometry remains unknown, either stop or define a separately named EIS exploratory geometry with every assumption labelled `eis_assumed`. Do not call that run a Tian reproduction.

## Solver sequence

### A. Supported modes

For the documented SOI waveguide cross-section:

- Solve the selected wavelength and polarization modes.
- Record effective index, group index if available, mode profiles, confinement and loss assumptions.
- Confirm mode identity and normalization convention.
- Check mesh refinement stability before using the mode as an input to component simulation.

### B. MMI component response

For each MMI separately:

- Simulate the 1×2 and 2×2 MMI geometry.
- Extract complex modal amplitudes at all declared ports, not only output powers.
- Record the port ordering, phase reference, normalization, propagation direction and reference-plane coordinates.
- Verify power balance against modeled material and radiation loss.
- Repeat with mesh refinement and, where material data supports it, wavelength variation.

### C. MZI assembly

- Assemble the two MMI responses and arm propagation sections using explicit complex scattering/transfer conventions.
- Compare assembled output fields and powers against the 001B analytical model only after matching topology, port order, reference planes, input normalization and phase convention.
- Preserve the MMI-derived model as a separate physical model. Do not overwrite the ideal directional-coupler reference.

## Cloud-cost preflight

Before any cloud submission, record:

- Tidy3D package/API version and solver type.
- Simulation domain dimensions and grid/mesh strategy.
- Estimated grid cells / memory footprint and simulation duration.
- Number of parameter points and jobs.
- Estimated FlexCompute credits or monetary cost using the current account estimate.
- Planned stopping criteria and a maximum budget.
- Whether a local/non-cloud validation can reject an invalid setup first.

No cloud job should be submitted merely to discover whether an undocumented geometry runs. Start with the smallest justified supported-mode calculation, then one MMI, and only proceed when each stage passes.

## Evidence record required for each run

Each run must preserve:

- Immutable source/configuration file and SHA-256.
- Tidy3D version and solver settings.
- Material source and provenance.
- Geometry parameter ledger with evidence labels.
- Mesh-convergence evidence.
- Port mode definitions and reference planes.
- Complex S-parameters / complex field arrays and normalization.
- Power conservation / loss accounting.
- Cloud job ID, run date, credits/cost and logs.
- Explicit status: `simulated`, not measured or fabricated.

## Gate 2 acceptance

Gate 2 passes only when the mode solve and the required MMI/MZI simulations complete with documented convergence, material and geometry provenance, reference planes, complex-field outputs, and cost records.

A notebook hosted in a Tidy3D workspace that only executes NumPy/Matplotlib is not a Tidy3D electromagnetic simulation. A successful import or API connectivity test is also not optical evidence.

## Current decision

**NOT READY / NO JOB SUBMITTED.** The source review establishes the MMI topology, but the physical stack, MMI dimensions, exact wavelength, polarization and reference planes are not yet sufficiently specified for a source-faithful electromagnetic run.
