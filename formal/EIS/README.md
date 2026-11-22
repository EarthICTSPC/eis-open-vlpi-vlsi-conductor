# EIS Lean4 Optical Netlist IR

The Lean4 EIS.Netlist namespace defines the typed, versioned intermediate representation (IR) for EIS optical circuit topology.

## Authority boundary

Lean4 owns component-kind vocabulary, instance and port identities, optical connectivity, top-level optical inputs and outputs, and structural validation.

Python is a lowering and execution layer. It may instantiate the validated IR in PhotonForge/FlexCompute, attach approved PDK cells, generate layouts, and invoke simulations. It must not silently change topology or invent missing physical parameters.

The v0.1 netlist is a **topological IR**, not a geometry-complete mask description. Component parameters are descriptive strings until a separately versioned physical-parameter schema is adopted.

## Component kinds

- laser
- mmi1x2
- mmi2x2
- fanoutTree
- mziCell
- balancedPhotodetector

The MZI macro-cell contract is defined in the EIS-KKA-001B experiment documentation.

## Validation

validateNetlist checks unique instance identifiers; declared connection endpoints; declared top-level boundary ports; no self-connections; no repeated connection endpoint; and no duplicate top-level boundary ports.

This is deliberately a structural check. It does not establish mode compatibility, passivity, reciprocity, power conservation, optical phase correctness, geometric routability, DRC/LVS, or fabrication readiness. Those belong to later contracts and evidence gates.

## Lowering

The canonical JSON representation is the serialization of the Lean Netlist structure using Lean.toJson. The Python adapter validates the version and structure again at the language boundary, maps each ComponentKind to an explicitly registered PhotonForge component, and creates PhotonForge's Python netlist dictionary.

If a required component kind has no registered cell, lowering fails closed. The adapter must not substitute an arbitrary splitter, coupler, or detector.

## Immutability and provenance

Every lowered artifact should record the Lean source commit and compiler version; netlist JSON SHA-256; adapter version and Python package versions; component-registry revision and PDK identity; any eis_assumed physical values; and resulting PhotonForge component and GDS/OASIS hashes.

No optimizer may modify a Lean-authored source netlist in place. Candidate variants must be new netlist values with new IDs and provenance.
