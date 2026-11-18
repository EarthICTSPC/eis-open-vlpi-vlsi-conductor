# EIS-KKA-BENCH-001 — Three-way attention benchmark

**Status:** executable software protocol scaffold; no physical SOI measurement or KKA/SoftMax equivalence is claimed.

## Research question

At matched output quality, context, workload, precision and latency, what computation and energy are removed, replaced or added when conventional attention is compared with an interference-native KKA implementation?

## Three configurations

1. **Electronic baseline:** scaled dot-product attention, including QK, scaling, stable SoftMax and AV.
2. **Electronic KKA reference:** a caller-supplied, versioned KKA score/weight operator operating on complex fields. It must not silently call SoftMax. Its transfer, phase reference, detector convention and normalization semantics are part of the run manifest.
3. **Physical SOI KKA:** the same algorithmic contract, with measured device outputs and synchronized power/latency traces. The physical adapter must ingest measured outputs; it must not synthesize or infer device measurements from the electronic reference.

The KKA operator is deliberately an injected interface. This scaffold does not invent a KKA attention equation or assert that arbitrary interference outputs equal normalized SoftMax weights. A study must pin the source equation, encoding, transfer response, detector convention and output semantics before a KKA result is eligible for comparison.

## Acceptance and fairness

All three paths must use identical Q/K/V tensors, masks, head dimensions, sequence lengths, batch, causal/padding behavior and output-value convention. Report:
- max absolute and relative output error against the electronic baseline;
- cosine similarity and RMS error;
- task-level quality on a frozen dataset/model when available;
- p50/p95 latency and throughput;
- energy by component and system boundary;
- raw operation ledger, keeping MACs, additions, comparisons, exponentials, divisions and optical interference events distinct.

A result failing the predeclared quality tolerance is **not an energy win**. Do not compare only operation counts or optical-core energy.

## Operation ledger

For full attention with sequence length S, H heads and head dimension d:

- QK: H S² d MACs (2 H S² d conventional FLOPs if multiply and add count separately).
- Score scaling: H S² scalar multiplications.
- Stable SoftMax: row maximum comparisons/reductions, H S² subtractions, H S² exponentials, row-sum additions, and H S² divisions. Keep each operation class separate; do not count exp/div as ordinary FLOPs.
- AV: H S² d MACs (2 H S² d conventional FLOPs).
- KKA: count the actual implementation's operations/interference events from its own trace. Do not infer a universal operation-equivalence factor.

The often-quoted rough SoftMax count ~3 H S² is only a shorthand for exponentials + score subtractions + normalization divisions, excluding row-max and row-sum reductions. Adding score scaling gives another H S² multiplications. This is not a standardized FLOP count and must not be added to MACs without preserving operation types.

For one autoregressive decode query against S cached keys, replace S² with S for per-token attention score/SoftMax work: approximately 3 H S shorthand operations, plus H S score scaling multiplications. This is per layer and assumes all H heads attend over S positions.

## Energy boundary

For physical SOI KKA, include synchronized measurements for:
- optical source/laser and distribution;
- modulator drive;
- phase shifters/heaters and phase-lock/control;
- detector, TIA and ADC (where present);
- calibration and recalibration;
- electronic control, memory/data movement and interface;
- cooling/facility overhead when included in the declared boundary.

Integrate measured power over a defined run interval using timestamped samples. Include idle/background subtraction only when separately measured and documented. Report both gross and incremental energy. Never use simulated power as measured power.

## Files

- benchmark.py: reference baseline, injected KKA operator, physical trace integration and output metrics.
- test_benchmark.py: deterministic software tests, including fail-closed KKA interface tests.
- run_manifest.example.json: provenance and workload manifest.

## Run

    python -m unittest discover -s experiments/EIS-KKA-BENCH-001 -p 'test_*.py' -v

No GPU, SOI device, foundry PDK or FlexCompute service is required for these software tests. A physical result requires calibrated instruments, synchronized power traces and traceable device data.

## Evidence labels

- **E0:** specification / proposed protocol.
- **E1:** deterministic software test.
- **E2:** independently reproduced numerical result.
- **E3:** simulation with declared model and provenance.
- **E4:** physical device measurement with calibration and uncertainty.
- **E5:** matched end-to-end model/service workload.

This PR scaffold is E0/E1 only until its checks pass. It does not claim KKA accuracy, physical energy savings, or SoftMax equivalence.
