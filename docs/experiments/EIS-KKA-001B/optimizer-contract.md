# EIS-KKA-001B — MZI Design-Space Optimization Contract

**Status:** optimizer contract; not yet connected to a FlexCompute optimization run.

## Governing principle

Earth ICT, SPC specifies the functional contract, acceptance constraints, process constraints and objective measures. The optimization engine searches the admissible design space and returns candidate geometries with evidence. It must not invent missing process limits, silently turn unknowns into fixed values, or change the acceptance contract to make a candidate pass.

The target is **human-free geometry selection inside a human-approved, machine-checkable design space**—not human-free engineering responsibility. Humans establish and approve requirements, foundry/PDK limits, and any exploratory bounds not supplied by the process design kit. The optimizer performs the search, evaluates candidates and exposes trade-offs.

## 1. Fixed source facts versus free design variables

The following source-reported values are carried as fixed source facts in the exploratory model, not optimizer-selected values:

- waveguide cross-section: 450 nm × 220 nm;
- TiN heater: 200 µm × 2 µm × 120 nm;
- TiN sheet resistance: 12 Ω/sq.

These values are reported by Tian et al. (2025). Their use does not establish support by a different foundry process or PDK. Process compatibility must be checked separately.

Candidate geometry variables include, where the selected PDK exposes or permits them:

- MMI body length and width;
- access taper length and width;
- MMI port pitch and waveguide gap;
- interferometer arm lengths and differential path length;
- bend radius and routing geometry;
- heater-to-waveguide offset and heater routing geometry.

This is a candidate variable inventory, not a declaration that all parameters are independently variable or that numeric bounds are known.

## 2. Search-domain rule

Every free variable must have a name and physical unit; finite admissible lower and upper bounds (or an explicitly enumerated legal set); a source for those bounds (PDK rule, foundry design manual, measured process capability, or EIS-approved exploratory bound); a source/evidence identifier and revision; and a declared status (free or fixed).

No numerical bounds are supplied by this contract. The current MZI geometry therefore remains **blocked from physical optimization** until the target PDK and applicable rules are identified and the design-space manifest is populated. Do not substitute arbitrary “reasonable” dimensions.

A bound labelled eisApprovedBound is a deliberate engineering assumption, not a foundry guarantee. It must be visibly identified in every result and must not be promoted to a PDK fact.

## 3. Optimization objectives

Do not collapse the design into a single undocumented score. Return a Pareto set over applicable objectives:

- optical insertion loss;
- output balance / extinction or interference contrast;
- optical bandwidth and wavelength sensitivity;
- footprint;
- phase-shifter electrical power and tuning range;
- thermal crosstalk / temperature sensitivity;
- robustness to fabrication variation and parameter uncertainty.

The exact objective definitions, reference planes, operating conditions and acceptance thresholds must be frozen in the run manifest before candidate evaluation. Objectives that cannot yet be measured or simulated remain not_evaluated; they must not be assigned invented values.

## 4. Hard constraints versus objectives

Hard constraints are pass/fail gates, not optimization preferences. Examples include PDK DRC and permitted layer/spacing rules; connectivity and port-order contract; optical response requirements at defined reference planes; heater/electrical limits; thermal and reliability limits; and preservation of the 001B analytical complex-field reference within a declared comparison tolerance.

The 001A SI-4 calibration reference remains read-only. Optimization may consume it as a separate reference artifact but must not write back to its equation, coefficients or baseline.

## 5. Search and evidence loop

1. Lean4 owns the typed component/netlist and acceptance contract.
2. Python validates the design-space manifest and lowers a candidate into the pinned PhotonForge/PDK implementation.
3. PhotonForge creates candidate layout geometry; DRC and connectivity checks reject invalid candidates before expensive simulation.
4. FlexCompute/Tidy3D evaluates only candidates that pass inexpensive gates.
5. The optimizer updates its search using simulation results and returns a Pareto set, not merely one unexplained “best” point.
6. EIS retains the input manifest, candidate parameters, tool/PDK versions, seeds, constraints, raw results, derived metrics and rejection reasons.

The optimizer may choose geometry values only within the declared domain. It may not alter source facts, acceptance thresholds, evidence labels or the domain itself.

## 6. Required candidate record

Each candidate result must identify immutable source netlist and design-space manifest hashes; candidate parameter values and units; bounds and provenance for each free variable; PhotonForge, PDK and simulation versions; DRC/connectivity status; simulation settings, reference planes and run identifiers; objective values with units and evidence class (simulated, derived, or measured); hard-constraint results and failure reasons; uncertainty/sensitivity information; and Pareto-dominance status.

A candidate without this record is not an accepted optimization result.

## 7. Current gate

**Current state: BLOCKED — no target PDK, no approved numeric search bounds, no PhotonForge component implementation, and no FlexCompute optimization adapter have been validated.**

The next executable step is to bind this contract to the selected foundry PDK and generate the first admissible MZI design-space manifest. Only then should FlexCompute begin searching. This keeps humans out of manual dimension-picking while preventing the optimizer from exploring physically invalid or unsupported geometries.
