# EIS-TIAN-KKA-LIFT-001A — Numerical Reference Gate: PASS

**Recorded:** 2026-11-21  
**Gate:** Numerical execution of Tian SI-4 Eq. (S13) against all ten Table S1 fitted entries  
**Notebook artifact:** `EIS-TIAN-KKA-LIFT-001A-frozen.ipynb`  
**Notebook SHA-256:** `a9c5db4b31405e2e0d3e78d9e75b79e9a1d08b36a5342fb7e42c3b59661d39f5`

## Result

**PASS — 10/10 entries evaluated.**

Each entry produced a finite `(281, 281)` response on the illustrative voltage grid `VA = VB = np.linspace(0.0, 7.0, 281)`.

| Table S1 entry | Shape | Finite | Minimum | Maximum |
|---|---:|---:|---:|---:|
| S1-row-01 | (281, 281) | True | -1.015855 | 0.984057 |
| S1-row-02 | (281, 281) | True | -0.994070 | 1.005820 |
| S1-row-03 | (281, 281) | True | -0.992061 | 1.007838 |
| S1-row-04 | (281, 281) | True | -1.005728 | 0.994160 |
| S1-row-05 | (281, 281) | True | -0.999709 | 1.000150 |
| S1-row-06 | (281, 281) | True | -0.991339 | 1.008534 |
| S1-row-07 | (281, 281) | True | -0.983850 | 1.016067 |
| S1-row-08 | (281, 281) | True | -1.012707 | 0.987147 |
| S1-row-09 | (281, 281) | True | -1.009759 | 0.990148 |
| S1-row-10 | (281, 281) | True | -1.000664 | 0.999245 |

## What this pass establishes

The EIS implementation of Tian et al. (2025) Supplementary Information SI-4 Eq. (S13), using all ten Table S1 fitted parameter entries, evaluated successfully over an illustrative 281 × 281 voltage grid. All outputs were finite and had the expected dimensions.

The slight excursions outside [-1, 1] are consistent with the additive fitted offset `e_i` in Eq. (S13); the scalar response is not constrained to a normalized optical-power interval.

## Evidence boundary

This pass establishes numerical execution of the transcribed source equation. It does **not** establish:
- reproduction or fit quality against Tian's raw experimental traces;
- that the illustrative grid matches Tian's measurement sampling;
- coefficient units or scalar-observable normalization (not specified here);
- a complex optical transfer function;
- a Tidy3D electromagnetic simulation;
- physical SOI MZI/KKA validation or foundry-process transfer;
- optimization or array-scale performance.

Table S1 values remain classified as source-reported **fitted** values, not raw measurements.

## Freeze rule

Treat the SI-4 Eq. (S13) implementation and all ten Table S1 entries as the frozen numerical reference for subsequent work. Any change must be a separately reviewed revision with source, rationale, and regression evidence. Do not silently change coefficients, units, normalization, or equation form during optimization.

## Next gate

Proceed separately to physical SOI MZI optical-field reproduction only after the geometry, material stack, wavelength, polarization, boundary conditions, and reference planes are documented with source/assumption labels. Estimate cloud simulation cost before submitting a Tidy3D job.
