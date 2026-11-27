# EIS-FAB-REF-TIAN-001 — Tian KKA / SOI Reference Evidence Assessment

**Parent specification:** [EIS-FAB-REQ-001](../EIS-FAB-REQ-001.md)  
**Status:** Source-led assessment; open issues remain  
**Reference:** Tian et al., *Photonic Transformer Chip: Interference Is All You Need*, PhotoniX 6, 45 (2025), [DOI 10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).  
**Supporting Information:** [Publisher-hosted SI PDF](https://static-content.springer.com/esm/art:10.1186%2Fs43074-025-00182-7/MediaObjects/43074_2025_182_MOESM1_ESM.pdf).

## 1. Purpose and scope

This assessment records what the Tian publication is useful for when evaluating EIS-FAB-REQ-001. It does not treat the paper as a complete transferable PDK, nor does it imply that EIS has reproduced the chip or its performance.

Tian is the primary **computational and architecture reference** for EIS's KKA investigation. The publication describes a runtime-programmable optical-interference attention mechanism, a silicon photonic transformer chip, numerical studies, and experimental validation. Its central proposition is that amplitude–phase-coupled optical interference can provide the nonlinearity used in KKA and allow omission of the conventional SoftMax activation in the specified KKA formulation. That is a research result to reproduce and test against matched workloads—not a universal theorem that any attention mechanism can omit SoftMax.

## 2. What the source reports

| Topic | Source-reported evidence | EIS interpretation / limit |
|---|---|---|
| Computational primitive | Interference operation is expressed as (a\square b=|a|^2+|b|^2+2\operatorname{Re}(ab^*)\), with balanced detection used to remove the intensity-superposition terms and expose the cross term. | This is the paper's general KKA interference definition. Keep it distinct from the SI-1 specific quadrature BPD expression. |
| Attention formulation | KKA replaces the conventional MAC-based attention operations with interference operations; paper writes the KKA sequence ((Q^T\square K)\square V). | Exact numerical reproduction must resolve SI-13 pseudocode and any notation/aggregation ambiguities before claiming implementation equivalence. |
| Nonlinearity | The authors attribute useful nonlinear behavior to amplitude–phase coupling and report that this permits omission of SoftMax in KKA. | Reproduce the source's encoding, training procedure, normalization, and workload. Do not generalize beyond the tested formulation. |
| Hardware | Silicon photonic chip with 11 MZI cells. Each MZI has one external and two internal thermal phase shifters. | These are three phase-shifter degrees of freedom per MZI; the six θ variables in SI-1 refer to the two MZIs in the I/W branches, not six heaters per individual MZI. |
| Process | The paper reports fabrication at CUMEC using its CSiP-180AL platform. | This is source-reported process provenance, not an available EIS process recipe or proof of equivalence to another SOI PDK. |
| Phase shifters | 200 µm × 2 µm TiN heaters; 12 Ω/sq sheet resistance; thermal tuning. | Useful reported design datum. It does not establish EIS's heater efficiency, settling time, thermal-crosstalk matrix, or target process compatibility. |
| MZI couplers | The paper reports 1×2 and 2×2 MMIs as nominal 50:50 beam splitters. | Nominal design description is not a measured distribution of splitter ratios or a full complex S-matrix. |
| Control / thermal environment | Separate pads for phase-shifter traces; shared grounds for a column of MZIs; TEC/thermistor feedback stabilizes chip temperature at 25 ± 0.2 °C. | This describes the reported experimental setup. It is not a complete control electronics or thermal-management specification for EIS. |
| Experimental detection | Passive demonstrator uses paired power meters at two grating couplers to probe intensities; authors describe integrated balanced photodiodes as a practical active implementation. | Distinguish demonstrated external optical-power measurement from proposed/integrated balanced photodiode implementation. |
| High-speed test | 5 Gbaud modulated light is injected to emulate high-speed inputs; electrical conversion and eye-diagram observation are described. | This is not evidence that the thermal phase-shifter control/calibration loop operates at 5 GHz. |
| Numerical model | Paper reports a two-head ViT example with input (10\times10), (W_q,W_k,W_v) each (10\times10), and head size (10\times5). | Keep this numerical tensor shape separate from the physical chip's 10-branch demonstration and from an eventual EIS 64×64 tile. |
| Code and data | MNIST and CIFAR-10 datasets are public; numerical data and a public code version are available on reasonable request; SI-13 supplies pseudocode. | SI-13 is not a complete executable training repository. Missing training details must remain open until source data/code or author clarification is obtained. |

Source: publisher article and its Supporting Information. Numerical claims in the paper are not re-measured by EIS merely by being transcribed here.

## 3. SI-1 circuit and reference-plane interpretation

The SI-1 schematic places the laser input field (E_{in}) before the first/upstream MMI. That MMI divides the common input into the two MZI branches conventionally denoted I and W. The ideal SI-1 field equations use (E_{in}/\sqrt{2}) in both branch expressions.

The source equations are:

\[
E_I'=\frac{E_{in}}{\sqrt2}
\cos\left(\frac{\theta_3-\theta_2}{2}+\frac\pi4\right)
e^{i\left(\theta_1+\frac{\theta_3+\theta_2}{2}+\frac\pi4\right)}
\]

\[
E_W'=\frac{E_{in}}{\sqrt2}
\cos\left(\frac{\theta_6-\theta_5}{2}+\frac\pi4\right)
e^{i\left(\theta_4+\frac{\theta_6+\theta_5}{2}+\frac\pi4\right)}
\]

and the SI-1 BPD expression is:

\[
P_{out}=2E_IE_W\sin\left(
\theta_1-\theta_4+\frac{\theta_3+\theta_2}{2}
-\frac{\theta_6+\theta_5}{2}
\right).
\]

Equivalently, with the source's complex fields and signed real amplitudes:

\[
P_{out}=2\operatorname{Im}(E_I'\overline{E_W'}).
\]

