# EIS-4LC-COUPLED-001

Formal and executable first-pass model of DeBenedictis ZF013 Fig. 4a's coupled four-node resonant ring, plus a matched comparison contract for room-temperature geometric LC and cryogenic HKI implementations under one shared EIS EO load.

## Files

- `Lean/EIS/FourLC.lean`: four-node ring topology, ideal graph-Laplacian eigenmodes, quadrature pair, KCL/KVL state equations, stored-energy expression, modal conditioning ledger, static-hold versus periodic-modulation compatibility, and matched technology comparison record.
- `experiments/eis-4lc-coupled-001/ring_model.py`: standard-library RK4 reference integrator for the eight-state model.
- `experiments/eis-4lc-coupled-001/test_ring_model.py`: synthetic regression tests for modal eigenpairs, quadrature differential outputs, state-equation power balance, numerical energy conservation, and matched EO load enforcement.
- `docs/experiments/EIS-4LC-COUPLED-001.md`: source extraction, equations, modal analysis, EO interface constraints, candidate comparison and evidence plan.

## Run reference tests

From the repository root:

```sh
python -m unittest discover -s experiments/eis-4lc-coupled-001 -p 'test_*.py' -v
```

The RK4 script is a reference model, not an EM solver or PDK simulator.

## Source-faithful topology

Four inductors are connected in a closed ring:
- L0: P0-P1
- L1: P1-P2
- L2: P2-P3
- L3: P3-P0

Each Pn node has its own shunt capacitor Cn to ground. The first EO load approximation adds a phase-port shunt capacitance and conductance at each node. If the target EO phase shifter is differential/push-pull or distributed traveling-wave, replace that approximation with a measured/extracted multiport model before making a device claim.

## Ideal symmetric-ring modal result

For equal L and C, the ring graph-Laplacian eigenvalues are 0, 2, 2, and 4. The quadrature cosine and sine modes are degenerate; a traveling combination of those two modes creates four phase-related node waveforms. The common and alternating modes are tracked as undesired mode content rather than discarded.

## EIS-specific caution

The resonator outputs are periodic sinusoids. Direct connection to an EO phase shifter is a periodic phase modulation, not a static phase hold. Static phase configuration requires a characterized buffer/sample-hold or another explicit bias-retention interface and its leakage/acquisition energy must be charged to the co-power ledger.

## Evidence status

The test fixtures are synthetic and exist only to test model equations. They are not EIS component values. No actual room-temperature LC device, HKI device, TFLN phase-shifter model, measured loaded Q, mode-purity result, hardware top-off, cryocooler energy or photonic energy advantage is asserted.
