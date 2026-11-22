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

## Exploratory example

The current 10-output Tian-inspired example is stored at `schema/examples/eis_tian_ptc_10_output_exploratory.json`. It contains 11 MZI macro-cell instances (10 A-side plus one shared B-side), 33 phase-shifter functions, ten output-combiner MMIs and ten BPDs. Source-derived values and unknowns are individually labelled in each parameter record. The A-side fanout and B-side broadcast remain logical-only abstractions; they are not physical splitter trees yet.

The Python bridge is `experiments/eis-kka-001b-mzi-field/eis_netlist_to_photonforge.py`. It requires a caller-supplied component registry and fails closed if a component kind has no approved PhotonForge cell. It does not currently export top-level boundary ports because that mapping must be pinned to the selected PhotonForge API version and tested explicitly.

## Lean example and current validation status

The 10-output topology is also constructed in `formal/EIS/Examples/TianExploratory.lean`. It evaluates the structural validator and prints the serialized Lean JSON representation. The repository does not yet contain a pinned Lean toolchain or Lake project configuration, and a Lean compiler was not available in the current execution environment. Therefore the Lean source has **not yet been compiled** and the checked-in JSON example has not yet been confirmed byte-for-byte against Lean's emitted JSON.

The JSON example was independently checked for declared endpoints, duplicate connection-port use, 11 MZI instances, 33 phase-shifter functions, ten BPD instances, and valid evidence-class labels.

The Python adapter and its pytest tests are authored but have not yet been executed in this environment. PhotonForge is not installed here. No PhotonForge component was built, no layout was exported, and no Tidy3D job was submitted.
