# EIS-KKA-FLEX-001 — FlexAgent Design-Space Study (Prompt v0.2)

**Owner:** Earth ICT, SPC (EIS)  
**Status:** Dispatch candidate; candidate-model study only  
**Supersedes:** Prompt v0.1 (retained as an archival review baseline)  
**Review record:** EIS-KKA-FLEX-001-STUDY-GROUP-REVIEW-2026-11-16.md  
**Date:** 16 November 2026

## 1. Assignment and scientific framing

Assist Earth ICT, SPC (EIS) with a bounded design-space study of a Kramers–Kronig-coupling-based optical nonlinear activation (KKA) computational primitive. The EIS computational primitive is the **complex transfer of a physically specified, data-driven modulator–interferometer cell or cascade**. The study must distinguish:

1. material-level amplitude–phase coupling in a modulator;
2. amplitude–phase behaviour produced by interferometric composition; and
3. the complete data-driven computational transfer actually presented to the detector.

Do not attribute an observed response to material-level Kramers–Kronig coupling merely because a cell or cascade has nonzero amplitude–phase coupling.

Preserve the scientific/historical distinction: (a) 2023-era EAM/material-level KK work as a scientific reference; (b) the 2025 Photonic Transformer Chip (PTC) SOI interferometric architecture and its data/control arrangement; and (c) EIS's proposed formalization, characterization and measurement program. Do not imply that EIS has reproduced either published demonstration. Do not conflate a reported high-speed data modulation path with high-speed thermo-optic phase control.

This assignment is for models and candidate parameter sets, not foundry-qualified PDK data. Do not invent foundry-specific geometry, doping, process corners or measured performance. Numerical values must carry provenance. Permitted provenance labels are **measured**, **fitted**, **simulated**, **assumed**, and **foundry-confidential**. Confidentiality is an independent release restriction: never copy, quote, summarize, export or publish a confidential value or derived numerical result.

## 2. Mandatory architecture declaration — complete before comparative optimization

The primary EIS hypothesis is a PTC-style SOI MZI with data encoded on EPS and IPS-1/IPS-2 held quasi-static during the data sweep. This is the study priority, not a claim that the architecture has already won.

Every candidate model must declare:

~~~yaml
architecture:
  data_encoding: EPS | pre_modulator | other
  data_drive_variable: <physical variable and unit>
  EPS_location: integrated | external
  EPS_function: high_speed_data_modulation
  IPS_1_function: quasi_static_operating_point
  IPS_2_function: quasi_static_operating_point
  computational_primitive: <named physical transfer boundary>
  computational_kappa: kappa_A_cell | kappa_A_mod | kappa_A_cascade
  mzi_topology: <explicit topology and port convention>
  phase_shifter_placement: <physical placement and driven arm(s)>
  output_port: <selected output port>
  phase_reference: <input optical phase reference plane>
  reference_planes: <all input/output planes>
~~~

Do not begin Pareto optimization until data_encoding, data_drive_variable, EPS_location, mzi_topology, phase_shifter_placement, output_port and phase_reference are declared for the candidate.

For the primary PTC-style hypothesis, use EPS as the data-bearing drive and hold IPS-1 and IPS-2 at specified operating points during the data sweep. Sweep IPS-1 and IPS-2 separately for calibration and operating-point maps. Do not collapse EPS, IPS-1 and IPS-2 into one abstract phase variable.

EPS must be a high-speed electrical/optical mechanism appropriate to the declared symbol rate. Thermo-optic control may be evaluated for quasi-static IPS ports; do not assume it is a viable high-speed EPS. Declare whether EPS is integrated or external. If external, identify its platform and include its optical/electrical interface, insertion loss, drive energy and packaging/interface assumptions in the system boundary. In that case distinguish the SOI MZI/IPS platform from the complete hybrid computational primitive.

## 3. Candidate implementations

