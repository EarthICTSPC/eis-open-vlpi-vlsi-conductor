# EIS-KKA-001: KKA Interference Primitive and Validation Contract

**Status:** Proposed engineering work package; KKA-001A reference implementation committed on the working branch. No PhotonForge integration or physical validation is claimed yet.

**Scientific reference:** Tian, Y., Xiang, S., Guo, X. et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025), https://doi.org/10.1186/s43074-025-00182-7.

## Objective

Develop a composable model of the Kramers–Kronig attention (KKA) physical primitive without reducing it prematurely to a conventional fixed-weight matrix-vector multiplier. Separate ideal field-interference mathematics, the calibrated physical transfer function, the attention algorithm, and system-level energy/performance accounting.

## KKA-001A — Mathematical conformance

The reference coupler convention is:

\[
E_1=(A+B)/\sqrt{2},\qquad E_2=(A-B)/\sqrt{2}.
\]

Therefore:

\[
|E_1|^2-|E_2|^2=2\operatorname{Re}(AB^*).
\]

For responsivity \(\mathcal R\) in A/W and field envelopes normalized so \(|A|^2\) and \(|B|^2\) become optical power after applying a declared scale \(P_0\) in watts, the ideal differential current is:

\[
i_{diff}=2\mathcal R P_0\operatorname{Re}(AB^*).
\]

Required analytic tests:

- Equal unit fields and zero relative phase: \(i_{diff}=+2\mathcal R P_0\).
- Equal unit fields and relative phase \(\pi\): \(i_{diff}=-2\mathcal R P_0\).
- Equal unit fields and relative phase \(\pi/2\): \(i_{diff}=0\).
- Randomized complex-field samples: port-power difference agrees with the closed-form cross-term.
- Time integration returns charge \(Q=\int i(t)dt\) in coulombs; average current is \(\bar i=Q/(t_1-t_0)\) in amperes.

The implementation in `experiments/EIS-KKA-001/kka_reference.py` is a dependency-free mathematical reference, not a PhotonForge component or a physical device model.

## KKA-001B — PhotonForge 1.4.7 API proof

Before claiming compatibility, verify in an environment with the exact PhotonForge 1.4.7 package:

1. Package version and import provenance are recorded.
2. The installed `AbstractComponent`, port declarations, `TimeStepper`/`SMatrixTimeStepper`, `setup_state`, `step_single`, registration, and circuit connection APIs are inspected against the 1.4.7 docs/source.
3. A minimal import/API probe is run without launching Tidy3D/FDTD or consuming simulation credits.
4. Any mismatch between this proposed contract and the actual release API is documented before implementation.

Do not assume `add_port`, `PortType.ELECTRICAL`, `register_time_stepper_class`, or the shown stepper signatures exist until the probe confirms them. An `AbstractComponent` port topology alone does not implement time-domain behavior.

## KKA-002 — Physical transfer function

The intensity-dependent logarithmic phase law sometimes proposed for this primitive is **a candidate model only**. It is not accepted as Tian et al.'s physical transfer function without a derivation, a direct source in the paper/supplement, or calibration data tied to a specified device and operating condition.

Represent the field transformation through a replaceable interface:

\[
A=\mathcal F_A(x;\theta,\mathbf p),\qquad B=\mathcal F_B(x;\theta,\mathbf p),
\]

where every parameter in \(\mathbf p\) has documented units, provenance, calibration conditions, and validity range. Distinguish Pockels phase modulation from carrier-mediated amplitude–phase coupling. Do not assign a generic linewidth-enhancement factor to a mechanism for which it is not physically justified.

The ideal linear phase-only model is the control case. Any nonlinear model must be compared against it and report the mechanism it represents and the effects it omits.

## KKA-003 — Attention equivalence

Implement a frozen software reference for the specific KKA operation described in the paper. Use identical inputs and parameter settings for reference and candidate implementations. Pre-register tolerances and task-level acceptance metrics. A nonlinear response curve alone does not demonstrate attention equivalence or replacement of Softmax.

## KKA-004 — Energy and performance

Compare complete inference pipelines at equivalent accepted task quality and operating conditions. Record latency, throughput, rejected/late/history-corrupted outputs, reset/calibration/control energy, laser wall-plug efficiency, optical losses, detector and conversion energy, and any heater or carrier-sweep bias. Use \(E_{useful}=E_{total}/N_{accepted}\) only when \(N_{accepted}>0\); when zero transformations are accepted, the metric is undefined. Failed attempts and their energy remain in \(E_{total}\).

Baselines must be explicitly defined before measurement, including a conventional digital attention pipeline and any claimed photonic alternatives. Simulation results must be labeled separately from physical measurements.

## Execution gates and spending boundary

- KKA-001A is a pure mathematical/software test and requires no PhotonForge license, cloud simulation, or FDTD job.
- KKA-001B is an API/import probe only; no paid electromagnetic simulation is authorized by this work package.
- KKA-002 requires transfer-function provenance before a physical claim is made.
- KKA-003 requires a frozen algorithmic reference and acceptance criteria.
- KKA-004 requires comparable system boundaries and an auditable energy ledger.

**Permitted claim after KKA-001A:** “The ideal real-cross-term interference reference passes analytic conformance tests.”

**Not yet permitted:** “PhotonForge 1.4.7 integration passed,” “Tian's chip was reproduced,” “the primitive replaces Softmax,” or “the design improves energy efficiency.”
