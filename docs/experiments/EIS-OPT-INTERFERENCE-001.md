# EIS-OPT-INTERFERENCE-001 — ideal interference contract

## Purpose

Define a small, machine-checkable ideal optical-interference contract and connect a typed two-input/two-output interferometer netlist to that contract through an explicit denotational semantics.

## Source context

- TorchLean paper: https://arxiv.org/pdf/2602.22631
- TorchLean repository: https://github.com/lean-dojo/TorchLean

These are background references for Lean-based neural-network specification and verification. This prototype does not depend on TorchLean APIs and does not claim that TorchLean already implements KKA or photonic netlists.

## Frozen ideal convention

Represent each complex-like field by real coordinates `a = (x,y)`, `b = (u,v)`. Define

`I(a,b) = 2 * (x*u + y*v) = 2 Re(a * conjugate(b))`.

The netlist denotes unnormalised outputs `sum = a+b` and `difference = a-b`. Define the balanced observable as half the intensity difference:

`B(a,b) = (|a+b|^2 - |a-b|^2)/2`.

The semantic theorem establishes `B(a,b) = I(a,b)` in the ideal real-coordinate model.

## Formal properties

- Coordinate identity.
- Symmetry of the contract.
- Self-interference equals twice ideal intensity.
- Zero-input properties.
- Typed port direction (`input` versus `output`).
- Netlist denotation satisfies the interference contract.

## Evidence boundary

A successful Lean build establishes only that the stated definitions and theorems are accepted by the configured Lean kernel and dependencies. It does not establish real-device conformance, loss, bandwidth, detector behavior, fabrication feasibility, energy efficiency, equivalence to Softmax, or a KKA Transformer result. No simulation credits or hardware work are authorized by this milestone.

## Current status

Implementation is on the feature branch. Status must remain `not-run` until CI or a reproducible local build completes; after a successful build, classify only the mathematical build/proof evidence as `proved`/`tested` with the run link and commit hash recorded.