This is a **quadrature / imaginary cross-term** for the SI-1 circuit convention. It is not identical, without a phase-coordinate rotation, to the main article's general real cross-term (2\operatorname{Re}(ab^*)). The algebraic bridge is exact:

\[
\operatorname{Im}(E_I'\overline{E_W'})
=\operatorname{Re}((-iE_I')\overline{E_W'}).
\]

That (-i) is an algebraic coordinate rotation; it does not by itself assert that an extra physical phase shifter is present.

The ideal source diagram supports a common pre-split (E_{in}) and nominal equal branch division in the ideal model. It does **not** establish that a fabricated upstream MMI is exactly 50:50. Actual split ratio, loss, phase imbalance, and process variation require measurement or a qualified model.

## 4. What is not specified sufficiently for EIS fabrication

The publication and SI are research references, not a complete process transfer package. The following are not established sufficiently for EIS to fabricate an equivalent device without additional information:

- complete silicon/BOX/cladding/substrate stack and material dispersion data;
- complete foundry design rules, mask layers, process corners, and dimensional distributions;
- all waveguide cross-sections, etch depths, sidewall profiles, bend rules, and transition rules;
- measured complex S-parameters and uncertainty for each MMI, coupler, waveguide, and grating interface;
- measured per-device phase-shifter (V\mapsto\phi), amplitude–phase response, heater resistance distribution, efficiency, thermal time constants, and lifetime;
- full thermal-crosstalk matrix and its dependence on simultaneous operating states;
- detector responsivity, noise, bandwidth, gain/offset, common-mode rejection, and calibration;
- wafer-level yield, process-corner distributions, and reproducible test-structure data;
- full executable training code, all hyperparameters, seeds, exact data-loader order, and all numerical artifacts needed for independent source-faithful reproduction;
- a complete mapping from the SI-1 physical BPD observable to every computational KKA operator and every stage of the model.

The paper's reported CSiP-180AL process details must not be silently transferred to CORNERSTONE Si220, SiEPIC EBeam, GlobalFoundries, or another process.

## 5. EIS reproduction and evidence plan