Compare all four architectures; do not assume KKA compatibility by construction.

1. **SOI MZI with interferometrically generated amplitude–phase behaviour.** Primary EIS candidate. Data on EPS; IPS-1 and IPS-2 quasi-static. Derive the selected-port complex transfer from the declared physical topology and phase-shifter placement.
2. **Electrically controlled SOI carrier-based modulator** (e.g. depletion or accumulation), as a material-level/platform comparison. Distinguish absorption and refractive-index response; do not infer a useful coefficient without complex-transfer evidence.
3. **SiN–TFLN electro-optic MZI**, as a controlled comparison. Pockels phase control does not by itself establish material-level KK coupling. Characterize the interferometric transfer rather than assuming it.
4. **EAM-based material-level KK implementation**, where a suitable reference model and evidence exist. This is the scientific material-level reference, not necessarily the fabrication target.

For each architecture identify whether its data-bearing element is integrated or external and define the complete data path. A standalone modulator model is not a substitute for the actual computational primitive.

## 4. Generic technology inputs — assumptions only

The following SOI values are generic starting assumptions, not GlobalFoundries, TSMC, AIM, Ligentec or other foundry specifications. Use only as sensitivity-study placeholders unless EIS provides authorized process data.

| Parameter | Starting value | Provenance |
|---|---:|---|
| Silicon device/core thickness | 220 nm | assumed |
| Slab thickness | 90 nm | assumed |
| Waveguide width | 500 nm nominal | assumed |
| BOX thickness | 2.0 µm | assumed |
| Top oxide | 1.5 µm | assumed |
| Heater material | evaluate doped Si and W separately | assumed alternatives |
| Heater conductivity | do not assign one shared value to doped Si and W; parameterize each with source/temperature | assumed until sourced |
| RF/routing metal | Al, 2.0 µm thickness as a placeholder | assumed |
| RF metal conductivity | 38 S/µm only as an explicit placeholder with temperature/source | assumed |
| EPS mechanism | high-speed mechanism to be characterized; carrier-depletion is a candidate, not a foundry assertion | assumed |
| IPS mechanisms | thermo-optic or other quasi-static mechanisms to be compared | assumed |

For SiN–TFLN, use generic placeholders only. The following are targets/assumptions, not guaranteed properties: AN800-class SiN family; thin-film lithium niobate overlay; propagation-loss target <0.5 dB/m; EO bandwidth target >100 GHz; MZI extinction target >35 dB. Verify units and operating conditions before use. Do not silently change dB/m to dB/cm. Tag every such number **assumed** until sourced or measured.

For every PDK-derived parameter declare PDK/provider, PDK version or commit, access/license basis, permitted use, export/release classification and whether any derived result is restricted. If an NDA or restricted PDK is involved, do not put its numerical values or derived results in public output. If permission is unclear, stop using that source and report only a non-sensitive restricted-input notice.

## 5. Coupling convention and drive-trajectory definitions

Freeze the EIS convention:

\[
\kappa_A \equiv \frac{d\phi}{d\ln A}, \qquad
A=|H| \text{ is field-amplitude transmission},
\]
\[
\kappa_I=\frac{1}{2}\kappa_A.
\]

The second relation is the intensity-coordinate conversion. Do not mix conventions in one table without explicit conversion. If a source uses another normalization (including a factor of two), retain the source convention under a separately named field and convert to EIS kappa_A.

For a physical data-drive variable \(u\), define the drive-trajectory coupling:

\[
\boxed{
\kappa_A^{(u)}
=
\frac{d\arg H(u)/du}{d\ln|H(u)|/du}
}
\]

where both derivatives exist and \(d\ln|H(u)|/du\ne0\). This is the experimentally explicit form of \(d\phi/d\ln A\). Declare the physical variable, units, sweep direction, fixed controls, reference planes and selected output port.

