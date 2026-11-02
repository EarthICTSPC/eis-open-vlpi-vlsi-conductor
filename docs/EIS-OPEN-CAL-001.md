# EIS-OPEN-CAL-001 — Open SOI MZI Characterization and Calibration

**Status:** specified; implementation and physical evidence pending  
**Repository:** `EarthICTSPC/eis-open-vlpi-vlsi-conductor`  
**Scope:** open SOI MZI characterization, calibration, layout-enabling infrastructure, and evidence discipline.

## 1. Engineering question

Given an explicit device-computation contract, can an open, reproducible calibration procedure reduce the measurements needed to qualify an unseen Mach–Zehnder interferometer (MZI) while maintaining the required acceptance reliability?

The experiment compares conventional individual-device calibration with a learned population-model initialization followed by targeted device-specific measurements. The held-out evaluation must be defined before collecting or examining test-device calibration data.

## 2. Non-claims

This specification does not claim that:
- a particular SiEPIC PDK revision or fabrication run has already been pinned and validated;
- a generated layout is DRC-clean, LVS-clean, fabrication-qualified, or physically measured;
- the calibration model transfers across dies, wafers, fabrication runs, or foundries;
- Lean4 proves that a fabricated device physically satisfies its contract;
- a custom OASIS serializer is compliant with SEMI P39.

Simulation, fitted models, formal proofs, layout checks, and physical measurements are distinct evidence classes.

## 3. Architectural separation

Keep these artifacts independently versioned:

1. **Physical device model:** mathematical model, parameter definitions, units, operating domain, assumptions, and uncertainty.
2. **Calibration procedure:** raw-data ingestion, fitting, initialization, targeted measurement selection, and model diagnostics.
3. **Lean4 acceptance contract:** formal predicates defining required behavior and the evidence obligations for acceptance.
4. **Technology adapter:** pinned PDK identity, layer mapping, component mapping, port semantics, and tool compatibility.
5. **Layout implementation:** technology-aware placement/routing and export through an established layout engine.
6. **Evidence manifest:** content hashes, toolchain identity, source provenance, verification results, and evidence classification.

No layer may silently promote a claim from another layer into a stronger evidence class.

## 4. Implementation sequence and evidence gates

### G0 — PDK identity

- Select one actual SiEPIC SOI process target.
- Record upstream repository URL, immutable commit or release tag, license, supported process modules, and tool compatibility.
- Extract the layer map and component definitions from that exact revision.
- Do not combine EBeam and CUMEC process assumptions into a synthetic layer map.
- If the required revision or process evidence is unavailable, mark the adapter `blocked-unpinned`.

**Exit evidence:** pinned source identity, license review, layer-map provenance, and supported-device inventory.

### G1 — Component integrity

- Define a minimal passive MZI and reference structures using supported PDK components.
- Obtain ports from actual component definitions; include center, orientation, width, layer, and cross-section/type.
- Validate parameter ranges and geometry.
- Do not infer active heater, metal, via, detector, or probe-pad availability from layer numbers alone.

**Exit evidence:** component tests, port tests, geometry checks, and PDK-source references.

### G2 — Routing integrity

- Use a technology-aware router or PDK-provided routing primitives.
- Euler routing may be used only when supported by the chosen waveguide cross-section and router.
- Validate curvature/bend constraints, width, layer continuity, endpoint alignment, obstacle clearance, and connectivity.
- A sequence of rectangles with sharp corners is not an Euler bend.
- Routing failure must stop the build; no silent fallback to invalid geometry.

**Exit evidence:** route tests and independent geometry/connectivity inspection.

### G3 — Layout serialization

- Use KLayout's supported layout API or another established, pinned layout engine for OASIS export.
- Do not use the previously proposed custom subset writer as a production OASIS encoder.
- Reopen the exported file independently and compare database unit, cell hierarchy, layer inventory, and geometry counts or canonical geometry hashes.
- OASIS export success is not DRC or fabrication qualification.

**Exit evidence:** export/reopen test, geometry comparison, tool versions, and output hash.

### G4 — Provenance integrity

Record hashes of the source netlist, PDK identity manifest, configuration, scripts, and output layout. Record tool versions, units, database grid, verification commands, result status, and timestamp.

Use explicit evidence states such as:
- `specified`
- `simulated`
- `measured`
- `fitted`
- `assumed`
- `formally-verified`
- `layout-verified`
- `fabrication-qualified`

A manifest field is a provenance claim, not proof that the claim is true. Verification records must identify the actual tool invocation and result.

### G5 — Calibration readiness

- Freeze the device-computation contract and required operating domain.
- Define training, validation, and held-out partitions before test data are used.
- Preserve raw observations and instrument metadata.
- Compare individual calibration with learned initialization plus targeted correction.
- Report calibration effort, prediction error, coverage, false acceptance, and final independent contract compliance.

**Exit evidence:** reproducible analysis, partition manifest, model version, uncertainty report, and predeclared acceptance thresholds.

### G6 — Physical qualification

Requires fabricated structures and traceable measurements. Do not label simulated or public third-party data as EIS-fabricated measurements.

## 5. Calibration experiment

### Baseline

Calibrate every device independently using the full declared measurement procedure.

### Candidate

Train a population model on the training population. Use its predictions to initialize calibration of held-out devices, then perform only the targeted measurements specified by the candidate procedure.

### Required metrics

- number of measurements per device;
- calibration elapsed time;
- calibration energy, if instrumented with a defensible method;
- prediction error and uncertainty coverage;
- proportion of devices requiring full recalibration;
- false-acceptance rate under an independent acceptance test;
- final computation-contract compliance.

### Partition discipline

Do not split repeated observations from the same physical device across training and test partitions. Report separately:
- held-out cells on represented dies;
- held-out dies;
- held-out wafers or fabrication runs, when available.

These test different levels of portability and must not be conflated.

### Acceptance rule

The candidate succeeds only if qualification effort is reduced while the predeclared reliability and computation-contract criteria remain satisfied. Numerical thresholds must be derived from the intended contract and measurement uncertainty before held-out evaluation; this specification does not invent them.

## 6. Open publication policy

Publish EIS-authored schemas, protocols, algorithms, formal contracts, test scripts, and data for which EIS has redistribution rights. Preserve original licenses and notices for third-party PDKs, models, and datasets. Keep NDA or supplier-restricted process data out of the public repository. A public GitHub repository does not grant redistribution rights to third-party content.

## 7. Current implementation boundary

This document establishes the work plan and acceptance discipline. It does not certify that G0–G6 have passed. Each gate must link to its own reproducible artifact and evidence record before being marked complete.
