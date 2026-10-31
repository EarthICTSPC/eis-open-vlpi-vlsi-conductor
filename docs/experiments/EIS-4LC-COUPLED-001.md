# EIS-4LC-COUPLED-001 — coupled four-node resonator and EO comparison

**Status:** Formal topology and state equations drafted; numerical candidate inputs are not yet populated; no physical simulation, PDK extraction, or measured result is claimed.

## 1. Source topology extracted from DeBenedictis ZF013

Source: Erik P. DeBenedictis, *Scaling up Reversible Logic with HKI Superconducting Inductors*, Zettaflops Technical Report ZF013, 11 April 2025, especially Figs. 1, 4 and 5 and the simulation/top-off discussion.  
PDF: https://debenedictis.org/erik/CATC/ZF013V25r.pdf  
arXiv: https://arxiv.org/abs/2504.09229

Figure 4a is not four isolated LC oscillators. It is one four-node closed ring:

- Node/phase ports: P0, P1, P2, P3.
- Inductor L0 connects P0 to P1.
- Inductor L1 connects P1 to P2.
- Inductor L2 connects P2 to P3.
- Inductor L3 connects P3 back to P0.
- Capacitors C0, C1, C2, C3 connect their respective phase nodes to ground.

Figure 4b tiles these quad-resonator cells in a checkerboard. Its boundary inductors are modified (the report's caption specifies twice the value) to support the boundary pattern. The present v1 formal model is the single quad cell; it does not claim that the checkerboard array or its boundary equations are already reproduced.

ZF013 describes the four nodes as naturally producing four sinusoidal phases in quadrature. It also says the circuit has multiple oscillation modes. In the simulator experiment, the author initialized the desired mode, attached a 2LAL load, observed run-down and eventual failure, and then used an external AC top-off source through a resistor. The source was described as both replenishing the desired mode and draining undesired modes. The report describes both four-phase AC and a two-phase AC alternative with 90-degree separation and three wires (GND and two phases).

The report's 15 kΩ and 5 kΩ drive-resistor values are specific to its simulator example. They are **not** EIS driver values and must not be copied into a room-temperature EO design.

## 2. Coupled state equations

Use the orientation i_n from P_n to P_(n+1), with indices modulo four. Let v_n be the voltage at P_n, L_n/R_n the series inductance/resistance of edge n, C_n the resonator shunt capacitance at node n, and Cload_n/Gload_n the first-order equivalent EO load to ground.

KCL at each node:

\[
(C_n+C_{load,n})\dot v_n =
u_n -(i_n-i_{n-1})-G_{load,n}v_n.
\]

KVL on each ring edge:

\[
L_n\dot i_n = v_n-v_{n+1}-R_ni_n.
\]

The complete dynamic state has eight quantities: four node voltages and four branch currents. The Lean module `Lean/EIS/FourLC.lean` defines the four node equations, four edge equations, state, parameter records, and total stored-energy expression.

Stored energy in the first lumped model:

\[
E=\frac12\sum_{n=0}^{3}(C_n+C_{load,n})v_n^2
 +\frac12\sum_{n=0}^{3}L_ni_n^2.
\]

The model keeps branch resistance and EO shunt conductance explicit so that dissipation is not silently labelled recoverable energy.

### First-order equivalent-circuit boundary

The present EO port is a per-phase single-ended-to-ground equivalent load. This is only a starting point. If the actual Ligentec/X-FAB SiN/TFLN phase shifter is differential/push-pull, has electrode-to-electrode capacitance, distributed traveling-wave electrodes, or a nontrivial multiport S-parameter model, replace this approximation with an extracted multiport capacitance/conductance or frequency-domain model. Do not force an actual differential device into four independent grounded capacitors without evidence.

## 3. Ideal modal analysis of the symmetric ring

For the reference case L_n=L and C_n=C, with zero loss, zero drive, and no EO load, the voltage modes satisfy:

\[
C\ddot{\mathbf v}+\frac{1}{L}\mathcal L_{ring}\mathbf v=0,
\qquad
\mathcal L_{ring}=
\begin{bmatrix}
2&-1&0&-1\\
-1&2&-1&0\\
0&-1&2&-1\\
-1&0&-1&2
\end{bmatrix}.
\]

The eigenvectors/eigenvalues are:

| Mode | Node vector (P0,P1,P2,P3) | Eigenvalue \(\lambda\) | Ideal angular frequency |
|---|---|---:|---|
| Common | (1,1,1,1) | 0 | 0 |
| Quadrature cosine | (1,0,-1,0) | 2 | \(\sqrt{2/(LC)}\) |
| Quadrature sine | (0,1,0,-1) | 2 | \(\sqrt{2/(LC)}\) |
| Alternating | (1,-1,1,-1) | 4 | \(\sqrt{4/(LC)}\) |

The two quadrature basis vectors are a degenerate pair. A traveling-wave combination of those modes produces the four phase-shifted node waveforms. This is a mode-selection condition, not four independent oscillator frequencies.

The Lean proofs establish these four exact graph-Laplacian eigenpairs. They do not prove that a fabricated loaded ring will maintain the ideal spectrum after asymmetry, loss, coupling, and EO loading.

## 4. EIS-specific connection question: differential outputs and static phase

The ideal quadrature basis has two opposite-node differential outputs:

- P0−P2 carries the cosine-mode differential.
- P1−P3 carries the sine-mode differential.

In the normalized basis vectors these differentials are 2 and 0, then 0 and 2, respectively. This suggests a possible way to feed two differential EO channels with 90-degree-related waveforms. It is a candidate interface mapping, not yet a verified match to a Ligentec/X-FAB electrode layout.

A critical constraint: the 4LC's natural outputs are **periodic sinusoids**. Directly applying them to an EO phase shifter gives periodic phase modulation. It does not hold a static phase setting. Therefore:

- `periodicDataModulation` may be evaluated with direct differential outputs.
- `staticPhaseHold` requires a characterized sample/hold, buffer/isolation, or another explicit bias-retention interface.
- Hold leakage, buffer energy, acquisition energy, phase droop, and settling must be included in the system energy budget.

This distinction is enforced by the Lean predicate `eoInterfaceCompatible`; direct quadrature outputs are not accepted as a static hold interface.

## 5. Mode control and top-off

The report identifies multiple modes and describes load-induced run-down and mode cross-talk. EIS v1 tracks four modal energy buckets:

- common mode;
- quadrature cosine mode;
- quadrature sine mode;
- alternating mode.

The intended useful mode is the quadrature pair. The other modes are not discarded from accounting. A conditioning-cycle record tracks desired-mode top-off, energy returned from the EO load, energy delivered to the EO load, resonator/driver losses, and energy drained from undesired modes. The destination of drained energy is separately labelled as dissipation or return to the external drive.

EIS should not assume that the ideal symmetry alone selects the desired mode. The actual design must characterize startup/initialization, phase reference, load imbalance, frequency splitting of the degenerate modes, amplitude/phase stability, and the top-off/undesired-mode-drain transfer function.

## 6. Comparison: cryogenic HKI 4LC versus room-temperature geometric LC

The fair comparison uses the **same EO load and same useful output requirements** for both candidates. The ring topology and state equations are shared; technology-specific values populate L, R, C, current limit, area, loaded Q, thermal overhead, and driver losses.

| Dimension | DeBenedictis HKI 4LC candidate | Room-temperature LC candidate | EIS acceptance input |
|---|---|---|---|
| Inductor implementation | Patterned superconducting HKI layer in report's 4 K example | Geometric/passive metal inductors: discrete, package, or on-chip spiral candidate | Extracted L, ESR/R(f), mutual coupling, current limit |
| Temperature | ZF013 states 4 K for the HKI example; 77 K YBCO is discussed as a future path | Nominal room-temperature operation; actual operating temperature measured | Temperature and thermal stabilization power |
| Energy storage | HKI areal energy-density argument is central to ZF013 | Magnetic-field energy stored in geometric inductors; footprint and metal loss matter | Maximum current, stored energy, area/volume |
| Loss | Resonator Q, coupling loss, load loss, and mode crosstalk still matter | Metal ESR, skin/proximity effect, substrate/package loss, driver and coupling loss | Loaded Q and per-cycle loss, measured at target frequency/load |
| Mode quality | Desired quadrature mode must persist under load; top-off also suppresses unwanted modes | Same modal requirement; parasitics/asymmetry may split or mix modes | Frequency split, phase error, amplitude error, ring-down and mode-purity data |
| Thermal cost | Include cryocooler wall-plug overhead at the declared cold stage | Include actual room-temperature driver/thermal management; no cryogenic penalty is assumed | Wall-plug joules per accepted cycle |
| EO load | ZF013's example load is reversible logic clock capacitance, not a TFLN modulator | Same EIS EO load is applied to the candidate | Actual modulator equivalent circuit and required modulation/hold regime |

ZF013 itself says normal-metal inductors are lossy at high frequencies and that geometric inductors require physical volume. It does not supply a room-temperature LC implementation for EIS, nor a numerical room-temperature-vs-HKI comparison. That comparison therefore remains an EIS experiment, not an extracted result from the report.

### Shared EIS load contract

For each candidate, populate the same:
- effective EO capacitance or full multiport capacitance matrix;
- conductance/termination and frequency-dependent loss;
- required phase swing (including Vπ/drive convention);
- target modulation bandwidth or static-hold duration;
- maximum settling time and allowed phase/amplitude error;
- operating frequency and output topology;
- current/voltage limits.

Candidate-specific evidence:
- all four L and R values, all four resonator C values, and any mutual inductances;
- measured/extracted loaded Q, modal frequencies, frequency splitting, and temperature dependence;
- footprint/area, current handling and thermal power;
- driver/top-off wall-plug energy and any returned energy;
- for HKI: measured cryogenic cooling wall-plug overhead at the operating point;
- for room-temperature LC: driver/inductor thermal loss and package parasitics.

## 7. Fair comparison protocol

1. Extract or measure one actual EIS EO phase-shifter electrical model. Record whether it is single-ended, differential, or traveling-wave. No guessed capacitance.
2. Use that same load and output-quality target for both candidate networks.
3. First solve/characterize the unloaded and loaded modal spectrum; quantify quadrature frequency split, phase error, amplitude imbalance, and mode purity.
4. Evaluate startup and top-off. Confirm how the desired quadrature mode is initialized and how undesired modes are drained without unstable mode capture.
5. Run time-domain RLC/EM co-simulation using measured/extracted R, C, L, coupling, driver impedance, and load. Track reservoir energy, EO load energy, source top-off energy, returned energy, and losses separately.
6. Include cryocooler wall-plug energy for the HKI candidate and package/thermal losses for the room-temperature candidate.
7. Compare only at matched phase swing, bandwidth/settling, phase/amplitude error, duty cycle, and accepted optical result.

No winner is assumed. A room-temperature LC implementation may avoid cryogenic overhead but pay more in inductor area and metal loss. HKI may provide higher energy density and lower conductor loss but pays a cryogenic system penalty and relies on a superconducting process. The measured load and loaded resonator Q decide.

## 8. Evidence status and non-claims

- **Source-derived topology:** four inductors in a closed ring, four shunt node capacitors, quadrature mode, checkerboard tiling with altered boundary inductors (ZF013 Figs. 4a–b).
- **Formalized:** ideal ring Laplacian and its four modal eigenpairs; eight-state KCL/KVL model; explicit load and technology-comparison records; static-hold versus periodic-modulation interface distinction.
- **Not established:** Lean CI result for this new branch; no actual SiN/TFLN EO equivalent circuit; no room-temperature LC component values; no EIS 4LC layout; no extracted mutual coupling or package model; no measured loaded Q, phase noise, top-off energy, cryocooler energy, or mode purity.
- **Not claimed:** a fabricated 4LC; AQFP equivalence; room-temperature equivalence to superconducting HKI; zero-energy operation; or photonic energy savings.

## Sources

1. Erik P. DeBenedictis, “Scaling up Reversible Logic with HKI Superconducting Inductors,” Zettaflops Technical Report ZF013, 11 April 2025. https://debenedictis.org/erik/CATC/ZF013V25r.pdf
2. Erik P. DeBenedictis, “Kinetic Inductors Enable Reversible Logic,” arXiv:2607.10046, 10 July 2026. https://arxiv.org/abs/2607.10046. This later work describes a quantitative framework using kinetic-inductor energy-storage models, a four-phase 4LC supply, and RLC simulation that accounts for data-dependent loading. It does not by itself establish EIS device data.