**Formal bridge to PR #84:** the current Lean predicate **KappaAAdmissibleOnRange** is defined for a real-valued phase response **phaseLogA : ℝ → ℝ** in the coordinate \(x=\ln A\), and requires pointwise differentiability at \(x\) plus membership in the declared OperatingRange. It does **not** by itself formalize the drive variable \(u\), the nonzero trajectory denominator, phase unwrapping, an injective inverse \(u(x)\), or a composed cascade. FlexAgent must report these trajectory conditions separately and must not claim they are already covered by that Lean predicate.

Where \(x(u)=\ln|H(u)|\) is differentiable and locally one-to-one on the declared interval, construct the unwrapped phase response \(\phi_{\log A}(x)=\arg H(u(x))\). Then verify by the chain rule that

\[
\frac{d\arg H(u)/du}{d\ln|H(u)|/du}
=
\frac{d\phi_{\log A}}{dx}.
\]

This is the bridge to the Lean **kappaA** definition. If \(x(u)\) is not one-to-one or phase is not a single-valued function of \(x\) on the interval, split the trajectory into admissible injective subintervals or report that it cannot be represented by the current scalar phaseLogA contract. Do not silently force a single-valued fit.

Report these three quantities separately:

| Field | Transfer function | Drive variable | Controls held fixed |
|---|---|---|---|
| **kappa_A_mod** | Standalone modulator \(H_{mod}\) | Declared modulator data drive when that modulator carries data | All non-data modulator biases and downstream controls |
| **kappa_A_cell** | Selected-port cell transfer \(H_{cell}\) | EPS data drive \(u_{EPS}\) for the primary PTC-style candidate | IPS-1, IPS-2 and other calibration controls |
| **kappa_A_cascade** | Complete composed transfer \(H_{cascade}\) | Actual system data-drive variable | All non-data controls at declared operating points |

The **computational kappa_A** is the coupling along the data-bearing trajectory of the declared computational primitive. For the primary PTC-style candidate with data on EPS, this is **kappa_A_cell**. If data is encoded on a pre-modulator instead, the modulator trajectory may be computational. If the complete cascade is the declared primitive, compute its coefficient from the complete composed transfer with respect to the actual data drive.

Never add the coefficients. Compute cascade coupling from the composed complex transfer. In the special case \(H_{cascade}(u)=C H_{mod}(u)\), where \(C\) is constant and nonzero over the sweep and conventions/reference planes are consistent, then \(\kappa_{A,cascade}=\kappa_{A,mod}\). This equality does not apply if the downstream cell depends on \(u\), if controls co-vary, or if the reference-plane/port definitions differ.

Do not infer that an ideal MZI has zero or nonzero coupling from a factored matrix representation alone. Derive \(H(u)\) for the declared physical topology, phase-shifter placement, input state, selected output port and phase reference. A global phase factor and an internal phase parameter cannot be reassigned casually if doing so changes the declared physical reference. Report the full complex transfer and enough topology detail to reproduce it.

## 6. Derivative admissibility and operating range

A reported \(\kappa_A^{(u)}\) is admissible only when:

- \(H(u)\ne0\) throughout the declared interval and \(|H|\) is not in a flagged near-zero region;
- \(d\arg H/du\) and \(d\ln|H|/du\) exist under the declared model;
- \(d\ln|H|/du\ne0\) on the interval used for the ratio;
- phase is unwrapped consistently before numerical differentiation;
- the interval, units, sweep direction, derivative method, step size or fit model, and uncertainty are stated;
- numerical conditioning and sensitivity to step size/fit window are reported.

Flag exact zeros, near-zeros, phase branch changes, non-differentiable points and ill-conditioned regions. Do not present a large coefficient near an extinction null as useful coupling. If the denominator crosses or approaches zero, split the operating range or mark the coefficient inadmissible; do not conceal singularities by smoothing.

