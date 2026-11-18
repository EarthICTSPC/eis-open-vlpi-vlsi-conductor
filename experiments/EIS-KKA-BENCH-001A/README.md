# EIS-KKA-BENCH-001A — Tian equation and operation-count reproduction

**Status:** formal specification and reproducible software artifact under review. No physical SOI result or energy-saving result is claimed.

## Purpose

Freeze what Tian et al. call the interference operator, formalize the ideal detector identity, and produce an auditable operation ledger before estimating any avoided work or energy.

Primary source: Tian et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025), DOI: [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).

The formal source is `EISKKA/Bench001A.lean`. The Lean executable emits JSON; `generate_python.py` turns that generated JSON into the Python module `formal_counts.py`. The Python tests consume that generated module. Lean is the authority for the equations and integer count definitions.

## Equation boundary

Tian Eq. (1) defines the two-field interference operation:

```
a □ b = |a|² + |b|² + 2 Re(a b*)
```

The 50:50 balanced detector removes the self-intensity terms. With output fields `(a+b)/sqrt(2)` and `(a-b)/sqrt(2)`, responsivity `R`, and detector polarity `I_plus - I_minus`:

```
Y = R ( |a+b|²/2 - |a-b|²/2 )
  = 2 R Re(a b*)
```

Lean proves both identities for the ideal two-field model. This does not establish real coupler imbalance, responsivity matching, noise, bandwidth, phase drift, or a foundry device's transfer function.

Tian Eq. (2) is an approximate model correspondence:

```
SoftMax(QᵀK / sqrt(d)) V  ~  (Q_KKAᵀ □ K_KKA) □ V_KKA
```

The paper motivates this with random Fourier feature analysis and supports it with numerical and experimental model comparisons. The `~` is essential: this is not a universal equality for arbitrary Q/K/V tensors. The trained KKA projections/encodings are part of the approximation. The Lean development records this status and deliberately does not prove an arbitrary-tensor equivalence.

## What is replaced, and what is not

For one attention invocation with `H` heads, sequence length `S`, Q/K feature dimension `d`, and V output dimension `d_v`:

| Conventional attention-core work | Count |
|---|---:|
| QK multiplications | `H S² d` |
| QK additions | `H S² (d-1)` |
| Score scaling multiplications | `H S²` |
| Stable SoftMax row-max comparisons | `H S (S-1)` |
| SoftMax score subtractions | `H S²` |
| SoftMax exponentials | `H S²` |
| SoftMax row-sum additions | `H S (S-1)` |
| SoftMax normalization divisions | `H S²` |
| AV multiplications | `H S² d_v` |
| AV additions | `H S d_v (S-1)` |

Tian's KKA formulation replaces the QK and AV product/accumulation stages with interference-based field-pair operations and omits the explicit SoftMax and the `1/sqrt(d)` score scaling in the KKA path. The paper's Eq. (2) asserts approximate attention correspondence, not a universal numerical identity. Therefore this work reports KKA interference samples separately:

- QK stage: `H S² d` logical field-pair interference samples.
- Value aggregation stage: `H S² d_v` logical field-pair interference samples.

These are not FLOPs and must not be subtracted from electronic MAC counts as if they were the same operation. They are logical pair-event counts implied by the matrix-product dimensions. Physical time integration, modulation, phase control, calibration, detector/TIA/ADC, memory movement and laser energy are not represented by these counts.

The attention-core ledger excludes Q/K/V learned projections. Tian's paper also expresses Q, K and V generation using the interference operator; if the benchmark boundary includes those projections, they must be counted in a separate projection ledger with the actual input/weight dimensions. Do not silently omit or double-count them.

## Worked count example

For the Lean emitter's illustrative shape `H=2, S=10, d=5, d_v=5`:

- 200 attention scores.
- QK: 1,000 multiplications + 800 additions.
- Score scaling: 200 multiplications.
- Stable SoftMax: 180 row-max comparisons + 200 score subtractions + 200 exponentials + 180 row-sum additions + 200 divisions.
- AV: 1,000 multiplications + 800 additions.
- KKA logical field-pair samples: 1,000 for QK + 1,000 for value aggregation.

The 200 score-scaling multiplications plus the five stable-SoftMax categories total 1,160 typed conventional operations that the KKA path is designed to bypass or replace. This is **not** a claim of 1,160 physical operations or a net system saving: the row reduction is replaced by time-domain integration, SoftMax approximation quality must be measured, and the KKA path adds interference, modulation, control, calibration and detector costs. QK/AV arithmetic terms are replaced by interference events, not counted as eliminated work.

## Generated artifacts

- `EISKKA/Bench001A.lean`: theorem-backed field identities, exact Nat operation-count definitions and JSON emitter.
- `formal_spec.generated.json`: Lean-emitted machine-readable specification.
- `generate_python.py`: deterministic JSON-to-Python generator.
- `formal_counts.py`: generated Python constants for the example shape.
- `test_formal_counts.py`: checks generated counts and guards operation-type separation.

## Reproduce

From repository root:

```bash
lake exe eis_kka_bench_001a > experiments/EIS-KKA-BENCH-001A/formal_spec.generated.json
python experiments/EIS-KKA-BENCH-001A/generate_python.py
python -m unittest discover -s experiments/EIS-KKA-BENCH-001A -p 'test_*.py' -v
```

The workflow runs Lean with warnings-as-errors, emits the JSON, regenerates Python, checks that the committed generated module is current, and runs the tests.

## Explicit non-claims

- No universal proof that KKA equals SoftMax for arbitrary tensors.
- No proof that the trained KKA model has identical outputs or task quality to standard attention.
- No claim that the ideal BPD identity includes real-world mismatch/noise.
- No physical SOI measurement, FlexCompute simulation, GPU benchmark or energy result.
- No inference that the logical interference-event count equals physical device cycles or energy.
