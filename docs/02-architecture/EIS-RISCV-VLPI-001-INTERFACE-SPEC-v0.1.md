# EIS-RISCV-VLPI-001 — RISC-V / VLPI Tile Interface Specification

**Status:** Draft, technology-independent interface contract  
**Version:** 0.1.0  
**Repository workstream:** EIS VLPI–VLSI co-design  
**Depends on:** EIS-PTC-MZI-001 (PR #81, draft); EIS-PTC-10x1 reconstruction (PR #78, draft)  
**Normative language:** MUST, MUST NOT, SHOULD, MAY are requirements keywords.

## 1. Purpose and scope

Define the control, data, telemetry, calibration, fault, and energy-accounting boundary between an electronic RISC-V control processor and one or more Very Large-Scale Photonic Integration (VLPI) compute tiles.

This specification is technology-independent. It defines logical responsibilities and observable interface behavior; it does not select a RISC-V core, bus fabric, memory technology, foundry, package, optical geometry, electrical signaling standard, or physical pinout.

The first implementation target is a KKA tile whose logical cell interface is described by EIS-PTC-MZI-001. A tile may contain many optical cells and associated electronic support. A logical tile is not assumed to equal one MZI, one die, one package, or one attention head.

## 2. Architecture and responsibility split

The system has three cooperating planes:

1. **RISC-V control plane.** Runs firmware/runtime services; accepts work descriptors; validates and schedules commands; manages queues, buffers, calibration state, telemetry, faults, and energy ledgers; coordinates electronic support devices. It MUST NOT silently reinterpret a rejected operation or claim that a command completed merely because it was enqueued.
2. **Photonic compute plane.** Executes the tile's specified optical transformation (for the initial KKA path, interference-derived operations). It exposes bounded command, completion, status, and calibration interfaces. Its internal optical implementation remains behind the tile contract.
3. **VLSI support plane.** Provides memory and data movement, clock/reset, laser and modulator drivers, detector front ends, ADC/DAC where used, power conversion/monitoring, thermal sensors/actuators, and package/host interfaces. These functions may be integrated, distributed, or external; the interface MUST identify which are inside the accounting boundary.

RISC-V is selected as a candidate control ISA, not as a claim that all system control must reside on one CPU. The implementation MAY use one controller per tile, a shared controller for a tile group, or a hierarchy. The choice MUST be justified by measured command rate, queue depth, calibration cadence, telemetry volume, fault-containment needs, latency, and energy.

## 3. Design invariants

- **Contract authority:** the versioned tile contract defines legal commands, port roles, units, limits, and completion semantics. Firmware and LLM-generated artifacts MUST NOT override it at runtime.
- **Deterministic control:** identical accepted descriptors under identical declared state and versioned configuration MUST produce the same command interpretation and auditable sequence of state transitions. Physical outputs need not be bit-identical unless a separate measured tolerance contract says so.
- **Explicit state:** every command is either rejected before issue, accepted with a unique transaction ID, completed, failed, cancelled, or timed out. No silent defaults.
- **Backpressure:** queue-full and resource-unavailable conditions are explicit; producers MUST retain or retry work according to the defined policy.
- **No false completion:** enqueue, dispatch, optical execution, detector capture, host-visible result, and energy-ledger closure are distinct events.
- **Evidence discipline:** specified, formally verified, simulated, experimentally demonstrated, and measured are distinct evidence classes. This interface specification does not establish physical performance or energy savings.
- **Energy boundary:** all reported energy values identify interval, scope, measurement source, calibration version, and uncertainty/status.

## 4. Logical topology

A system instance contains:
- one or more RISC-V control agents;
- one or more tile endpoints, each with a stable `tile_id` and contract version;
- optional shared VLSI support endpoints (memory, laser, detector, thermal/power controller);
- host/system interface and persistent provenance store.

A tile endpoint MUST expose:
- capability and contract discovery;
- command submission and queue status;
- completion/result retrieval;
- calibration control and calibration-state query;
- telemetry snapshot/stream access;
- fault and reset status;
- energy-accounting records or references.

The physical transport may be memory-mapped registers, descriptor rings over an interconnect, a coherent or non-coherent fabric, a serial control link, or a combination. Transport selection is an implementation profile and MUST preserve the logical semantics below.

## 5. Command descriptor and queue semantics

### 5.1 Command envelope

Each command MUST carry:
- `protocol_version`, `tile_id`, `tile_contract_id`;
- unique `transaction_id` and monotonically increasing per-producer `sequence_number`;
- `opcode` and typed `payload`;
- input/output buffer references with byte length, alignment, ownership, and memory-domain attributes;
- `deadline` or explicit no-deadline marker;
- `calibration_epoch` expected by the command;
- requested result/telemetry flags;
- provenance reference for workload, model, and software/configuration identity.

The JSON Schema in `../schema/riscv-vlpi/command-envelope.schema.json` defines a transport-neutral interchange representation. A binary descriptor or MMIO mapping MUST preserve all required fields and validation rules.

### 5.2 Required command classes

Minimum logical opcode classes:
- `DISCOVER_CAPABILITIES`
- `LOAD_INPUT` / `BIND_BUFFERS`
- `EXECUTE`
- `READ_RESULT`
- `CALIBRATE`
- `READ_TELEMETRY`
- `CANCEL`
- `QUIESCE` / `RESUME`
- `RESET`

Tile-specific operations MUST be capability-advertised and versioned. Unknown opcodes MUST be rejected with a stable error code.

### 5.3 Queue behavior

The endpoint MUST expose submission capacity, queue occupancy, and backpressure state. Submission is atomic: either the complete descriptor is accepted and assigned/confirmed a transaction ID, or it is rejected without partial execution.

A successful submit response means **accepted**, not executed. Completion is reported asynchronously or through polling and MUST include terminal status, timestamps or monotonic cycle counters, result references, calibration epoch used, and fault flags.

Ordering is per queue. The default ordering is FIFO within one queue. Cross-queue ordering is unspecified unless an explicit dependency/fence is supplied. A fence MUST identify the transactions it orders. Cancellation is best-effort after dispatch and MUST report whether work was cancelled before execution, stopped during execution, or could not be cancelled.

Timeouts MUST NOT be represented as successful completion. A timed-out transaction may later be reconciled through transaction lookup; the runtime MUST prevent duplicate execution when retrying an uncertain submission.

### 5.4 Buffer ownership and coherency

Every buffer reference MUST declare address space/domain, length, alignment, access direction, and ownership-transfer point. The profile MUST specify cache-coherency behavior and required memory barriers. The tile MUST NOT read a producer-owned input before ownership transfer, nor write a consumer-owned output after ownership has returned to the consumer.

DMA-capable implementations MUST define address width, IOMMU/protection domain, descriptor lifetime, maximum transfer size, and error reporting. These values are implementation-profile parameters, not assumed here.

## 6. Calibration interface

Calibration is a controlled state transition, not an implicit side effect of execution.

Each tile MUST expose:
- calibration capability and supported procedure IDs;
- active `calibration_epoch`;
- calibration validity state: `VALID`, `STALE`, `IN_PROGRESS`, `FAILED`, or `UNKNOWN`;
- calibrated parameter set identifier and provenance;
- validity conditions and expiry/drift criteria;
- calibration start, progress, completion, and failure records.

A calibration operation MUST specify the procedure, target ports/cells, input stimulus reference, measurement channels, requested tolerance, and acceptance contract. The result MUST record measured values, units, uncertainty, instrument/source identity, timestamp, environmental conditions, and evidence class.

An execution descriptor MUST name the calibration epoch it expects. If that epoch is not active and valid, the tile MUST reject the command or return an explicit stale-calibration status; it MUST NOT silently substitute a newer or older epoch.

The initial MZI model's heater resistance, phase efficiency, thermal coupling matrix, coupler visibility, and loss parameters remain caller-supplied/unknown until characterized. This interface does not convert synthetic model fixtures into device calibration.

## 7. Telemetry and fault model

Telemetry records SHOULD include:
- command/queue counters, occupancy, backpressure, latency and timeout counts;
- optical source/laser state and power, when instrumented;
- detector/BPD and ADC capture status, saturation and validity;
- heater commands, measured voltage/current, estimated or measured power, and thermal sensor values;
- supply rails, clock/reset state, temperature, and power/energy monitor status;
- calibration epoch and drift indicators;
- error, warning, and fault counters.

Every metric MUST declare name, value, unit, timestamp or interval, source, validity, uncertainty (if known), and evidence/provenance class. Missing sensors MUST be reported as unavailable, not zero.

Faults MUST be classified at minimum as recoverable, command-fatal, tile-fatal, or system-fatal. Fault records MUST include stable code, source, affected transaction/tile, timestamp, and recovery recommendation. A reset MUST state what state, queues, calibration, and telemetry are preserved or invalidated.

## 8. Energy accounting contract

### 8.1 Accounting principle

The primary EIS comparison metric is energy per accepted useful transformation, under a matched quality, latency, workload, and system-boundary contract. Device-only optical energy or a processor's nominal TOPS/W is not a system result.

Every energy record MUST identify:
- `accounting_scope_id` and boundary version;
- measurement interval start/end and synchronization basis;
- included components and excluded components;
- measured versus modeled/estimated status;
- sensor/instrument or model identity and calibration;
- energy value and unit (canonical SI joules);
- uncertainty or explicit unknown;
- workload/result transaction set;
- accepted-useful-result count and acceptance-contract ID.

### 8.2 Component ledger

Where applicable, separately account for:
- laser/source electrical input and optical output (do not conflate);
- modulator/heater drive energy;
- photodetector and analog front-end energy;
- ADC/DAC and clocking;
- RISC-V control processor and memory;
- DMA/interconnect and external host transfers;
- thermal management/cooling attributable to the tile;
- power conversion and shared support overhead.

Shared overhead allocation MUST declare the allocation method and denominator. Do not double-count energy across parent and child scopes. Report both component subtotals and the total boundary value where measurements support them.

### 8.3 Useful transformation acceptance

A result counts as useful only when its transaction is complete, its output passes the declared numerical/functional acceptance contract, and all required validity checks (including calibration epoch) pass. Failed, timed-out, cancelled, dropped, or invalid results MUST NOT enter the useful-result denominator. Report attempted, accepted, rejected, and failed counts separately.

The normalized metric is:

`E_useful = E_total(scope, interval) / N_accepted_useful`

If `N_accepted_useful = 0`, the metric is undefined, not zero. Any comparison against an electronic baseline MUST match workload, output quality, latency/service target, utilization policy, and accounting boundary.

## 9. Security, isolation, and provenance

The implementation profile MUST define privilege boundaries, firmware update/authentication, debug access, DMA protection, queue ownership, and tenant isolation. Commands MUST be attributable to a producer identity and software/configuration digest. Calibration and energy records MUST be tamper-evident or stored in an auditable provenance system.

Untrusted LLM agents MAY propose descriptors or analysis but MUST NOT directly write privileged control registers, bypass validation, change acceptance criteria, or certify their own outputs. A deterministic validation layer and the tile contract remain authoritative.

## 10. Versioning and compatibility

Protocol version, tile contract version, capability set, and calibration epoch are separate identifiers. A minor protocol revision MUST NOT change the meaning or units of existing fields. Unknown optional fields MAY be ignored only when the versioned profile permits it; unknown required features MUST cause explicit rejection.

A controller MUST discover capabilities before issuing tile-specific commands. A tile MUST report unsupported features and version mismatch explicitly.

## 11. Required verification and acceptance gates

The interface is not implementation-complete until evidence exists for:
1. schema validation of valid and invalid command envelopes;
2. deterministic state-machine tests for submit/accept/complete/fail/cancel/timeout;
3. queue saturation and backpressure tests;
4. buffer ownership and coherency tests on the selected transport;
5. calibration epoch invalidation and stale-epoch rejection;
6. telemetry unit/provenance/unknown-sensor tests;
7. energy-ledger reconciliation with no double-counting;
8. useful-result denominator and zero-result handling;
9. fault injection and reset-state tests;
10. an end-to-end tile test using a declared tile contract and evidence manifest.

Formal properties SHOULD be stated in Lean4 for command-state transitions, queue acceptance, calibration-epoch validity, ownership transfer, and energy-ledger conservation/reconciliation. Python or another executable reference model MAY serve as an independent conformance oracle; it is not a substitute for formal proof or hardware measurement.

## 12. Explicit non-goals and open decisions

This v0.1 does not select:
- a particular RISC-V core, vendor, privilege profile, extensions, or safety/security certification;
- AXI, TileLink, CHI, PCIe, CXL, NoC, or a custom bus;
- cache coherence strategy, DMA engine, memory map, register offsets, interrupt topology, or clock-domain crossing;
- optical geometry, foundry PDK, MZI layout, detector implementation, laser architecture, package, or chiplet standard;
- a fixed tile size, controller-to-tile ratio, or throughput target.

These are later implementation profiles and must be selected from measured workload/control requirements and foundry/package constraints. GF, TSMC, and Intel process support or ecosystem relationships do not by themselves establish that a specific RISC-V core, interface IP, or photonic tile is available in a given process.

## 13. Relationship to EIS-PTC-MZI-001

EIS-PTC-MZI-001 defines the logical single-MZI cell and its typed optical/electrical ports, three heater controls, and evidence boundaries. EIS-RISCV-VLPI-001 defines how a control processor discovers, configures, calibrates, commands, observes, and accounts for a tile built from such cells.

The MZI cell's three heater controls are not equivalent to three processor command queues or three tile ports. Cell geometry and foundry mapping remain behind a later explicit approval gate.

## Appendix A — Initial implementation sequence

1. Validate the JSON command-envelope schema and create a typed Python dataclass/reference model.
2. Define the tile capability and completion schemas.
3. Implement a pure state-machine model with queue/backpressure and calibration epochs.
4. Add Lean4 invariants for command lifecycle and useful-result/energy-ledger accounting.
5. Bind the model to the EIS-PTC-MZI-001 port-map and evidence manifest.
6. Select a transport profile only after command-rate, data-rate, and calibration/telemetry budgets are measured.
7. Add hardware-specific memory map, DMA, interrupt, CDC, and signoff only after platform selection.

## Appendix B — Evidence status

This document is a **specified** logical contract draft. It is not a formally verified implementation, measured interface, fabricated architecture, or demonstrated energy-saving system. All numerical limits and transport-specific parameters remain open until supported by an implementation profile and evidence.