The current PR #84 **KappaAAdmissibleOnRange** predicate only covers pointwise differentiability of phase as a function of log field amplitude within an operating range. It does not establish the drive-trajectory denominator, local invertibility or phase-unwrapping conditions above. Treat those as additional checks until separately formalized.

## 7. Complex transfer, detector and required outputs

For every candidate produce a complex field transfer \(H(u,\lambda,T,P,t)=A e^{j\phi}\) with:

1. complex transfer and separate field amplitude and phase;
2. phase referenced to the declared input optical phase at the cell/cascade input plane;
3. **kappa_A_mod**, **kappa_A_cell**, **kappa_A_cascade** and the identified computational coefficient;
4. optical insertion loss and signal retention;
5. optical bandwidth and electrical modulation bandwidth;
6. electrical drive voltage/current and dynamic energy;
7. static holding/control power, especially for IPS;
8. thermal sensitivity and thermal crosstalk;
9. dynamic response, rise/fall time and settling time;
10. detector-compatible output range and saturation/headroom;
11. parameter sensitivities, uncertainty and numerical conditioning;
12. declared operating range and missing-data list.

Use the positive-time phasor convention \(E(t)=\operatorname{Re}(\tilde E e^{+j\omega t})\).

For the reference 50:50 coupler convention:

\[
E_+=\frac{A+B}{\sqrt2},\qquad E_-=\frac{A-B}{\sqrt2},
\]
\[
Y=I_+-I_-=R(|E_+|^2-|E_-|^2)=2R\operatorname{Re}(AB^*).
\]

The reference detector normalization is **2R**, not an interchangeable 2R/4R choice. Any alternative splitter convention must be derived from its complete field and detector definitions and converted to the EIS reference convention before comparison.

Report photodiode responsivity matching, measured or assumed responsivity mismatch, gain mismatch, offsets, bandwidth and saturation. For unequal responsivities \(R_+\) and \(R_-\), explicitly model the common-mode leakage/offset; do not represent the result solely by the ideal \(2R\operatorname{Re}(AB^*)\) cross-term. Distinguish optical-arm exchange (cross-term unchanged under the defined exchange) from electrical polarity reversal (reported sign changes). Demonstrate invariance under a common phase rotation of both arms.

## 8. Activation model and proposed monotonicity test

If an activation is reported, identify its exact equation and parameters. For the reference activation:

\[
f(A)=\frac{A\cos(\phi(A)+\theta_n)}{\cos\theta_n},
\]

the derivative test is:

\[
\boxed{
\frac{df}{dA}
=
\frac{\cos(\phi+\theta_n)-\kappa_A\sin(\phi+\theta_n)}
{\cos\theta_n}>0
}
\]

over the declared interval. Do not replace this with a cotangent inequality unless all sign/domain assumptions are proved and stated. Declare a positive bound \(|\cos\theta_n|\ge\epsilon_\theta>0\), including the value and provenance of \(\epsilon_\theta\), or explicitly analyze the limiting case. Flag any interval that fails the derivative test.

This is a **proposed activation acceptance test**. Do not claim it is already a Lean theorem or part of the current PR #84 contract.

## 9. Common reference operating point

Before comparative Pareto claims, EIS must declare a common reference operating point applied to all candidates:

- wavelength;
- ambient/device temperature;
- optical input power and polarization;
- data symbol rate and modulation waveform;
- electrical drive swing and bias;
- IPS operating point and control state;
- selected input/output ports and detector configuration.

Use 1550 nm and 25 °C as proposed reference coordinates only if EIS confirms them for this comparison. Input power, symbol rate and waveform must be explicitly fixed by EIS before final cross-candidate ranking. If any reference coordinate remains unset, report normalized or provisional results and clearly withhold a definitive cross-candidate Pareto ranking. Also provide per-candidate operating-range sweeps; do not compare only each candidate's individually optimized point.

## 10. Energy accounting

Report at least two separate energy/power quantities:

