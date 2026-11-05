# EIS-KKA-SOI-001C — Lean-anchored Python scalar reference

This directory implements EIS-KKA-SOI-001 Scalar Field and Interference
Contract v1.0 in
docs/02-architecture/EIS-KKA-SOI-001-SCALAR-CONTRACT-v1.md:

- total_intensity(a, b) = |a + b|²
- cross_term(a, b) = 2 Re(a · conjugate(b))
- propagate(E, T) = T · E

The formal authority is the pinned Lean project:
- `lean-toolchain`: Lean 4.35.0
- `lakefile.lean` and `lake-manifest.json`: Mathlib pinned to commit
  `56a005855ea17e0b0958f73ec801ae140b0a1679`
- `EISKKA/Scalar.lean`: scalar field algebra, interference operator,
  independent complex transfers, polar form and proved identities/bounds
- `EISKKA/ConformanceVectors.lean`: exact rational/integer theorem anchors
  for the JSON/Python conformance cases

Each vector in `vectors.json` names the Lean theorem(s) that prove its exact
mathematical result. The Python test suite verifies that every declared theorem
anchor exists in the formal source and checks the corresponding binary64
implementation result against the vector. This is a reviewed cross-language
conformance mapping, not automatic code generation from Lean.

The Python implementation uses IEEE-754 binary64 complex/float arithmetic.
Its 1e-12 absolute/relative tolerance is a software conformance tolerance,
not a physical device acceptance threshold or uncertainty budget. Lean's
mathematical reals do not represent IEEE-754 NaN or infinity; Python finite
input/output checks remain a runtime boundary.

The signed cross term is not clipped. Field transfer functions are supplied
complex values and are separate from the ideal operator. No Kramers–Kronig
coefficient, SOI TPA, Kerr effect, heater calibration or foundry-specific
response is assumed.

## Reproduce

From the repository root:

    lake build --wfail
    python -m pytest -q experiments/EIS-KKA-SOI-001C

The Lean GitHub Actions workflow also runs the axiom audit. The reviewed
allowlist is `propext`, `Classical.choice`, and `Quot.sound`; no `sorry`
or custom axiom declaration is permitted in the EIS formal source.

A passing Python suite is E2 software evidence. A Lean build and axiom audit
are formal-verification evidence for this scalar contract. Neither is an
optical simulation, physical measurement, detector qualification, full
tensor-attention proof, or energy/CO₂e result.
