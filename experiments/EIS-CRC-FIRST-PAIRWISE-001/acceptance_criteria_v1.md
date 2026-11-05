# EIS-CRC-FIRST-PAIRWISE-001 — Frozen Screening Criteria v1

**Status:** frozen for model-level screening; physical-performance gate remains BLOCKED  
**Version:** EIS-CRC-FIRST-PAIRWISE-001-AC-v1  
**Applies to:** pairwise comparator only; not a top-k cascade or K/V router  
**Freeze rule:** these criteria must not be changed after candidate outputs are inspected. Any change requires a new version, rationale, and rerun.

## 1. Input and decision contract (frozen)

1. The software reference domain is normalized scores (s_A,s_B\in[0,1]). This is a test convention, not a claim that PRISM scores are already optical powers.
2. The v1 synthetic indifference gap is \(g_{min}=0.05\) normalized score units.
3. If \(s_A-s_B>0.05\), expected output is `A_WINS`; if \(s_B-s_A>0.05\), expected output is `B_WINS`.
4. If \(|s_A-s_B|\leq0.05\), expected output is `INDETERMINATE`. Do not break ties by arbitrary candidate ordering.
5. Non-finite inputs, out-of-domain scores, invalid calibration, or operation outside the declared envelope must produce `FAULT` or a declared `INDETERMINATE`; they must not silently produce a winner.
6. Winner identity is part of the output contract. A scalar “difference” without a recoverable A/B identity token does not pass.

**Scope note:** the 0.05 gap is a preregistered synthetic screening value chosen to exercise the contract. It is not derived from a PRISM workload distribution and must not be presented as an application requirement. A workload-derived gap may be introduced only as a new version before inspecting candidate outputs.

## 2. Behavioral-model correctness gate (frozen)

- Use at least 3,000 deterministic, preregistered test vectors per candidate model, including both orderings, values just outside and inside the gap, equal scores, boundary scores 0 and 1, input imbalance, and declared noise/variation corners.
- For cases outside the indifference band, require **zero false-winner decisions** in the 3,000-vector screening set.
- Within the band, require no forced winner; the result must be `INDETERMINATE` or `FAULT` according to the declared operating-envelope policy.
- Report the full confusion matrix, indeterminate rate, fault rate, and every excluded vector with its exclusion reason.
- Zero observed false winners in 3,000 trials is a finite screening result, not proof of zero error probability or a universal reliability claim.

## 3. Physical-boundary and evidence gate (frozen)

- Declare the score-to-physical-signal mapping, calibration procedure, input range, reference plane, and candidate-identity encoding before simulating.
- Every numeric parameter must be tagged `MEASURED`, `PAPER_REPORTED`, `SIMULATED`, `MOCKED_FOR_EXPLORATION`, or `UNKNOWN`, with a source or rationale.
- A B1 “optical” result requires the comparison decision and winner-identity token to remain optical through the declared output boundary. Any photodetection/electronic decision inside that boundary classifies the implementation as `analog_optoelectronic` or `electronic`, not B1.
- A behavioral reference or ideal transfer function cannot establish physical validation.
- A result without a calibrated signal/noise model and explicit energy boundary is `INCOMPLETE`, not PASS.

## 4. Physical performance thresholds: intentionally not fabricated

The existing repository and identified references do not establish workload-approved numerical limits for optical contrast, insertion loss, latency/recovery, energy per comparison, or variation. Those values therefore remain **UNSET / BLOCKING** rather than being filled with arbitrary numbers.

Before any candidate-specific FDTD/EM spend, EIS must freeze these values from a declared workload and system boundary:
- minimum usable winner-token contrast/separability;
- maximum allowed insertion loss;
- maximum decision latency and recovery time;
- maximum energy per comparison, including source, encoding/modulation, phase control or bias, any regeneration, and the complete declared receiver/selection boundary;
- allowed fabrication, temperature, wavelength, input-power and noise envelope;
- required yield/confidence treatment and calibration overhead.

The budgets must identify the workload requirement, measurement reference planes, included/excluded components, and owner approval. If they are not set, status remains `BLOCKED_PHYSICAL_BUDGET`; do not spend on FDTD/EM.

## 5. Frozen go/no-go sequence

1. **Software contract:** validate input-domain and decision semantics.
2. **Analytical feasibility:** establish a candidate-specific signal/decision mechanism and bounded parameter model using provenance-labelled values.
3. **CRC-FIRST screen:** reject candidates analytically when the contract is impossible under the declared bounds; retain equations, assumptions and rejection trace.
4. **Pre-simulation review:** verify all Section 4 budgets are frozen and candidate parameters have defensible sources or explicit uncertainty bounds.
5. **Only then:** authorize the smallest targeted physics simulation that resolves a named uncertainty. Simulation is not physical validation.

Any change to Sections 1–3 after candidate output inspection requires a new criteria version. Section 4 must be completed before the first candidate-specific FDTD/EM run.

## 6. Current status

- Functional screening criteria: **FROZEN v1**.
- Application-derived physical budgets: **UNSET**.
- Defensible candidate-specific device model: **NOT ESTABLISHED**.
- FDTD/EM authorization: **NO-GO**.
