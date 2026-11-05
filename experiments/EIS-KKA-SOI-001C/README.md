# EIS-KKA-SOI-001C — scalar Python reference

This directory implements the scalar mathematical convention already written
in docs/02-architecture/EIS-KKA-001-Interference-Operator-and-Physical-Response-Contract.md:

- total_intensity(a, b) = |a + b|²
- cross_term(a, b) = 2 Re(a · conjugate(b))
- propagate(E, T) = T · E

The signed cross term is not clipped. Field transfer functions are supplied as
complex values and are deliberately separate from the ideal operator. No
Kramers–Kronig coefficient, SOI TPA, Kerr effect, or foundry-specific response
is assumed.

## Important formal-status boundary

The repository HEAD inspected for this work contains no .lean source file,
lean-toolchain, or lakefile.lean. The existing EIS-KKA-001 Markdown contract
is explicitly marked “Proposed; not formally verified or physically validated.”
Therefore this Python reference is a software mirror of that written
mathematical contract, not a claim that it was generated from or proved
equivalent to a Lean 4 specification. Issue #58 must first add and compile
the Lean source, pin its toolchain, and cross-reference each definition/theorem.
Only then can #59 be upgraded to Lean-derived conformance.

## Run

From this directory, in a Python 3.12 environment with pytest installed:

    python -m pytest -q

No optical simulator, PDK, foundry data, or cloud service is required. A passing
test suite is E2 software evidence only; it is not E3 simulation or E4
measurement.

## Vectors

vectors.json records the factor-of-two convention, binary64 tolerance, hand
computable cases and transfer examples. Tolerance is currently a software
conformance tolerance, not a physical-device acceptance threshold.
