# EIS-KKA-PHASE-001 — SOI Phase-Control, Thermal-Isolation and Calibration Lessons

**Status:** Research-grounded engineering plan. No EIS SOI device has yet been simulated, fabricated or measured from this work package.  
**Parent workstream:** [#66 — EIS-KKA-64-001](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/66)  
**Primary implementation issue:** [#71 — phase-control, calibration and thermal-management architectures](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/71)  
**System-budget interface:** [#72 — optical, detector and full-system energy budget](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/72)

## 1. Purpose

Extract transferable engineering lessons from Liao and Lee's Ligentec Si3N4 circuit and apply them as testable hypotheses for EIS's SOI KKA/VLPI implementation. The objective is not to reproduce a quantum photonic circuit or import its heater-power numbers. It is to improve the classical KKA phase-control, thermal-management, calibration and evidence architecture.

The Liao–Lee experiment uses two on-chip squeezed-vacuum sources and balanced interference to control two-mode Gaussian correlations. EIS's Tian-style KKA work is a different computational use of programmable amplitude/phase-coupled fields and interference. The shared engineering layer is integrated interferometry with programmable phase control—not quantum state generation.

## 2. What the Ligentec paper reports

Liao and Lee report:
- Si3N4 waveguide circuit, fully clad in SiO2, fabricated by Ligentec SA using a commercial photolithographic process.
- TiN microheaters for thermo-optic tuning.
- Deeply etched air trenches near each microheater, intended to mitigate thermal crosstalk.
- Calibrated, approximately linear effective phase-versus-heater-power response for the output-path heater.
- Aligned and orthogonal squeezing-orientation settings at approximately 30 mW and 101 mW dissipated heater power, respectively.
- Fitted phase tuning rate of 1.242 degrees/mW and a π-phase-shift power of 145 mW.
- While tuning that output-path heater over the 0–90 degree effective-phase range, the dual-ring squeezer resonance positions showed no appreciable shifts in that particular test.

These are results for that specific Si3N4/TiN circuit and measurement. They are not SOI specifications. The observed absence of appreciable resonance shifts is not proof of zero thermal coupling in a larger array.

## 3. Why the lessons transfer to SOI

There is direct SOI prior art for the same engineering questions. Jacques et al. experimentally compared TiN and N++ doped-silicon thermo-optic phase shifters in the same SOI process. They report:
- Optimized TiN heater: Pπ = 21.4 mW and time constant τ = 5.6 µs.
- Best N++ doped-Si heater: Pπ = 22.8 mW and τ = 2.2 µs.
- Deep trenches were the best tested structures, without special fabrication techniques, for mitigating heat leakage to nearby phase-sensitive devices.

This makes the Liao–Lee design lesson transferable in principle: characterize the thermal interaction network, treat layout/isolation as an engineering variable, and measure phase response and neighboring-device disturbance together. It does **not** mean the Ligentec SiN trench geometry can be copied into an SOI PDK unchanged. Trench geometry, depth, spacing, mechanical robustness, process design rules, optical loss and thermal time constant must be evaluated for the actual SOI stack and foundry rules.

The SOI heater numbers are literature benchmarks, not EIS measurements and not guaranteed GF/AMF process performance.

## 4. EIS SOI hypotheses to test

1. **Thermal isolation is a layout-level design variable.** Evaluate trench/no-trench or foundry-approved isolation variants around SOI phase shifters, subject to PDK rules and mechanical/process constraints.
2. **Heater material and geometry must be compared on the same process.** Compare TiN/metal and doped-silicon options only where supported by the authorized PDK; record resistance, current density, optical loss, phase efficiency, footprint and reliability.
3. **A phase shifter is a multiport thermal object.** A single phase-versus-power curve is insufficient for a dense tile. Measure or simulate the effect of each heater on every relevant optical phase/resonance observable.
4. **Calibration is part of the computation system.** Record initial phase, amplitude balance, wavelength, chip temperature, heater state, drift, repeatability and recalibration cost.
5. **Static holding power matters.** Report both transition energy and steady-state holding power. For a thermal phase shifter, do not describe Pπ as energy per operation; energy depends on waveform, duration, duty cycle and thermal settling.
6. **Alternatives must be compared at the system boundary.** Carrier-based or electro-optic phase control may reduce static thermal load or improve speed, but can introduce insertion loss, drive energy, voltage constraints, process requirements and calibration complexity. Do not assume an option is available on GF/AMF until confirmed.

## 5. SOI characterization model

For heater vector P and calibrated phase-observable vector φ:

    φ = φ0 + Hthermal P + r(P, λ, T, history)

Hthermal is the measured/fitted small-signal heater-to-phase interaction matrix; r captures nonlinearity, hysteresis, history dependence and residual effects; λ is optical wavelength and T is controlled chip/environment temperature.

Retain the complex transfer model:

    Eout = T(device controls, wavelength, temperature, optical power, history) · Ein

Do not reduce this to phase alone: heater-induced amplitude changes, loss and wavelength shifts can alter the KKA interference result.

Minimum characterization records:
- Phase-versus-power curves, increasing and decreasing sweeps.
- Heater resistance, voltage, current and dissipated power.
- Phase efficiency Pπ, time constant and settling/overshoot.
- Insertion loss and amplitude change versus heater state.
- Full thermal interaction matrix, with uncertainty and layout variants.
- Wavelength and ambient/chip-temperature sensitivity.
- Repeatability, drift, hysteresis and recalibration interval.
- Process, die, device, layout and instrument provenance.
- Uncertainty and calibrated measurement floor.

## 6. Proposed experiment sequence

**PHASE-A — SOI phase-shifter baseline**
- One standalone phase shifter per available authorized heater option.
- Measure phase, amplitude/loss, resistance, Pπ and time response.
- Establish reference conditions and uncertainty before testing.

**PHASE-B — thermal interaction coupon**
- Two or more adjacent phase shifters with a documented spacing sweep.
- Compare only foundry-authorized isolation geometries, including trench variants if supported.
- Build Hthermal; include nearest-neighbor and nonlocal coupling.

**PHASE-C — three-phase-shifter KKA MZI**
- Apply characterized phase-control elements to the Tian-style MZI topology.
- Measure complex transfer and interference output; verify the KKA field-transfer contract.
- Keep phase-control energy separate from optical source, detector and conversion energy.

**PHASE-D — calibration and drift**
- Test reference-assisted calibration, temperature tracking and recalibration scheduling.
- Quantify calibration time, data overhead, drift between calibrations and impact on KKA output/attention quality.

**PHASE-E — 64×64 budget integration**
- Use measured or explicitly fitted phase-control parameters in the tile energy and area model.
- Include static holding power, reconfiguration energy, calibration overhead, drivers, routing, thermal management and idle states.
- Report sensitivity to control cadence and tile utilization.

No paid EM/FDTD, external compute, MPW booking, fabrication or laboratory measurement is authorized by this document. Each requires a separate EIS-approved, costed plan.

## 7. Acceptance gates

- **SPECIFIED:** SOI stack, PDK release, test structures, observables, test conditions and thresholds are frozen.
- **COMPUTATIONALLY DEMONSTRATED:** deterministic analysis and synthetic-data tests pass.
- **SIMULATED:** only after a named/versioned simulator has actually run and raw inputs/outputs are retained.
- **MEASURED:** raw instrument data, calibration, device identity, environmental conditions and uncertainty are retained.
- **SOI PHASE-CONTROL QUALIFIED:** phase range, loss, time response, thermal coupling, drift and reliability meet predeclared requirements.
- **KKA-CONFORMANT:** measured complex transfer and interference output satisfy the reviewed Lean/Python KKA contract.
- **64×64 SYSTEM-ACCEPTED:** phase-control plus calibration overhead is included in the matched full-system energy/quality/latency comparison.

No single heater metric is a pass criterion by itself. Select the preferred architecture on a Pareto comparison of static power, transition energy, speed, optical loss, thermal crosstalk, area, reliability, driver complexity and calibration burden.

## 8. References

1. Cheng-Ting Liao and Ming-Chang M. Lee, “On-chip reconfigurable two-mode Gaussian correlations in a Si3N4 photonic circuit,” *Optics Express* **34**(24), 45394–45406 (2026). DOI: [10.1364/OE.616756](https://doi.org/10.1364/OE.616756). Published 16 November 2026. Ligentec-fabricated Si3N4/SiO2 circuit with TiN microheaters and etched air trenches.
2. Maxime Jacques, Alireza Samani, Eslam El-Fiky, David Patel, Zhenping Xing, and David V. Plant, “Optimization of thermo-optic phase-shifter design and mitigation of thermal crosstalk on the SOI platform,” *Optics Express* **27**(8), 10456–10471 (2019). DOI: [10.1364/OE.27.010456](https://doi.org/10.1364/OE.27.010456). Direct SOI comparison of TiN and N++ doped-silicon heaters and thermal-isolation structures.
3. “Thermo-optic phase shifters based on silicon-on-insulator platform: state-of-the-art and a review,” *Micromachines* (2022). DOI: [10.3390/mi13121982](https://doi.org/10.3390/mi13121982). Background review; use primary device papers for quantitative design decisions.

## 9. Evidence classification

- Liao–Lee circuit construction and numerical results: **reported experimental results in the cited paper**.
- Jacques et al. SOI heater and trench results: **reported experimental results in the cited paper**.
- Transfer of trench/isolation and calibration principles to EIS SOI KKA: **engineering inference / hypotheses to test**.
- EIS SOI performance, 64×64 suitability and system energy advantage: **not yet demonstrated**.
