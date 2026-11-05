# EIS-CRC-FIRST-PAIRWISE-001 — Analytical Model and Physics Gate

**Status:** model plan / no validated device model  
**Purpose:** determine whether a candidate has a physically meaningful comparison mechanism before requesting FDTD/EM.

## 1. First question: what physical quantity encodes a score?

The abstract contract compares normalized scores. A device model cannot begin until an implementation declares how each score becomes a physical signal. At minimum, specify:

- encoding: optical power, field amplitude, phase, wavelength, time, or a defined combination;
- transfer function from score to signal, including range and monotonicity;
- calibration/reference procedure and drift;
- whether A and B are mutually coherent, incoherent, or time-multiplexed;
- input power range and imbalance;
- how candidate identity is encoded and preserved;
- output reference planes and the physical meaning of a “winner” token.

Do not equate a software score with optical power without an explicit encoding function.

## 2. Architecture-neutral analytical baseline

For a simple monotonic power encoding, write

\[
P_i=P_{\mathrm{off}}+K_s s_i+\delta P_i,\qquad i\in\{A,B\},
\]

where (s_i\in[0,1]), (K_s\) is the score-to-power scale, (P_{\mathrm{off}}\) is an offset if the encoding requires one, and \(\delta P_i\) collects calibrated encoding error and drift. These are symbols until supported by data; no numerical value is implied.

The ideal reference decision is

\[
\Delta P=P_A-P_B,\qquad
d=\begin{cases}
A\_WINS & \Delta P>\Delta P_{\min},\\
B\_WINS & \Delta P<-\Delta P_{\min},\\
INDETERMINATE & |\Delta P|\leq\Delta P_{\min}.
\end{cases}
\]

\(\Delta P_{\min}\) must be derived from the frozen score gap, encoding scale, noise, and uncertainty. It is not automatically equal to the normalized gap 0.05.

A first-order uncertainty budget should keep separate terms for:
- score-encoding error and calibration drift;
- input power imbalance and source fluctuation;
- optical propagation/coupling loss;
- detector noise for Interface A;
- device threshold uncertainty and hysteresis for a nonlinear optical candidate;
- temperature, wavelength, and fabrication variation;
- uncertainty in the model itself.

For an intensity-detection baseline, if the declared receiver produces a differential estimate \(\widehat{\Delta P}=\Delta P+n\), then the probability of a wrong decision depends on the distribution and variance of (n\), threshold offset, and the decision margin. Do not report a numerical error rate until those distributions are justified. If a Gaussian noise approximation is used, label it as an approximation and validate its regime before using it for a claim.

This baseline is an equation-level model, not a device compact model and not evidence that an optical-only comparator exists.

## 3. Physical limitation that must not be skipped

A passive linear optical network maps input complex fields linearly to output fields. That fact alone does not implement a general score comparison with a robust sign decision and an identity-bearing winner token. Interference can create measurable output differences, but a comparison still needs a defined encoding, observable, decision margin, and mechanism that maps the observable to A_WINS/B_WINS.

For a detector-free B1 claim, the candidate must identify a plausible optical decision mechanism—such as a specified nonlinear/thresholding element or a demonstrably valid coherent encoding and routing scheme—and explain how it:
1. distinguishes both score orderings over the declared envelope;
2. resolves or flags the indifference band;
3. emits a winner-identity token rather than only a scalar metric;
4. recovers and remains stable across repeated comparisons;
5. meets the frozen physical budgets.

A thresholding paper or isolated resonator response is not by itself a complete comparator model. Do not assume a thresholder performs comparison or preserves candidate identity.

## 4. Keep two candidates separate

### Candidate B1 — detector-free optical decision

Required model elements:
- score-to-optical-signal encoding and calibration;
- explicit optical decision mechanism and its transfer curve;
- propagation, coupling, insertion loss and output contrast;
- threshold/hysteresis and recovery dynamics where applicable;
- noise and parameter variation;
- winner-token generation and separability;
- energy accounting including optical source and control/bias/regeneration elements inside the boundary.

**Current status:** BLOCKED. The repository has not established the score encoding, optical decision mechanism, or a validated transfer model.

### Candidate A — analog optoelectronic baseline

Required model elements:
- same score encoding and input envelope as B1 where fair comparison is possible;
- photodetector responsivity and bandwidth/noise;
- transimpedance/analog comparison transfer and threshold;
- winner-token generation and output interface;
- detector, amplifier, bias, and optical-source energy;
- latency, recovery, calibration, and output fanout.

This is a distinct architecture and must not be described as all-optical. It can provide a practical baseline for deciding whether the extra complexity of B1 is justified.

## 5. Evidence hierarchy and model construction

Build the first model in this order:

1. **Symbolic feasibility model:** equations and explicit assumptions only; prove input/output mapping and identity preservation at the abstract level.
2. **Parameter ledger:** each parameter gets a value or interval, units, provenance, source/rationale, and uncertainty. Unknown parameters stay unknown; synthetic values are sensitivity probes only.
3. **Bounded sensitivity sweep:** use a small transparent script to test whether any candidate could meet the contract across declared intervals. Do not optimize to a candidate result before the acceptance contract is frozen.
4. **Independent review:** check dimensional consistency, reference planes, energy boundary, signal encoding and whether the assumed nonlinearity/decision behavior is actually supported.
5. **Simulation authorization:** only if the analytical model is physically interpretable, the required inputs have sources or bounded uncertainty, and the v1 physical budgets in `acceptance_criteria_v1.md` have been completed.
6. **Targeted FDTD/EM:** simulate only the unresolved electromagnetic question (for example, a specific coupler or resonator transfer curve). Do not ask FDTD to validate an entire comparator architecture whose decision mechanism has not been specified.

A parameter reported in a paper is not automatically transferable across geometry, process, wavelength, bias, or operating conditions. A simulated transfer curve remains simulated until validated against relevant measurements.

## 6. Energy and latency boundary

At minimum, report separately:
- optical source energy attributable to one comparison;
- encoding/modulation energy;
- phase/bias/thermal-control energy, if used;
- nonlinear element bias or regeneration energy, if used;
- detection, amplification, and decision energy for Interface A;
- calibration and control overhead, amortized only with an explicit duty cycle;
- output-token generation and any required conversion.

Use

\[
E_{\mathrm{comparison}}=\sum_j E_j
\]

only after each included term, reference boundary, activity factor, and amortization rule is declared. An optical-core-only figure must never be presented as end-to-end comparator energy.

Latency must likewise identify whether it includes encoding, optical propagation, threshold/regeneration, recovery, and output-token availability. Report steady-state throughput separately from single-decision latency.

## 7. No-go criteria for FDTD/EM spend

Do **not** start candidate-specific FDTD/EM if any of these remains true:

- score-to-signal encoding is unspecified;
- the proposed optical decision mechanism is only a label or analogy;
- winner identity is not represented at the output;
- the model uses unsupported “typical” device values without uncertainty bounds;
- energy/latency reference boundaries are ambiguous;
- Section 4 of the frozen criteria has no approved numerical budgets;
- no named question exists that an EM simulation can answer.

When blocked, the next experiment is analytical: define and review the encoding and decision mechanism, then build the parameter ledger. Do not spend simulation credits to discover what the contract or architecture has not yet defined.

## Current determination

**FDTD/EM: NOT AUTHORIZED.** The next valid engineering deliverable is a candidate-specific, source-backed analytical model and completed physical-budget approval—not a mesh, cascade, or layout.
