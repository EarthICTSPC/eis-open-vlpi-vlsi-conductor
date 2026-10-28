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


## End-to-end useful-inference energy contract (EIS metric)

### Primary metric

**Joules per accepted useful inference, at a declared quality and latency, measured across the complete system.**

For a frozen workload and measurement interval:

`E_useful = E_system / N_accepted`

where:
- `E_system` is measured energy in joules across the declared complete-system boundary during the interval.
- `N_accepted` is the number of inference results that satisfy the pre-registered acceptance criteria within the declared latency limit.
- A result that misses the latency limit or fails the quality/validity criteria is not counted as accepted; its energy remains in `E_system`. This prevents failed or late work from making the metric look artificially efficient.

Report both the ratio and its raw components (`E_system`, `N_accepted`, elapsed time, and rejected/late result counts). If no inference is accepted, report the run as failed and the metric as undefined—not zero.

### Required declaration before comparison

Freeze and publish:
1. **Task and workload:** model/checkpoint hash, dataset or prompt-set hash, tokenizer, input/context-length distribution, output-length or stopping policy, batch/concurrency, warm-up, and run duration.
2. **Quality and acceptance:** task-specific quality metric and threshold, correctness/validity checks, sampling/decoding settings, and the rule for accepting an individual result.
3. **Latency:** end-to-end latency limit and reporting statistic (including p50/p95/p99 where appropriate); state whether queueing and preprocessing are included.
4. **System boundary:** list every included energy consumer and measurement method. Include compute, lasers and optical sources, modulation and phase control, detectors, ADC/DAC, electrical regeneration, memory, data movement/interconnect, host/control processors, power conversion, and cooling where present. Identify any excluded component explicitly; do not call a partial component measurement a complete-system result.
5. **Comparison protocol:** same useful task, acceptance threshold, latency requirement, workload, and accounting boundary for photonic and electronic baselines. Report throughput and quality alongside energy so the ratio cannot hide degraded service.

### Evidence classes and claims

- A Lean theorem may prove properties of the *metric definition*, acceptance predicate, or accounting logic; it cannot prove that physical energy measurements are accurate.
- Software tests may validate workload accounting and rejection rules.
- Measured energy requires calibrated instrumentation or a documented, auditable energy-accounting method, with raw data and uncertainty retained.
- Simulation, device estimates, and projected TOPS/W must be labeled separately and must not be presented as measured end-to-end joules per accepted inference.
- Any claimed advantage over a GPU must name the GPU/system, software stack, operating conditions, workload, and quality/latency thresholds. The claim is valid only within that declared comparison.

This is an EIS evaluation contract to be connected to TorchLean-specified model behavior and the EIS Conductor evidence ledger. It does not imply that upstream TorchLean already measures system energy or supplies these acceptance criteria.
