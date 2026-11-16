# EIS-KKA-FLEX-001 — Study-Group Review and Convergence Record

**Date:** 16 November 2026  
**Disposition:** Consensus on v0.2 direction; v0.1 retained unchanged as the original review baseline.

## Consensus architecture

| Decision | Agreed position |
|---|---|
| Primary architecture | PTC-style SOI MZI with data encoded on EPS |
| Computational coupling | `kappa_A_cell` for the EPS-driven cell transfer |
| Diagnostic coupling | `kappa_A_mod` and `kappa_A_cascade` |
| Cascade rule | Derive from the composed complex transfer; never add coupling coefficients |
| Static controls | IPS-1 and IPS-2 held fixed during the data-drive sweep |
| EPS implementation | High-speed mechanism; explicitly declare integrated or external |
| Detector | 50:50 reference convention, normalization (2R), photodiode imbalance reported |
| Energy | Static control holding power and dynamic data energy reported separately |
| Reproducibility | Declared process-variation model; simulated sensitivity distinguished from measured reproducibility |
| Formal acceptance | Current Lean draft plus separately identified proposed activation tests |
| Drive trajectory | Define (κ_A^{(u)}) along the physical data-drive trajectory |
| MZI identity | Declare topology, phase-shifter placement, selected output port and phase reference |

## Four essential corrections adopted

1. Define the three coupling quantities mathematically and specify their drive variables, fixed controls, reference planes and selected output port.
2. Separate high-speed EPS data modulation from quasi-static IPS control. Thermo-optic phase shifters are not assumed to be the high-speed EPS implementation.
3. Fix the reference 50:50 detector normalization at (2R) for (E_±=(A±B)/√2); report photodiode responsivity mismatch.
4. Replace the incorrect cotangent monotonicity shortcut with the derivative test for the actual activation model. Treat this as a proposed acceptance test until separately formalized and proved.

## Normative drive-trajectory definition

For a physical data-drive variable (u), define:

[
κ_A^{(u)} =
\frac{d\arg H(u)/du}{d\ln|H(u)|/du}
]

where the denominator is nonzero and the derivatives exist. The phase must be consistently unwrapped. The declared operating interval, fixed control settings, reference planes and selected output port are part of the definition.

- `kappa_A_mod`: standalone modulator transfer, swept over its specified data drive when the modulator carries data.
- `kappa_A_cell`: selected cell-port transfer, swept over EPS data drive; IPS-1 and IPS-2 are held at declared operating points.
- `kappa_A_cascade`: complete composed transfer, differentiated with respect to the actual system data-drive variable.

Never add these coefficients. If (H_{cascade}(u)=C H_{mod}(u)) for constant nonzero complex (C), with identical reference conventions, then (κ_{A,cascade}=κ_{A,mod}). If the data is encoded on cell EPS and a preceding modulator is absent or static, the cell/EPS trajectory is the computational trajectory. Any cascade result must nevertheless be calculated from the actual composed transfer.

## MZI and phase-reference requirement

Mandatory fields: `mzi_topology`, `phase_shifter_placement`, `output_port`, `phase_reference`. Derive the complex transfer from the physical topology and chosen reference planes. Do not assume an ideal MZI necessarily has zero interferometric amplitude–phase coupling; do not infer material-level KK from a nonzero cell coefficient.

## Activation acceptance test

For (f(A)=A\cos(φ(A)+θ_n)/\cos θ_n):

[
\frac{df}{dA} =
\frac{\cos(φ+θ_n)-κ_A\sin(φ+θ_n)}{\cos θ_n}>0.
]

Declare a lower bound (|\cos θ_n|\ge ε_θ>0), or explicitly analyze the limiting case. This is a proposed activation acceptance condition, not a theorem currently established by PR #84.

## Additional mandatory additions

- Declare `data_encoding` and `EPS_location: integrated | external`. If external, include the EPS platform, optical reference plane, optical loss and electrical/energy costs in the system boundary.
- Separate static IPS holding power from dynamic EPS energy per data transition. Declare waveform (NRZ/PAM4), symbol rate, swing and integration method.
- Declare a common reference operating point for all candidates. Wavelength 1550 nm and 25 °C are suggested reference coordinates; input power, symbol rate and remaining conditions must be fixed by EIS before comparative Pareto claims. Per-candidate preferred-condition sweeps are additional, not substitutes.
- Define process-variation distributions and sample count for Monte Carlo. Simulated (σ_κ) is model sensitivity, not measured reproducibility.
- Declare PDK name, version, access/license basis and restrictions. Any NDA-derived parameter or result is restricted; never copy, summarize or expose confidential values or derived numerical results in a public artifact.
- Require machine-readable JSON output conforming to the companion schema.
- Preserve the historical distinction between material-level EAM/KK reference work (2023-era context), the 2025 PTC SOI interferometric architecture, and EIS's proposed formalization/measurement program. Do not imply EIS has reproduced either demonstration.
- Report balanced-photodiode responsivity matching, gain mismatch and offsets.

## Formal-contract status qualification

PR #84 is a draft. It formalizes selected conventions and detector properties, but general cascade composition and the activation acceptance condition are not yet established Lean theorems. FlexAgent must identify quantities not covered by the current formal contract. Do not call unformalized rules Lean-verified.

## Disposition

Produce `EIS-KKA-FLEX-001-PROMPT-v0.2.md`, retain v0.1 and this review record, and dispatch only through an authorized FlexCompute channel. Candidate outputs are not qualified data. No foundry-specific geometry or confidential PDK data may be invented or released.
