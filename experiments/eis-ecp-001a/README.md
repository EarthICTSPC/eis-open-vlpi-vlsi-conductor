# EIS-ECP-001A — numerical contract and saturation audit

Status: **specified reference implementation; not photonic-device evidence**.

This patch tightens the software experiment before any electromagnetic simulation or energy comparison. It does not claim Lean/Python conformance until the canonical Lean source, revision, executable build, and machine-readable contract are bound and tested.

## Frozen mathematical workload

For each request, Q,K,V have shape (T,D) with T=D=64. Q and K entries are sampled uniformly from [-1/sqrt(D), +1/sqrt(D)], and V entries from [-1,1]. The operator is Y=(Q K^T)V with no softmax or normalization.

Each Q and K row has Euclidean norm at most 1, so Cauchy–Schwarz gives |(QK^T)[i,j]| <= 1. This is a mathematical bound for the declared input domain, not a statement that scores are normally near 1.

Since each score and each V entry has magnitude at most 1, the unnormalized output satisfies |Y[i,k]| <= T. The bound is conservative; actual distributions must be measured on the frozen workload.

## Quantization and saturation rules

- The quantizer requires finite positive full-scale and bit width >= 2.
- Full-scale denotes the largest representable magnitude; values outside it are clipped.
- Saturation is counted **before clipping** and reported separately from numerical error.
- Default theoretical-safe score and output scales are 1 and T respectively. These avoid clipping for ideal exact inputs under the stated domain, but quantization/noise in intermediate stages can still change later values.
- Calibration from observed samples is not allowed to silently change the frozen protocol. If empirical calibration is chosen later, define a separate protocol revision and freeze calibration inputs before evaluation.

## Noise modes (assumptions, not device characterization)

- `shared`: one noisy encoded Q element and one noisy encoded K element are reused across their fan-out; one noisy V element is reused across score rows. This models correlated encoding error due to shared encoded operands.
- `per_use`: independent encoding noise is drawn at each modeled product use. This is a bounding/contrast assumption, not a claim that a particular layout has independent modulators.
- Detector noise is applied at the modeled detection boundary. The model does not represent measured laser RIN, phase drift, crosstalk, thermal coupling, responsivity, shot noise, or a calibrated component transfer function.
- Each physical conversion/quantization boundary must appear exactly once in a model diagram. The reference helper avoids an undocumented second score quantization; changing the stage model requires a protocol revision.

## Evidence and non-claims

This artifact can support unit-tested numerical bounds, quantizer behavior, saturation counts, and simulation results conditional on the declared noise assumptions.

It does **not** establish:
- Lean-to-Python conformance or a proof of the complete attention operator;
- Tidy3D electromagnetic simulation, an MZI transfer function, or a characterized PDK;
- fabricated-device accuracy, hardware latency, GPU performance, or end-to-end inference latency;
- energy per operation, energy per accepted useful transformation, or environmental advantage.

The original CPU benchmark, if run, measures that particular Python/NumPy implementation on the recorded host. The noise sweep is a numerical simulation, not an electromagnetic simulation. Operation counts are not energy estimates.

## Exit gates

1. Run `python -m unittest discover -s experiments/eis-ecp-001a -p 'test_*.py' -v`.
2. Bind the canonical Lean source and revision; build Lean in CI; add cross-language vectors generated from the Lean contract. Until then, conformance status remains `NOT_ESTABLISHED`.
3. Freeze an explicit device-stage diagram and replace assumed noise parameters only with traceable characterized data.
4. Add a separate energy ledger only when each boundary term has a measured or traceably estimated value.
