# Electronic–Photonic Interface Contract

**Status:** `draft` — interface proposal, not a verified implementation.
**Scope:** A contract boundary for co-designing a RISC-V host/control path with a Photonic Transformer Chip (PTC).

## 1. Purpose

Define observable behavior and acceptance obligations at the electronic–photonic boundary before selecting a specific register map, device topology, or foundry implementation. The first prototype may use ordinary RISC-V loads/stores and memory-mapped I/O (MMIO); DMA may be added if profiling shows that sustained data transfer requires it. Custom ISA instructions are not assumed necessary.

## 2. Interface boundaries

| Boundary | Inputs | Outputs / observations | Required specification |
|---|---|---|---|
| Host → control interface | Commands, configuration, buffers | Accepted/rejected command, status | Register or queue semantics, permissions, ordering |
| Electronic input → optical encoding | Digital operands and configuration | Optical fields at named ports | Encoding, precision, normalization, valid ranges, modulation assumptions |
| Photonic computation | Defined optical fields and configuration | Optical output fields | Reference transformation, port ordering, phase/amplitude convention, model assumptions |
| Optical readout → electronics | Detected signal | Digital/analog result and validity | Detector model, noise, dynamic range, conversion, precision, error threshold |
| State/control boundary | Start, reset, calibration, status | Busy/done/error, state observations | Reset semantics, state retention, timeout and fault behavior |
| System energy boundary | Workload and operating conditions | Energy, latency, throughput, quality | Included/excluded components and reproducible measurement method |

## 3. Contract fields

Every concrete interface revision should specify:
- Contract identifier, version, and status.
- Host and PTC timing assumptions.
- Data representation, widths, units, valid ranges, and overflow behavior.
- Register or queue map, read/write semantics, and command ordering.
- Optical ports, wavelength/mode assumptions, field normalization, and phase conventions.
- Startup, reset, calibration, capture, hold, update, and error behavior where applicable.
- Maximum latency and minimum sustained throughput targets.
- Numerical error metric and acceptance threshold.
- Energy-accounting boundary.
- PDK identity and provenance for every technology-specific parameter.
- Test vectors, expected outcomes, and evidence links.

Unknown values must remain explicitly `TBD` or `ASSUMED`; they must not be silently replaced by convenient numbers.

## 4. Proposed acceptance obligations

1. **Interface completeness:** every port, field, unit, state transition, and error path is specified.
2. **Trace legality:** writes, reads, command ordering, and state transitions obey defined rules.
3. **Timing:** start, settling, and timeout rules are defined and checked against an executable trace model.
4. **Functional conformance:** an executable reference model maps accepted input traces to expected output traces.
5. **Driver conformance:** the driver emits only legal transactions and handles completion, timeout, and error conditions.
6. **Photonic refinement:** a candidate implementation is shown to implement or approximate the reference transformation within a declared error bound.
7. **System accounting:** energy and performance include the electronics and conversions required to accept a useful result.
8. **Evidence traceability:** each criterion links to a test, proof, simulation, measurement, assumption, or explicit `NOT-RUN` status.

Numerical thresholds must be agreed before candidate evaluation. The first gate is to define those thresholds and measurement conditions—not to claim they have already been met.

## 5. Lean4's role

Lean4 can encode types, legal traces, state transitions, functional relationships, invariants, and proof obligations. It can prove properties that follow from definitions and assumptions actually represented in the Lean model.

Lean4 alone does not establish that an analog driver, modulator, detector, PDK model, or fabricated photonic circuit behaves as specified. Those links require validated models, conformance tests, simulation, measurement, or other explicit evidence.

## 6. Illustrative trace

```text
RESET
  → CONFIGURE
  → LOAD_INPUTS
  → WAIT_FOR_REQUIRED_SETTLING (if applicable)
  → START
  → POLL / RECEIVE COMPLETION
  → READ_RESULTS
  → CHECK VALIDITY AND ERROR STATUS
  → RECORD RESULT + EVIDENCE
```

This is a sequence sketch, not a register-level standard. Concrete semantics and timing must be defined in a versioned implementation contract.

## 7. Audit note for the proposed Lean sketch

The supplied sketch is a useful starting point, but it contains placeholder propositions (including `True` fields in legality and system acceptance) and an incomplete driver-refinement witness. It must not be called an end-to-end proof until those placeholders are replaced with substantive predicates, the module compiles, and the required theorems are discharged.

## 8. Exit gate

The interface design gate passes when the team has agreed what the PTC dimensions count; frozen a versioned interface contract and timing model; defined the reference computation and numerical error metric; agreed measurable acceptance thresholds and energy boundaries; listed Lean4 proof obligations separately from physical-evidence obligations; and identified a reproducible test path.

**Status remains `draft` until executable checks and review evidence are linked.**