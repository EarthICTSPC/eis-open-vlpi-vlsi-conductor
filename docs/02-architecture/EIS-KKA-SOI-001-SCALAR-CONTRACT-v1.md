# EIS-KKA-SOI-001 — Scalar Field and Interference Contract v1.0

**Status:** Scalar mathematical convention frozen; Lean 4 proof and axiom audit passed on PR head `7aa5645809478dd45639ac24415dad198e951531`  
**Applies to:** Scalar coherent-field primitive only  
**Does not define:** Full tensor KKA attention, a material response, a foundry macro, or a physical detector

## 1. Types and conventions

Let a,b ∈ ℂ be finite, dimensionless complex field envelopes under one declared normalization and coherent reference convention. The conjugate is denoted by an overbar. The real part is Re(·). The reference amplitude normalization, phase origin, wavelength, polarization, mode, and physical reference planes must be supplied by any physical mapping; they are not inferred by this scalar contract.

## 2. Normative observables

The ideal coherent total intensity is

`I_total(a,b) := |a+b|²`

The signed balanced cross-term convention is

`I_cross(a,b) := 2 Re(a · conjugate(b))`

The factor of two is normative. Do not silently substitute Re(a·conjugate(b)) or total intensity for the signed cross term. The cross term is signed and MUST NOT be clipped to nonnegative values.

The identity connecting the two observables is

`I_total(a,b) = |a|² + |b|² + I_cross(a,b)`

## 3. Field-transfer boundary

Each operand path may have an independently supplied complex field transfer:

`a_out := T_a · a`
`b_out := T_b · b`

The resulting observable is

`I_cross_out := I_cross(a_out,b_out)`

T_a and T_b are input parameters with provenance. This contract does not prescribe their physical origin, functional dependence, wavelength/temperature range, or calibration. In particular, it does not assume a universal pointwise Kramers–Kronig coefficient, SOI two-photon absorption, Kerr nonlinearity, or any specific foundry mechanism.

## 4. Required mathematical properties

For finite complex a,b:

1. Symmetry: I_cross(a,b) = I_cross(b,a).
2. Conjugation invariance: I_cross(conjugate(a),conjugate(b)) = I_cross(a,b).
3. Bound: |I_cross(a,b)| ≤ 2|a||b|.
4. Zero operand: I_cross(0,b) = I_cross(a,0) = 0.
5. Phase form: for a=A exp(iφ_a), b=B exp(iφ_b), I_cross = 2AB cos(φ_a−φ_b).
6. Constructive, destructive and quadrature limits: relative phases 0, π and ±π/2 yield +2AB, −2AB and 0 respectively for nonnegative A,B.

These are mathematical properties of the ideal scalar operator, not claims about a physical implementation.

## 5. Software conformance

The reference implementation uses Python binary64 complex/float arithmetic. The committed deterministic vectors specify absolute and relative software comparison tolerances of 1e−12 for the listed hand-computable cases. This tolerance is for implementation conformance only; it is not a physical device acceptance threshold, uncertainty budget, or downstream task threshold.

Inputs and supplied transfer coefficients must have finite real and imaginary components. Overflow/non-finite outputs are rejected. Tests must preserve signed outputs and include unequal amplitudes, arbitrary phase, zero fields, quadrature, loss/phase transfer and invalid non-finite inputs.

## 6. Explicit non-claims and deferred contracts

This scalar contract does not prove:
- that a particular device realizes T_a or T_b;
- that T is Kramers–Kronig-derived, TPA-enabled, Kerr-enabled, or temperature-controlled;
- that an optical detector realizes ideal balanced subtraction;
- that KKA equals standard softmax attention for arbitrary inputs or tasks;
- any tensor axes, reductions, scaling, head composition, encoding, training semantics, or finite-channel estimator;
- accuracy, latency, energy, thermal load, lifecycle impact, or CO₂e benefit.

Full KKA attention requires a separate tensor-level contract. Device response requires characterized or explicitly assumed parameters and an independent evidence record.

## 7. Formal status

This document freezes the scalar mathematical convention as EIS-KKA-SOI-001 v1.0.

**Formal evidence recorded on PR branch head** `7aa5645809478dd45639ac24415dad198e951531`:
- Lean 4.35.0 stable toolchain, pinned in `lean-toolchain`.
- Mathlib pinned to commit `56a005855ea17e0b0958f73ec801ae140b0a1679` in `lakefile.lean` and `lake-manifest.json`.
- `lake build --wfail` passed.
- Axiom audit examined 44 declarations under `EISKKA`; all were within the reviewed allowlist `propext`, `Classical.choice`, `Quot.sound`.
- Formal source check found no `sorry` or custom axiom declarations.
- Proved results include the intensity expansion, signed cross-term symmetry, conjugation invariance, zero-operand cases, squared and absolute Cauchy–Schwarz bounds, equivalence to twice the real part of the complex product, polar phase-difference form, and transfer coordinate semantics.
- Exact integer/rational conformance examples are proved in `EISKKA/ConformanceVectors.lean`.

This formal verification applies to the scalar mathematical model only. It does not establish physical transfer curves, device behavior, KKA full attention equivalence, detector realization, energy, latency, or environmental performance. The Python implementation remains a separate binary64 executable reference; the JSON vectors cross-reference Lean theorem names and the Python suite checks those anchors exist and checks the numerical results. This is a reviewed cross-language conformance mapping, not automatic code generation from Lean.

The evidence is on the draft PR branch; it becomes the repository's merged formal baseline only when the PR is reviewed and merged.
