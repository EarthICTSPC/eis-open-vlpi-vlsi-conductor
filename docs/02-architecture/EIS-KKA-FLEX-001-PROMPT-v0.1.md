# EIS-KKA-FLEX-001 — FlexAgent Design-Space Study (Prompt v0.1)

**Status:** Superseded by v0.2; retained as the original review baseline  
**Date:** 16 November 2026

## Context for the agent

You are assisting Earth ICT, SPC (EIS) with a bounded design-space study for a Kramers–Kronig-coupling-based optical nonlinear activation (KKA) computational primitive. The KKA primitive is the complex transfer function of a modulator–interferometer cascade whose control inputs are explicitly identified. Your job is to compare candidate device architectures on a Pareto front, not to produce a single winner, and to populate an evidence-provenance record for every parameter you return.

This assignment is scoped to models and candidate parameters, not to foundry-qualified PDK data. Do not invent foundry-specific geometry, doping, or process parameters. Every numerical value you report must carry one of the tags `measured`, `fitted`, `simulated`, `assumed`, or `foundry-confidential`; the last tag must never appear in any public artifact.

## Candidate implementations

1. **SOI MZI with interferometrically generated amplitude–phase coupling.** External phase shifter (EPS) carries high-speed data; internal phase shifters (IPS-1, IPS-2) set the interference operating point. This is the primary EIS candidate and the match to the 2025 Photonic Transformer Chip structure.
2. **Electrically controlled SOI carrier-based modulator** (depletion or accumulation), as a material-level comparison inside the SOI platform.
3. **SiN–TFLN electro-optic MZI.** Pockels phase shifter inside a low-loss interferometer. This is a comparison platform, not the primary one. A Pockels phase shift does not by itself establish material-level KK coupling; the interferometric amplitude–phase transfer must be characterized, not assumed.
4. **EAM-based material-level Kramers–Kronig implementation**, where a suitable reference model exists. This is the scientific reference for material-level KK, not necessarily the fabrication target.

## Technology inputs (generic, not foundry-qualified)

Use the following starting assumptions. Every value must be tagged `assumed` unless and until EIS supplies a measured or fitted replacement. Do not promote these to `measured` or to a named foundry process.

### SOI primary stack

| Parameter | Starting value | Tag |
|---|---:|---|
| Core Si thickness | 220 nm | assumed |
| Slab thickness | 90 nm | assumed |
| Waveguide width | 500 nm nominal | assumed |
| BOX thickness | 2.0 µm | assumed |
| Top oxide | 1.5 µm | assumed |
| Heater metal | doped Si or W, σ ≈ 0.2 S/µm | assumed |
| RF / routing metal | Al, σ ≈ 38 S/µm, 2.0 µm thick | assumed |
| Phase-shifter type | thermo-optic in one arm (EPS) + two internal (IPS-1, IPS-2) | assumed |

Required in the model: the SOI MZI cell must expose three separate control ports — `EPS` (high-speed data), `IPS_1`, `IPS_2` (quasi-static weight/operating point). Do not collapse them into a single phase parameter.

### SiN–TFLN comparison stack

| Parameter | Starting value | Tag |
|---|---:|---|
| SiN core | low-loss SiN waveguide (AN800-class) | assumed |
| TFLN overlay | thin-film lithium niobate on SiN | assumed |
| Propagation loss target | < 0.5 dB/m | assumed |
| Modulator bandwidth target | > 100 GHz | assumed |
| MZI extinction target | > 35 dB | assumed |

The SiN–TFLN stack is a controlled comparison. Its purpose is to test whether the loss budget and EO bandwidth advantages translate into a better KKA operating characteristic, not to assume they do.

## Required model outputs

For every candidate, produce a complex field transfer (H(V,λ,T,P,t)=A(V,λ,T,P,t)e^{jφ(V,λ,T,P,t)}), and report:

