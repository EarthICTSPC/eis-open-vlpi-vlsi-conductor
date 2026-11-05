# EIS-KKA-SOI-001C — scalar Python reference

This directory implements EIS-KKA-SOI-001 Scalar Field and Interference
Contract v1.0 in
docs/02-architecture/EIS-KKA-SOI-001-SCALAR-CONTRACT-v1.md:

- total_intensity(a, b) = |a + b|²
- cross_term(a, b) = 2 Re(a · conjugate(b))
- propagate(E, T) = T · E

The signed cross term is not clipped. Field transfer functions are supplied as
complex values and are deliberately separate from the ideal operator. No
Kramers–Kronig coefficient, SOI TPA, Kerr effect, or foundry-specific response
is assumed.

## Important formal-status boundary

The repository HEAD inspected for this work contains no .lean source file,
lean-toolchain, or lakefile.lean. Contract v1.0 freezes the written scalar
mathematics but is not formally verified. Therefore this Python reference is a
software mirror of the written contract, not a claim that it was generated
from or proved equivalent to a Lean 4 specification. Issue #58 must add and
compile the Lean source, pin its toolchain, and cross-reference each
definition/theorem. Only then can #59 be upgraded to Lean-derived conformance.

## Run

From this directory, in a Python 3.12 environment with pytest installed:

    python -m pytest -q

No optical simulator, PDK, foundry data, or cloud service is required. A passing
test suite is E2 software evidence only; it is not E3 simulation or E4
measurement.

## Vectors

vectors.json records the factor-of-two convention, binary64 tolerance,
hand-computable cases and transfer examples. Tolerance is for software
conformance only, not physical-device acceptance.
