# EIS-TIAN-KKA-LIFT-001A — Calibration Contract v0.1.0

**Status:** Source snapshot frozen; EIS interpretation gates open  
**Normative source:** Tian et al. (2025), Supplementary Information SI-3 and SI-4, especially Eqs. (S11)–(S13), Fig. S6–S8 and Table S1.

## 1. Contract purpose

This contract preserves the calibration procedure and fitted response model reported for Tian's PTC prototype. It establishes the reference that EIS must faithfully reproduce before proposing a new KKA optimization.

It is not a GF PDK specification, not an EIS measurement, and not a complete complex optical transfer model.

## 2. SI-3: individual thermo-optic heater characterization

Tian reports 11 MZIs with thermo-optic integrated heaters. The reported waveguide cross-section is 450 nm × 220 nm. The TiN heater is reported as 200 µm long, 2 µm wide and 120 nm thick; measured heater resistances are around 1 kΩ.

The reported characterization applies a one-at-a-time voltage sweep from 0 V to 7 V in 5 mV increments and records optical power-meter output. Figure S6 shows 20 exemplary heater responses.

The fitted observable is:

\[
y(V)=a\cos\left(\frac{bV^2}{R}+c\right)+d
\tag{S11}
\]

The voltage-to-phase relation is described as:

\[
\phi(V)=\frac{bV^2}{R}+c
\]

The source's coefficient units and full measurement normalization must be retained from the original experimental context; this contract does not invent them.

SI-3 gives a phase-error expression:

\[
\Delta y \approx \frac{\Delta\phi^2}{2}a\cos\phi
-\Delta\phi\,a\sin\phi
\tag{S12}
\]

and reports \(\mu=0.0017\) and a second statistic \(0.0295\), described in the text as variance \(\sigma\). The same supplement relates \(\sigma\) to a 7.73-bit estimate. Because variance and standard-deviation usage are not internally unambiguous, EIS must preserve the quoted values and **must not use the derived bit estimate as a calibrated acceptance limit** until the source meaning and units are resolved.

The supplement describes typical phase-shifting efficiency as approximately 20 mW. Since the source uses a power unit while calling it efficiency, EIS must not silently reinterpret it as \(P_\pi\) or as a process-independent value.

## 3. SI-4: pairwise KKA interference calibration

The calibration configuration considers the KKA operation induced by an internal phase control in MZI-B, while each MZI-A_i is modulated through its external phase control. Ten A_i/B_i groups are reported.

The preliminary pair model is:

\[
A_i \Omega B_i \propto
\cos(aV_B^2+b)
\cos(cV_A^2-aV_B^2+d)
\tag{S12}
\]

The source then corrects this model to account for unequal phase-shift efficiencies caused by nonlocal thermal effects:

\[
\boxed{
A_i \Omega B_i \propto
\cos(a_1V_B^2+b)
\cos(c_iV_A^2-a_2V_B^2+d_i)+e_i
}
\tag{S13}
\]

This corrected SI-4 Eq. (S13) is the source-faithful calibration fit. The distinction \(a_1\ne a_2\) is intentional: heating from one phase shifter can change the other control's effective phase response and/or splitting behavior. The residual \(e_i\) represents a fitted offset associated with nonideal contrast and related imperfections.

The Table S1 transcription is in \`table-s1-calibration.yaml\`. It records common coefficients \(a_1=0.0730\), \(b=4.5760\), \(a_2=0.0638\), and ten per-row values of \(c_i,d_i,e_i\). The source table does not print row labels for each \(A_i/B_i\) pair; the row-to-index association remains an explicit open mapping question.

**Do not use Eq. (S12) as the final nonideal calibration model when reproducing the reported corrected fit.** Eq. (S12) is retained only as the preliminary source equation.

## 4. What this contract does and does not model

The SI-4 model is a scalar fitted interference observable. It does not, by itself, specify:

- a full complex transfer function \(T_\mathrm{device}(V,\lambda,T)\);
- complex field amplitude and phase at every physical reference plane;
- wavelength- or temperature-dependent dispersion;
- detector responsivity, gain mismatch, offset, bandwidth or noise;
- a foundry-specific geometry, material stack or heater implementation;
- a GF, AMF or TSMC process transfer;
- dynamic thermal settling, hysteresis or a complete multi-heater thermal interaction matrix.

Those are separate EIS model and characterization requirements. They must be added with their own evidence classes and cannot be backfilled from generic photonic examples.

## 5. Required EIS calibration record

For each of the ten source groups, preserve a separate record. For any new EIS physical MZI, create a new device-specific record rather than overwriting the Tian record.

Each record must contain:

1. Device identity, cell identity, group identity and physical port/control mapping.
2. Source or process identity, exact PDK release where applicable, and material/geometry stack.
3. Raw voltage/current/power-meter or detector observations; never only fitted parameters.
4. Applied \(V_A,V_B\), measured heater resistance, temperature and elapsed settling time.
5. Wavelength, polarization/mode, optical input powers, reference planes and detector configuration.
6. Fit equation identifier (SI-3 S11 or SI-4 S13), coefficient values and explicit units.
7. Fit method, initial conditions, bounds, weighting, residual vector, MAE/RMSE/max residual and confidence/uncertainty estimates.
8. Repeatability, drift, hysteresis, cross-talk and operating-range coverage.
9. Tool/software versions, source commit, run identifiers and raw-data/artifact hashes.
10. Provenance classification and reviewer.

The ten Tian Table S1 records are classified \`tian_fitted\`; the source describes their underlying characterization as experimental. They are not raw-data records and are not EIS measurements.

## 6. Optimization prohibition and release gates

No optimizer may be authored or run against this calibration baseline until:

- [ ] Source article and supplement identity/hash are checked.
- [ ] Table S1 values are independently checked against the page image.
- [ ] Units and observable normalization are either resolved from source context or explicitly carried as unknowns.
- [ ] Table row-to-group mapping is resolved or kept explicitly non-binding.
- [ ] SI-3 variance/standard-deviation ambiguity is resolved or excluded from optimizer objectives and acceptance thresholds.
- [ ] The corrected SI-4 Eq. (S13) is implemented independently and tested against source equations.
- [ ] A single MZI/KKA reproduction is completed with source-traceable controls and observables.
- [ ] The ideal scalar interference contract and the nonideal calibrated response are kept as separate model layers.
- [ ] EIS-specific process parameters are independently sourced, measured or fitted; no Tian values are silently reused as GF values.

A source-faithful software reproduction may be tested before physical simulation. A physical simulation requires a separate, named physical question, authorized process model, solver configuration, cost estimate and approval.

## 7. Relationship to RU-001 and existing EIS contracts

This package supplements the scalar interference contract in \`docs/02-architecture/EIS-KKA-001-Interference-Operator-and-Physical-Response-Contract.md\` and provides source material for the three-heater MZI workstream \`EIS-PTC-MZI-001\`.

It does not silently revise the repository's generic \`ru/RU-001\` acceptance limits or its historical design-context PDK identity. RU-001 and the Tian-specific calibration contract must be explicitly reconciled in a later reviewed change. In particular, the Tian SOI prototype data must not be conflated with the older SiN/TFLN reference context or with a GF PDK.

## 8. Acceptance meaning

Passing this contract means the source transcription, model boundary and calibration records are reproducible and reviewed. It does not mean an EIS device is fabricated, measured, foundry-qualified, or optimized. The next technical gate is faithful single-MZI reproduction—not optimization.
