# EIS-4LC-COUPLED-001

Formal and executable first-pass model of DeBenedictis ZF013 Fig. 4a's coupled four-node resonant ring, with a published room-temperature hybrid SiN/TFLN EO phase-modulator reference.

## Files

- Lean/EIS/FourLC.lean: ring topology, ideal graph-Laplacian eigenmodes, quadrature pair, KCL/KVL state equations, stored-energy expression, modal bookkeeping, static-hold versus periodic-modulation distinction, and candidate comparison record.
- experiments/eis-4lc-coupled-001/ring_model.py and test_ring_model.py: standard-library RK4 reference and synthetic equation regression tests.
- experiments/eis-4lc-coupled-001/eo_reference.py and test_eo_reference.py: published Lee et al. 2024 device values, explicit capacitance-terminal uncertainty, and conditional ideal 4LC sizing equations.
- docs/experiments/EIS-4LC-COUPLED-001.md: ZF013 topology/source extraction, equations and evidence plan.
- docs/experiments/EIS-4LC-EO-LOAD-001.md: published measured EO reference, terminal-definition limitation, conditional sizing and next evidence.

## Run reference tests

~~~sh
python -m unittest discover -s experiments/eis-4lc-coupled-001 -p 'test_*.py' -v
~~~

The RK4 reference is not an EM solver or PDK simulator. The EO-reference tests check published values and an ideal differential-load formula under a deliberately explicit hypothetical input. They are not device simulation.

## Source-faithful 4LC topology

Four inductors form a closed ring: L0 P0-P1, L1 P1-P2, L2 P2-P3, L3 P3-P0. Each Pn node has a shunt capacitor Cn to ground. This models one quad cell from ZF013 Fig. 4a, not the Fig. 4b checkerboard array with altered boundary inductances.

## EO model boundary

The original eight-state ODE currently represents first-order single-ended-to-ground shunt C/G loads. Lee et al. 2024 report 0.98 pF capacitance per EO phase modulator using an LCR meter and a push-pull MZI characterization, but do not state the LCR terminal definition. That measured value is kept separate and must not be assumed to be differential or single-ended-to-ground until the terminal diagram is confirmed. A push-pull/differential or distributed traveling-wave device requires the appropriate two-terminal or extracted multiport model.

The 18 nH figure is a conditional ideal sizing point only if 0.98 pF is verified as the full differential capacitance across each of two opposite-node outputs, with Cg negligible and 1.2 GHz chosen as a purely illustrative reference frequency. The source's 1.2 GHz is an estimated modulator bandwidth, not a required resonator frequency.

## EIS-specific caution

Direct resonator outputs are periodic sinusoids, not DC phase holds. A static programmed phase requires a separately characterized bias/hold or isolation interface and its leakage/acquisition costs.

## Evidence status

The ideal modes are analytical. The 4LC RK4 tests use synthetic parameters. The EO reference is external published device data; its 0.98 pF terminal definition is unspecified in the paper. The conditional sizing equation is analytical only. No EIS PDK extraction, room-temperature LC L/R/Q, fabrication, measured mode purity, top-off energy, returned-energy fraction, or energy advantage is claimed. EIS scope is room-temperature VLPI; cryogenic HKI remains literature context only.