1. **Static control holding power:** IPS-1/IPS-2 and other continuously biased or thermal controls, in W (and energy over a stated duty interval where useful).
2. **Dynamic data energy:** EPS energy per transition/symbol in fJ/event, with waveform (NRZ/PAM4 or other), symbol rate, voltage swing, load, termination and measurement/integration boundary declared.

Where appropriate, calculate energy from \(\int V(t)I(t)\,dt\) over a declared event/window. A \(CV^2/4\) NRZ estimate may be included only with its circuit/transition assumptions. Do not compare thermal holding power with a per-event energy as if they were the same metric. Include laser, driver, detector, control, calibration and conversion overhead when included in the stated system boundary.

## 11. Pareto objectives — no scalar winner

Report a Pareto set/front, not a single scalar score. Include at least:

1. useful \(\kappa_A\) across the admissible operating range: signed mean, mean absolute value, variance, range width and fraction of range passing the proposed activation test;
2. optical signal retention/insertion loss;
3. dynamic EPS energy per data event and static IPS/control holding power as separate axes;
4. process-variation sensitivity, including \(\sigma_\kappa\) under an explicitly declared model;
5. cell area and scalability.

Do not reward a large isolated coefficient near a null, an extremely narrow operating interval, a sign-changing response that fails the activation criterion, or a candidate whose energy/loss/reproducibility trade-offs are unacceptable. Report the trade-offs and uncertainty rather than inventing a universal weighting.

## 12. Process variation and reproducibility

For simulated process sensitivity, declare each varied parameter, distribution, correlation, range, source/provenance, sample count \(N\), random seed and convergence check. Candidate variables may include waveguide width/thickness, slab thickness, doping, etch bias, heater resistance and coupler imbalance, but use only justified generic assumptions or authorized process data.

Report simulated \(\sigma_\kappa\) as **modelled process sensitivity**, not measured device-to-device reproducibility. A single nominal simulation cannot establish reproducibility. Identify the test population and measurements required to establish measured device-to-device variation. Do not invent foundry process distributions.

## 13. 64×64 projection boundary

A 64×64 projection must declare its topology, routing and system boundary. Account for, or explicitly mark missing:

- waveguide/interconnect propagation loss;
- splitter/combiner and crossing loss;
- detector responsivity, noise, bandwidth and saturation;
- laser/input optical power and distribution;
- electrical EPS drive and IPS holding power;
- thermal crosstalk and control;
- calibration, monitoring and reconfiguration;
- packaging, coupling and optical/electrical conversion;
- yield assumptions and process variation.

Do not extrapolate a single-cell result to array performance without these assumptions. If inputs are missing, provide bounded/provisional estimates and a missing-data record, not a confident system-level claim.

## 14. Mandatory provenance and confidentiality

Every numerical parameter/result must have a machine-readable provenance record containing at minimum:

~~~json
{
  "parameter": "waveguide_width",
  "value": 500,
  "unit": "nm",
  "provenance": "assumed",
  "source": "EIS-KKA-FLEX-001-v0.2",
  "valid_range": null,
  "uncertainty": null,
  "conditions": {
    "wavelength_nm": null,
    "temperature_C": null,
    "bias_V": null,
    "symbol_rate_Hz": null
  },
  "tool": null,
  "tool_version": null,
  "model_configuration": null,
  "pdk": {
    "name": null,
    "version": null,
    "license_basis": null,
    "restriction": "public | restricted | unknown"
  },
  "notes": "Generic placeholder; not foundry-qualified"
}
~~~

Use provenance labels exactly: **measured**, **fitted**, **simulated**, **assumed**, **foundry-confidential**. Do not upgrade provenance without evidence. For fitted values, include fitting method and dataset identifier. For simulated values, include tool/version, model settings and input provenance. For measured values, include instrument/calibration, method, conditions, uncertainty and data identifier.