1. Complex field transfer, with amplitude and phase separated.
2. Amplitude response (A).
3. Phase response (φ), referenced to the input optical field phase at the cell input port.
4. Amplitude–phase coupling (κ_A ≡ ∂φ/∂ln A), with convention stated.
5. Optical insertion loss.
6. Optical bandwidth and electrical modulation bandwidth.
7. Electrical drive requirements (voltage, energy per modulation event).
8. Thermal sensitivity and thermal crosstalk estimate.
9. Dynamic response and settling time.
10. Detector-compatible output range.
11. Device parameter sensitivity and uncertainty.
12. Missing-data list identifying parameters needed to replace assumptions with measurements.

All amplitudes use the (e^{+iωt}) phasor convention. Balanced-detection output is (Y=2R,Re(AB^*)) under the 1/√2 coupler convention; if a different splitter normalization is used, report the constant explicitly as `detector_normalization`.

## Objectives — Pareto front, not scalar ranking

Report a Pareto front over:

1. Useful amplitude–phase coupling across the stated operating range (mean and variance of (κ_A)).
2. Optical signal retention (equivalently, 1/insertion loss).
3. Energy per modulation event (fJ/event).
4. Device-to-device reproducibility (define a (σ_κ) metric).
5. Area and scalability (µm² per cell; projected loss and power for a 64×64 array).

## Acceptance constraints

- Convention: (κ_A=∂φ/∂ln A), with (A) field amplitude, and (κ_I=κ_A/2).
- Separation: report `kappa_A_mod`, `kappa_A_cell`, and `kappa_A_cascade` separately.
- Phase reference: all complex amplitudes are referenced to the input-port phase; detector output is invariant under a common phase rotation applied to both arms.
- Polarity: distinguish optical-arm exchange (cross-term unchanged) from electrical polarity reversal (reported sign flipped).
- Operating range: state the interval on which the derivative exists.
- Activation monotonicity: if reporting an activation, use the condition (κ_A(A)>-cot(φ(A)+φ_bias)).
- Detector normalization: report `2R` or `4R` explicitly.

## What not to do

- Do not invent foundry-specific geometry, doping profiles, or process parameters for GlobalFoundries, TSMC, Ligentec, or any named foundry.
- Do not treat an arbitrary MZI transfer curve as proof of material-level Kramers–Kronig coupling.
- Do not treat the Physlib CKM three-mode phase-shift formalization as an optical MZI.
- Do not collapse EPS, IPS-1, and IPS-2 into one control port.
- Do not report a single best device.
- Do not mix (κ_A) and (κ_I) conventions without explicit conversion.
- Do not transfer a `foundry-confidential` value into a public artifact.

## Deliverables

1. Candidate device models, one per architecture, with complex transfer.
2. Parameter and sensitivity tables, with provenance tags.
3. Complex-transfer plots: amplitude and phase vs. drive.
4. KKA operating-range comparison table, including separated coupling quantities.
5. Optical and electrical loss budgets, per candidate and per 64×64 projection.
6. Recommended experimental test structures for a first MPW run.
7. Consolidated missing-data list.
8. Recommendation identifying a promising region of the Pareto front, not a single device.

## Success criterion

Identify the architecture that maximizes useful, stable, reproducible KKA computational performance across the Pareto axes—not the device with the largest isolated modulation coefficient.

## Handoff

Outputs are candidate parameter sets, not qualified data. EIS will run them through the Python reference implementation and Lean4 contract differential tests before promotion. The Lean4 contract is the normative oracle for conventions and composition rules; outputs must be expressed in a form that can be checked against it.

## Study-group convergence checklist

| # | Check | Status in v0.1 |
|---|---|---|
| 1 | (κ_A=∂φ/∂ln A), field amplitude; (κ_I=κ_A/2) | Review required |
| 2 | Separate modulator, cell and cascade coupling | Review required |
| 3 | (e^{+iωt}) phasor convention | Included |
| 4 | Detector polarity and normalization | Review required |
| 5 | SOI primary; SiN–TFLN comparison; EAM reference | Included |
| 6 | Three distinct control ports | Included, EPS implementation unresolved |
| 7 | Provenance tags and confidentiality restriction | Included |
| 8 | Pareto front, no scalar winner | Included |
| 9 | No invented foundry parameters; no arbitrary-MZI/material-KK conflation | Included |
| 10 | Lean4 acceptance oracle | Requires status qualification |
| 11 | Missing-data list | Included |
| 12 | Pareto-region recommendation | Included |
