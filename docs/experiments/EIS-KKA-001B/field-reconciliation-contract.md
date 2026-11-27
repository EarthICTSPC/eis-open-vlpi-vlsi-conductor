# EIS-KKA-001B — Complex-Field Reconciliation Contract

**Status:** Protocol defined; no EM result available  
**Comparison:** Tidy3D optical outputs versus the analytical 001B reference  
**Frozen dependency:** EIS-TIAN-KKA-LIFT-001A is immutable and read-only.

## Purpose

Define how independent electromagnetic results will be compared with the analytical complex-field model without treating different device topologies, port conventions or normalizations as if they were equivalent.

## Model identities

- **Analytical reference:** ideal reciprocal lossless directional-coupler MZI as implemented in 001B. Its coupler matrix and port phase convention are explicit.
- **Physical model:** source-faithful SOI waveguide and MMI-based MZI where Tian geometry is available, or a separately labelled EIS exploratory geometry if not.
- **Calibration reference:** 001A SI-4 Eq. (S13) and Table S1. It is a fitted scalar observable and is not a complex S-parameter target.

These three model layers must never be conflated.

## Preconditions for comparison

Before computing an error metric, align and document:

1. Physical topology and component identity.
2. Port ordering and propagation direction.
3. Input mode, polarization, wavelength and normalization.
4. Reference-plane coordinates and de-embedding.
5. Complex phase convention and time-harmonic sign convention.
6. Field amplitude units and power normalization.
7. Material loss and radiation-loss accounting.
8. Temperature and any included thermal state.

If these are not aligned, mark the comparison **NOT COMPARABLE** and explain why. Do not remove a phase offset or renormalize amplitudes merely to improve agreement unless that operation is explicitly defined as a separate diagnostic.

## Required comparisons

For matched ports and reference planes, preserve the complex quantities and report:

- Complex field difference: `E_sim - E_analytic`.
- Relative complex-field error with a declared denominator and zero-denominator handling.
- Magnitude error and wrapped phase error separately.
- Output-port powers and total transmitted/reflected/absorbed/radiated power where available.
- Balanced output difference using the same sign and port convention.
- Power-balance residual.
- Sensitivity to mesh refinement and wavelength.
- Uncertainty contributions from geometry, material data, mesh and reference-plane placement.

A scalar power-only match is not sufficient to validate complex-field agreement.

## Interpretation rules

- Agreement between the ideal analytic model and a simulated ideal two-coupler geometry validates the implementation under that mathematical convention; it does not validate Tian's fabricated MMI geometry.
- Agreement between an MMI-based EM model and measured complex S-parameters would be stronger device evidence, subject to provenance and uncertainty.
- Agreement between simulated powers and Tian SI-4 fitted scalar curves is not by itself a validation of the complex-field model.
- Differences caused by MMI topology, loss, phase convention or reference-plane mismatch must be classified before any parameter adjustment.
- No optimization, fitting or calibration update is part of this protocol.

## Gate 3 acceptance

Gate 3 passes only when:
- all comparison preconditions are met;
- complex outputs and port conventions are preserved;
- mesh and parameter sensitivity are quantified;
- discrepancy and uncertainty are reported separately;
- every conclusion is labelled as analytical, simulated, measured or inferred;
- no changes are made to the 001A source-fitted equation, coefficients or calibration baseline.

## KKA amplitude–phase adapter boundary

The adapter that maps a physical drive/control state to the complex optical field is a separate component and separate evidence package.

It must not infer a voltage-to-complex-field relationship from the SI-4 scalar fit. SI-4 Eq. (S13) remains a source-fitted scalar relation for its stated measured observable. A future adapter needs independent evidence for amplitude, phase, wavelength, polarization, operating range, reference plane, thermal state, repeatability and uncertainty.

Until that evidence exists, 001B accepts complex input fields as explicit caller-supplied values. It does not manufacture them from heater voltages.
