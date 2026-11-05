# EIS KKA Lean specification

This directory's project root is the repository root. The Lean toolchain is
pinned in `lean-toolchain`; Mathlib is pinned in `lakefile.lean` to the
matching release tag.

## Authority and boundaries

- `EISKKA/Scalar.lean` is the formal source for the scalar coherent-field
  operator and its proved algebraic properties.
- `EISKKA/ConformanceVectors.lean` defines exact examples used as anchors for
  the Python conformance vectors.
- `experiments/EIS-KKA-SOI-001C/` is the executable binary64 reference.
- `pdk/cornerstone-si220/manifest.yaml` identifies the implementation
  candidate. The PDK does not define the mathematics.

Lean's `Real` values are mathematical real numbers. They do not represent
IEEE-754 NaN or infinity. Python's finite-value checks are an implementation
boundary, not an additional theorem about mathematical reals.

This scalar specification does not prove KKA attention equivalence, a device
transfer curve, SOI TPA/Kerr behavior, a detector implementation, energy,
latency, or physical conformity.

## Reproduce

Install elan/Lake for the exact version in `lean-toolchain`, then run:

    lake update
    lake exe cache get
    lake build

The CI workflow runs the same build. Review the emitted `#print axioms`
reports for every exported theorem. No `sorry`, custom axiom, or opaque
unreviewed theorem is permitted in the trusted specification.