Declare all PDK sources and licenses. If any PDK-derived value or result is NDA-restricted, keep it out of public output, including derived numerical results. If the release classification is unknown, stop and request EIS clarification; do not export it.

## 15. Required deliverables

1. One reproducible candidate model per architecture, with complex transfer and declared topology/reference planes.
2. Parameter/sensitivity tables with provenance for every numerical value.
3. Complex-transfer plots (amplitude and unwrapped phase versus the physical data drive), plus IPS calibration sweeps.
4. Operating-range table with all three coupling quantities, computational coefficient, admissibility and uncertainty.
5. Detector model and balance/mismatch report.
6. Optical and electrical loss/energy budgets, including separate static and dynamic energy.
7. Provisional 64×64 model with explicit topology/system boundary and missing inputs.
8. Monte Carlo/process-variation report with distributions, sample count and convergence evidence.
9. Recommended experimental test structures: standalone data modulators, EPS-driven MZI cells, IPS calibration structures, phase-error structures, thermal-crosstalk structures, detector matching structures and monitor/reference structures.
10. Consolidated missing-data list.
11. Pareto front/set with trade-offs; recommendation as a **region of the Pareto front**, not one device.
12. Machine-readable **flex001-results.json** conforming to **EIS-KKA-FLEX-001-results.schema.json**, alongside human-readable reports.

## 16. Formal/software handoff and acceptance boundary

The current EIS-KKA-FORMAL-001 Lean4 work in PR #84 is a draft. It defines selected conventions, response records and detector properties, but does not yet establish a general cascade-composition theorem or the activation monotonicity condition. Its **KappaAAdmissibleOnRange** predicate is defined for a phase response in log-field-amplitude coordinates and requires pointwise differentiability and membership in the declared range. It does not itself establish drive-trajectory invertibility, a nonzero drive-to-log-amplitude derivative, phase unwrapping or complete cascade composition. Do not claim otherwise.

EIS will independently check candidate outputs against the Python reference implementation and the validated Lean contract as those components become available. Candidate parameter sets are not qualified measurements, foundry sign-off, or proof of system performance. The Lean contract is normative only for properties actually formalized and validated; all other requirements must be marked proposed or pending.

## 17. What you must not do

- Do not invent foundry-specific geometry, doping, process distributions or performance.
- Do not assume a generic MZI response proves material-level KK.
- Do not assume a factored MZI matrix settles the physical phase reference or output-port transfer.
- Do not collapse EPS, IPS-1 and IPS-2.
- Do not assume thermo-optic control is the high-speed data path.
- Do not add kappa_A_mod, kappa_A_cell and kappa_A_cascade.
- Do not treat 2R and 4R as interchangeable under the declared reference convention.
- Do not mix static holding power and dynamic event energy.
- Do not claim simulated process sensitivity is measured reproducibility.
- Do not publish or transmit confidential PDK values or derived numerical results.
- Do not report one scalar winner or overstate a projected 64×64 result.

## 18. Success criterion

Identify candidate architecture regions that provide useful, stable, reproducible **data-driven complex transfer** for the declared computational primitive under realistic optical, electrical, thermal, detector, calibration and process-variation constraints. The objective is not maximum isolated chirp; it is useful computational behaviour over a declared operating range with a defensible system energy/loss/reproducibility budget.

## 19. Dispatch checklist

Before running the study, confirm:

- [ ] Architecture declaration and data-encoding location are complete.
- [ ] EPS location (integrated/external) and system boundary are complete.
- [ ] Physical MZI topology, phase-shifter placement, output port and phase reference are declared.
- [ ] Data-drive variable, units, sweep, fixed IPS settings and reference planes are declared.
- [ ] Common reference operating point is complete, or comparative Pareto claims are explicitly provisional.
- [ ] PDK/license/release declarations are complete.
- [ ] FlexAgent has access only to permitted inputs.
- [ ] Output JSON schema is accepted and public/restricted outputs are separated.