| Work item | Required activity | Acceptance boundary |
|---|---|---|
| TIAN-COMP-001 | Reproduce the 10×1 source-led computational baseline from the main paper and SI-13. | Source equations, tensor shapes, training/test protocol, and unresolved pseudocode interpretations documented. |
| TIAN-SI1-001 | Implement SI-1 S2/S3/S4 source equations and their complex-field form. | Known-answer tests and explicit reference-plane / phasor / detector convention. |
| TIAN-DEVICE-001 | Build an independent idealized SOI MZI/coupler field model. | Reciprocity, passivity/unitarity where assumptions apply, port mapping, and complex transfer tests. |
| TIAN-MEAS-001 | Define minimum physical test coupon and metrology. | Measured complex field or calibrated equivalent sufficient to estimate amplitude, phase, loss, and drift. |
| TIAN-THERM-001 | Characterize heater response and thermal interaction. | Measured Δφ versus power/control and interaction matrix for stated geometry and conditions. |
| TIAN-KKA-ACC-001 | Compare KKA with a matched electronic attention baseline. | Same workload, model capacity, data split, training/evaluation protocol, quality metric, and declared system energy boundary. |

No task is physically accepted solely because an analytic model or simulation matches a source equation.

## 6. Requirement mapping

| EIS-FAB-REQ-001 IDs | Tian evidence contribution | Status |
|---|---|---|
| FAB-004, FAB-005 | Interference, MZI, MMI and SI-1 circuit description | SOURCE-REPORTED; physical per-device transfer data incomplete |
| FAB-006 | KKA formulation and 11-MZI PTC demonstration | SOURCE-REPORTED; EIS reproduction open |
| FAB-007, FAB-008 | Amplitude–phase coupling and thermal phase shifters | SOURCE-REPORTED / experimentally investigated by paper; full reusable transfer dataset not in public SI |
| FAB-009 | Thermal crosstalk included in authors' fitting discussion | SOURCE-REPORTED; reusable interaction matrix not established |
| FAB-010 | External BPD-style measurement; integrated detector described as practical option | PARTIAL |
| FAB-011, FAB-012, FAB-013 | Grating-coupler, electrical pad, and temperature-control setup described | PARTIAL; not EIS package specification |
| FAB-014, FAB-015 | Calibration and fabrication imperfections discussed | PARTIAL; process distributions and calibration data needed |
| FAB-017 | Source equations and model descriptions | PARTIAL; not a transferable PDK model set |
| FAB-020 | Paper/SI source provenance | SOURCE-REPORTED; EIS artifact-level reproduction remains open |
| FAB-022, FAB-023 | Scaling and energy projections discussed | PROJECTED; EIS matched workload and cost evidence required |

## 7. Questions for authors and the photonic community

1. Can the authors share the public code/data package referenced in the paper, including exact training configuration and numerical arrays?
2. Can the SI-13 KKA weighted-aggregation pseudocode be clarified against the implemented model and main-text equation?
3. Can the authors share measured complex transfer data for representative MMI/MZI cells, with port order, reference planes, wavelength, and calibration procedure?
4. Can the measured heater (V\mapsto\phi) and amplitude–phase-coupling data, including device-to-device variation, be shared in a reusable form?
5. What test structures and metrology were used to separate fabrication imbalance, programming non-ideality, and thermal crosstalk?
6. Which parts of the demonstrated KKA path are essential to the SoftMax-free behavior, and which are implementation choices?
7. What would be the most useful open benchmark for comparing KKA with standard self-attention on the same workload?

## 8. Community contribution opportunities

Useful contributions include source-faithful code reproduction, independent derivations, SI-1 circuit-model verification, measured complex-field datasets, heater/thermal-crosstalk characterization, test-coupon designs, and matched electronic-versus-KKA workload evaluation.

A negative result or unresolved ambiguity is publishable evidence if the method, assumptions, and artifact are recorded.

**EIS position:** Tian is the primary KKA research reference. The EIS goal is to reproduce and extend the computational principle while openly identifying what additional device, process, calibration, and metrology capabilities are needed for an independent implementation.
