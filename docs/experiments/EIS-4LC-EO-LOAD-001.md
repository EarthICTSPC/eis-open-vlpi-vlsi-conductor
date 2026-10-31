# EIS-4LC-EO-LOAD-001 — Published hybrid SiN/TFLN EO reference

**Status:** published measured-device reference; 4LC mapping remains conditional  
**EIS implementation scope:** room-temperature VLPI  
**Relationship:** evidence note for EIS-4LC-COUPLED-001; does not replace the present 4LC state model.

## 1. Source

Woo-Bin Lee, Yun-Jae Kwon, Do-Hyung Kim, Yoon-Ho Sunwoo, and Sang-Shin Lee, “Hybrid integrated thin-film lithium niobate-silicon nitride electro-optical phased array incorporating silicon nitride grating antenna for two-dimensional beam steering,” *Optics Express* 32(6), 9171–9183 (2024), DOI: [10.1364/OE.518961](https://doi.org/10.1364/OE.518961).

The paper reports a fabricated hybrid TFLN–SiN EO phase-modulator array and is a useful external reference. It is not EIS PDK data.

## 2. Source-reported device values and qualifications

| Parameter | Value | Evidence / qualification |
|---|---:|---|
| Platform | hybrid TFLN–SiN; SiN strip-loaded TFLN | fabricated device |
| Operating wavelength | near 1550 nm; 1530–1600 nm range | measured system range |
| MZI phase-modulator characterization | push-pull electrode configuration | reported |
| EO interaction length | 1.56 cm | device geometry |
| Capacitance | 0.98 pF per EO phase modulator | measured with HIOKI IM3536 LCR meter |
| LCR terminal definition | not stated | unknown; do not label as differential C or node-to-ground C |
| LCR test frequency | not stated in accessible paper text | unknown |
| Half-wave voltage | 3.64 V | reported for 1.56 cm element |
| Energy per π shift | 3.2 pJ/π per phase modulator | paper-reported |
| Bandwidth of 1.56 cm modulator | approximately 1.2 GHz | estimated from RC-limited scaling, not measured at that length |
| Measured 3 dB bandwidth | approximately 2.9 GHz | measured on shorter 0.94 cm MZI test structure |
| Low-frequency characterization | 100 kHz sawtooth applied through GSG probe | reported setup |
| DC behaviour | lithium-niobate DC drift observed | reported phase stability issue |

The authors describe the modulator as a capacitor and use \(E=C V_\pi^2/4\). With \(C=0.98\,\mathrm{pF}\) and \(V_\pi=3.64\,\mathrm{V}\), this expression gives approximately 3.25 pJ, consistent with 3.2 pJ/π after rounding. This is the paper's capacitor-energy estimate, not a measured net wall-plug cost or recovered-energy result.

The paper separately discusses a simulated estimate of 0.63 pF and 2.3 pJ/π. Those simulated values must not be confused with the later measured 0.98 pF / reported 3.2 pJ/π.

## 3. Critical terminal-definition limitation

The article says the MZI characterization used a push-pull electrode configuration and a GSG probe. It later says an LCR meter measured “the capacitance of each EO phase modulator” as 0.98 pF. It does **not** specify the exact LCR terminals, whether the value is differential across a pair, single-ended to ground, or a particular electrode equivalent, nor the LCR measurement frequency in the accessible description.

Therefore:
- 0.98 pF is a real published capacitance measurement per EO phase modulator;
- it is not yet a verified \(C_{EO}\) across a two-terminal differential port;
- it must not be divided across four ring nodes or attached to an ideal 4LC diagonal until the measurement terminals and modulator electrode schematic are confirmed.

This is the principal information gap before an actual matched ring/load comparison.

## 4. Conditional ideal 4LC sizing equation

For equal ring inductors \(L\), equal node-to-ground capacitance \(C_g\), and **if** two matched differential EO capacitors \(C_{EO}\) are truly connected across P0–P2 and P1–P3, the quadrature-mode relation is:

\[
f_q = \frac{1}{2\pi}\sqrt{\frac{2}{L(C_g+2C_{EO})}}.
\]

Thus:

\[
L = \frac{2}{(2\pi f_q)^2(C_g+2C_{EO})}.
\]

If, purely as a hypothetical, the published 0.98 pF value were confirmed to be the full two-terminal capacitance of each of those differential loads, and if \(C_g\to0\), then using 1.2 GHz as an illustrative frequency point gives approximately 18 nH per ring branch.

**This 18 nH result is conditional, not a measured-device match.** The paper's 1.2 GHz is an estimated modulator bandwidth, not an instruction to set the resonator frequency to 1.2 GHz. The actual operating frequency must follow the required phase-update waveform, data rate, driver architecture, and accepted settling/phase-error envelope.

If the 0.98 pF instead represents each individual electrode-to-ground or another equivalent capacitance, the loaded capacitance matrix and resulting modes change. We must obtain the source terminal diagram or independently characterize the port before using the number in the 4LC equations.

## 5. What the reference does tell us

It provides a real scale for the EO problem: a 1.56 cm hybrid SiN/TFLN phase modulator with reported \(V_\pi=3.64\) V, measured capacitance of 0.98 pF per modulator, and an estimated RC-limited bandwidth around 1.2 GHz. The paper reports phase programming using low-frequency sawtooth drive and observes DC drift in lithium niobate. It does not show a resonant driver, charge recovery, or a 4LC interface.

The reported 17.3 dB total insertion loss of that particular phased-array assembly is also a reminder that laser optical power cannot be assumed negligible in every system. Its loss stack is device-specific and should not be copied as EIS loss data.

## 6. EIS energy-domain boundary

The laser is an optical carrier source. In the photonic computing systems reviewed, the laser output feeds the PIC and the data/weights/phase are encoded downstream by EO modulators. The laser pump is not the electronic four-phase/eight-phase power-clock.

Keep these separate in EIS accounting:
1. laser electrical wall-plug energy;
2. optical power launched into and transmitted through the PIC;
3. EO driver energy;
4. passive optical interference;
5. detector/readout energy; and
6. electronic controller and its power-clock energy.

A room-temperature 4LC could be investigated as an electronic resonant reservoir for capacitive EO drive and/or controller power domains. It does not clock photons or ramp the laser pump.

A direct periodic 4LC sinusoid is not a DC phase hold. Static phase settings require a separate characterized bias/hold path, including the lithium-niobate drift behaviour, acquisition and leakage costs.

## 7. Decision and next evidence

The public data is sufficient to justify a **reference case**, but not an actual ring/load parameter match. The missing terminal definition means we cannot yet honestly say 18 nH is the device-matched answer.

Next evidence:
- retrieve the exact electrode/LCR terminal definition and measurement frequency from the paper authors or supplementary material;
- characterize the actual EIS SiN/TFLN EO device terminal matrix, including C, leakage, electrode R/L and bias stability;
- choose the ring operating frequency from the real update waveform, not by equating it with the paper's estimated bandwidth;
- extract or measure room-temperature geometric ring L/R/Q, parasitic capacitance, coupling, phase error and footprint;
- quantify driver/top-off energy, returned energy at the supply, static hold path and thermal dissipation.

**Scope:** EIS room-temperature VLPI only. Cryogenic HKI remains literature context, not an EIS candidate to reproduce.

No measured EIS 4LC, useful-energy recovery fraction, loaded Q, phase-mode purity, or net energy advantage is claimed.

## 8. Reproducible check

\`\`\`sh
python -m unittest discover -s experiments/eis-4lc-coupled-001 -p 'test_*.py' -v
\`\`\`

The Python functions contain the source values and conditional ideal-ring relation. Tests check source transcription and algebra only; they are not device simulation.
