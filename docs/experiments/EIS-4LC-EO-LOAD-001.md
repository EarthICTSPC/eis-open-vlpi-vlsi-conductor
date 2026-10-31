# EIS-4LC-EO-LOAD-001 — Measured differential EO load reference

**Status:** first public measured-device parameterization; analytical sizing only  
**EIS implementation scope:** room-temperature VLPI  
**Relationship:** extends the evidence basis for EIS-4LC-COUPLED-001; does not replace the current 4LC state model.

## 1. Why this reference

Lee et al. report a fabricated hybrid TFLN–SiN electro-optic phase-modulator array with a measured terminal capacitance and measured half-wave voltage. It is a closer public analog to an EIS SiN/TFLN phase-setting load than the SOI/TiN thermo-optic heaters in Tian et al.

Source: Woo-Bin Lee, Yun-Jae Kwon, Do-Hyung Kim, Yoon-Ho Sunwoo, and Sang-Shin Lee, “Hybrid integrated thin-film lithium niobate-silicon nitride electro-optical phased array incorporating silicon nitride grating antenna for two-dimensional beam steering,” *Optics Express* 32(6), 9171–9183 (2024), DOI: [10.1364/OE.518961](https://doi.org/10.1364/OE.518961).

## 2. Device data and evidence grades

| Parameter | Value | Evidence / qualification |
|---|---:|---|
| Platform | hybrid TFLN–SiN, SiN strip-loaded TFLN | fabricated device |
| Optical wavelength | near 1550 nm; 1530–1600 nm operating band | measured device range |
| EO electrode mode | push-pull MZI configuration | reported experimental configuration |
| EO interaction length | 1.56 cm | device geometry |
| Differential phase-shifter capacitance | 0.98 pF | measured with HIOKI IM3536 LCR meter |
| Half-wave voltage | 3.64 V | reported measured value for 1.56 cm element |
| Energy per π phase shift | 3.2 pJ/π | paper-reported; agrees with its stated sinusoidal-energy expression |
| Bandwidth for 1.56 cm element | approximately 1.2 GHz | estimated from RC-limited scaling; not directly measured at that length |
| Measured 3 dB bandwidth | approximately 2.9 GHz | measured on a shorter 0.94 cm MZI test structure |
| DC behavior | lithium-niobate DC drift observed | phase stability / bias-hold issue |

The authors' analytical expression is \(E=C V_\pi^2/4\). Substituting the measured \(C=0.98\,\mathrm{pF}\) and \(V_\pi=3.64\,\mathrm{V}\) gives approximately 3.25 pJ, consistent with the reported 3.2 pJ/π after rounding. This is the source's sinusoidal capacitor-energy convention; it is not a measured net wall-plug cost for a regenerative driver.

The same paper first gives an estimated capacitance of 0.63 pF for a simulated design and a 2.3 pJ/π result. Those are not the measured 0.98 pF / 3.2 pJ device values and must not be mixed.

## 3. Why the present PR #52 EO model cannot yet consume this data directly

The current Lean and Python models implement four independent single-ended shunt loads from each phase node to ground. Lee et al.'s measured phase shifter is characterized in a push-pull MZI electrode arrangement and reports a terminal capacitance per phase modulator. Therefore the 0.98 pF value must not be split arbitrarily among four node-to-ground capacitances.

The next model version needs a differential two-terminal load, initially two matched phase-shifter loads across the opposite-node output pairs P0–P2 and P1–P3. Each load requires:
- measured/extracted differential capacitance;
- differential leakage/conductance and electrode series resistance;
- terminal definition and measurement frequency for the 0.98 pF capacitance;
- output voltage swing and phase-shift mapping;
- bias/hold or refresh behavior, including the observed DC drift;
- driver output impedance and any isolation or sample/hold element.

A distributed traveling-wave modulator is a separate device class and must use a transmission-line or extracted multiport model, including electrode loss and termination. It is not represented by this lumped 0.98 pF reference.

## 4. Ideal differential-load 4LC sizing relation

For the equal-L four-node ring, equal node-to-ground capacitance \(C_g\), and two matched differential EO capacitances \(C_{EO}\) across P0–P2 and P1–P3, the quadrature-mode effective capacitance gives:

\[
f_q = \frac{1}{2\pi}\sqrt{\frac{2}{L(C_g+2C_{EO})}}.
\]

Here \(L\) is each of the four equal ring-branch inductances. The two equal differential loads preserve the ideal quadrature pair; loading only one diagonal port breaks the symmetry and should not be treated as the same matched four-phase case.

Using measured \(C_{EO}=0.98\,\mathrm{pF}\), and using the 1.2 GHz EO bandwidth estimate only as an illustrative frequency-sizing point, the ideal \(C_g\rightarrow 0\) limiting case requires:

\[
L = \frac{2}{(2\pi f_q)^2(2C_{EO})}
\approx 18\,\mathrm{nH}
\]

per ring branch. This is a first-order geometric-inductor sizing target, not a foundry value. Any nonzero ring-node capacitance changes the L required for the same frequency. Loaded Q, conductor loss, parasitic capacitance, mutual coupling, phase-mode purity, footprint, startup, and driver/top-off loss are still unknown.

With both differential EO loads driven sinusoidally to a peak differential voltage of \(V_\pi\), the source's average capacitor-energy convention gives:

\[
E_{EO,\mathrm{pair}} =
2\left(\frac{C_{EO}V_\pi^2}{4}\right)
\approx 6.5\,\mathrm{pJ}.
\]

That is the average electric energy represented by the two matched EO loads at the stated peak voltage. It is not the net energy drawn from the power supply per update, and it is not a recovered-energy measurement. The actual reservoir input must cover only the losses and any energy not returned, but those fractions are unknown until the loaded resonator and bidirectional driver are modeled and measured.

## 5. Relevance to EIS and the 4/8-phase distinction

The laser is the optical carrier source. In the comparable photonic systems, data and phase are imposed downstream by EO modulators; the laser pump is not a four-phase or eight-phase electronic power-clock. EIS should keep:
1. laser electrical wall-plug energy;
2. optical power launched into and transmitted through the PIC;
3. EO phase-shifter/modulator driver energy;
4. passive optical interference;
5. photodetector/readout energy; and
6. electronic controller/power-clock energy

as separate ledger terms.

A room-temperature 4LC would be an electronic resonant reservoir potentially relevant to the capacitive EO driver and/or electronic control supply. It does not modulate the laser's pump power and does not clock photons.

The distinction between periodic modulation and static phase holding remains. A 4LC sinusoidal output directly applied to an EO phase shifter produces a periodic phase waveform. Maintaining a static programmed phase requires an explicit bias hold, buffer, or isolation interface, with its own leakage, acquisition, and energy costs.

## 6. Decision and next evidence

**Preliminary result:** A room-temperature resonant driver is not ruled out for this class of lumped differential EO load. An ideal 4LC can be sized against a real 0.98 pF / 3.64 V push-pull phase-shifter benchmark. The first ideal sizing point is about 18 nH per ring branch if node shunt capacitance is neglected and 1.2 GHz is used as a reference frequency.

**Not established:** a fabricable low-loss 18 nH ring, loaded Q, phase accuracy, power-clock startup, sustained quadrature operation, static-phase hold, recovered charge fraction, driver wall-plug efficiency, or a net energy advantage.

The first actual EIS comparison requires measured or extracted room-temperature L/R/C/Q and parasitics for a geometric resonator, plus the actual EIS EO electrode terminal model and its driver/bias interface. Keep PR #52 draft; do not start cryogenic HKI reproduction for EIS.

## 7. Reproducible parameter check

Run alongside the existing synthetic 4LC regression tests:

~~~sh
python -m unittest discover -s experiments/eis-4lc-coupled-001 -p 'test_*.py' -v
~~~

The new Python benchmark constants and equations are in experiments/eis-4lc-coupled-001/eo_reference.py. The tests only check source transcription and the analytic ideal-ring relation; they do not simulate a physical device.
