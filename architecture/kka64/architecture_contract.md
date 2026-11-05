# EIS-KKA-64-001 — Architecture and workload contract

**Status:** DRAFT / SPECIFICATION IN PROGRESS  
**Version:** 0.1.0  
**Parent:** [Issue #66](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/66)  
**Scope:** logical KKA attention tile; not a foundry layout or a complete LLM.

## 1. Meaning of 64×64

For this workstream, 64×64 means a logical attention block producing a 64-query × 64-key interaction matrix:

\[
S = QK^T, \qquad Q,K \in \mathbb{R}^{64\times d_h}
\]

and therefore 4,096 pairwise score outputs for one head/block.

This is a **workload-level definition**, not a physical topology. It does not imply:
- 4,096 MZIs;
- 4,096 Tian KKA cells;
- a 64×64 MZI mesh;
- one physical primitive per score;
- an entire transformer head, transformer layer or LLM.

The mapping from one logical score to optical fields, couplers, phase-control elements, detectors and readout channels is an unresolved architecture variable. It must be derived from the KKA algorithm and validated reference implementation before device counts are frozen.

## 2. Computation boundary

The first candidate boundary is the query–key attention interaction and the KKA transformation demonstrated in the Tian photonic-transformer work. The architecture review must explicitly decide whether the tile returns:
1. raw QKᵀ-like scores;
2. scores after a KKA softmax-like transformation; or
3. a larger attention result including value aggregation.

Do not describe option 3 as implemented unless the algorithm and device mapping actually include it. List all operations left to electronics: Q/K formation, encoding, scaling, residual normalization, value multiplication, accumulation, output projection, memory and host control.

## 3. Required workload freeze

Before performance claims, freeze:
- model and checkpoint, layer/head and attention variant;
- sequence/context length, batch and prefill/decode phase;
- Q and K shapes, head dimension \(d_h\), and whether 64 is a tile dimension or full sequence length;
- precision and quantization for optical and electronic paths;
- input/output encoding, wavelength and polarization assumptions;
- score scaling, normalization and exact KKA approximation;
- numerical score error and downstream model-quality tolerance;
- throughput plus p50/p95 latency targets;
- reconfiguration frequency, active duty cycle and calibration policy;
- memory/KV-cache boundary and all data movement included in energy.

Until this freeze is reviewed, throughput, TOPS/W and system-energy targets remain **TBD**, not assumed.

## 4. Formal and executable authority

- Lean4 is the mathematical authority for device-independent field and interference properties.
- Python is the deterministic executable reference and cross-language conformance implementation.
- Device-specific complex transfer functions are parameters/models with provenance and validity domains; they are not silently promoted to universal mathematical laws.
- PDK adapters implement the interface. A PDK's cell names or default models do not define KKA semantics.

The current scalar Lean contract and its draft PR do not prove full tensor attention equivalence, physical device behavior, thermal behavior, energy efficiency or a 64×64 implementation.

## 5. Logical-to-physical mapping table (to be completed)

| Logical quantity | Required definition | Current status |
|---|---|---|
| Query vector | \(q_i\), dimension, encoding and update cadence | TBD |
| Key vector | \(k_j\), dimension, encoding and update cadence | TBD |
| Pairwise score | Mathematical observable and scaling | TBD |
| KKA transform | Exact approximation and operating domain | TBD |
| Optical primitive | Number/type per score and per tile | OPEN |
| Phase controls | Number/type, static/dynamic, calibration | OPEN |
| Detector/readout | Number, placement, bandwidth, noise | OPEN |
| Electronic residual | Explicit operation list | OPEN |

## 6. System energy boundary

Primary metric:

\[
E_{\mathrm{accepted\ block}} =
\frac{E_{\mathrm{total\ system}}}
{N_{\mathrm{accepted\ useful\ attention\ blocks}}}
\]

Include wall-plug laser energy, coupling/distribution, optical loss, modulation, phase control, calibration, detection, ADC/DAC, memory/KV-cache traffic, communication, host electronics, packaging and thermal management. Report idle and reconfiguration energy as well as active energy.

The electronic baseline must use the same model, tensors, precision/quality target, batch/context, throughput/latency and system boundary. Device-only optical energy must not be compared with full-system electronic energy.

## 7. Reference baseline and claims

Tian et al.'s published 10×1 prototype is an attributed literature baseline. Preserve the paper's stated measurement conditions and distinguish reported measurements from scaling projections. Do not copy its reported benchmark or energy numbers into EIS measurement fields.

## 8. Open decisions

1. Does the MVP target long-context prefill, a ViT perception task, or both in staged validation?
2. Does one tile represent 64 tokens by 64 tokens, or 64 query/key vectors drawn from a larger sequence?
3. Which KKA stage is optically implemented?
4. What physical topology realizes the required field interaction?
5. Which tuning mechanism meets static-power, update-rate and calibration constraints?
6. What is the matched electronic baseline and required system-level advantage?

## 9. Exit criteria for G0

G0 is complete only when the model/workload, tensor shapes, computation boundary, numerical/quality acceptance, latency/throughput, energy boundary and electronic baseline are versioned and reviewed. Unknown values remain explicitly TBD; no fabricated numeric target is permitted.
