# EIS VLPI — Lean 4 formalization

This directory is the home for EIS's Lean 4 formal definitions and proofs. Lean belongs in a dedicated `formal/lean4/` project rather than inside the Python harness: the two layers have different responsibilities and should be tested independently, then connected by explicit fixtures and equivalence tests.

## Scope

- Define semantic and physical representation distinctions.
- State machine-checkable contracts and composition predicates.
- Prove properties of the formal model.
- Keep simulation, measurement, and fabrication claims as separate evidence.

A Lean theorem proves its stated mathematical proposition under its definitions and assumptions. It does not, by itself, establish that a fabricated device conforms to a physical contract.

## Run locally

From this directory, with Lean 4 / Lake installed:

```sh
lake build
```

The initial foundation uses integer picoseconds and an explicit serial-additive latency predicate. The EIS-CRC-BUDGET-001 example sums to 228 ps against a 200 ps limit and is proved rejected. This is a formal arithmetic baseline, not a physical latency measurement and not yet a Python-orchestrator equivalence test.

## Project structure

- `lean-toolchain` pins the Lean version.
- `lakefile.toml` defines the Lake project.
- `EISVLPI.lean` is the initial import module for shared formal definitions.

As the model grows, split stable concepts into modules (for example `Types`, `Contracts`, `Composition`, and `Budget`) and import them from the project entry point. Do not encode proprietary PDK data or credentials in this public repository.
