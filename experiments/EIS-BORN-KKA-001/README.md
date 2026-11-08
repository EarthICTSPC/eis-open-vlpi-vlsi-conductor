# EIS-BORN-KKA-001 — Born Attention and KKA Computational Contract

This directory contains the executable scalar reference and parameterized energy ledger for the bounded investigation. The normative scope, equations, work packages, gates and claim boundaries are in [the experiment charter](../../../docs/experiments/EIS-BORN-KKA-001.md).

## Files

- `born_reference.py`: complex overlap, fourth-power Born score, row-normalized weights, quadrature reconstruction, signed KKA cross-term and scalar bilinear bridge.
- `energy_ledger.py`: explicit wall-plug component ledger and matched-run comparison.
- `test_born_reference.py`: deterministic and seeded randomized mathematical conformance tests.
- `test_energy_ledger.py`: energy-boundary completeness and matched-comparison tests.

## Run

From this directory:

```bash
python -m pytest -q
```

No optical simulator, PDK, proprietary data, network service or paid compute is required.

## Current evidence status

- Equations: E1 analytical target, source-faithful transcription to be reviewed.
- Python: E2 executable reference and tests; CI result pending.
- Lean: E3 proof candidate in `EISKKA/BornAttention.lean`; Lean CI result pending.
- Energy ledger: parameterized accounting model only. All values in unit tests are synthetic fixtures.
- Device/optical mapping: not run.
- Hardware, PDK, energy advantage and task-quality claims: none.

## Interpretation discipline

The scalar KKA cross-term supplies a signed real projection. Born attention requires the complex overlap magnitude, its fourth power, and row normalization. The formal identity between the measured bilinear readout and a conjugated KKA operand does not establish a physical conjugator or circuit. A second quadrature measurement/reconstruction, magnitude-square, intensity multiplication, and row reduction/normalization remain explicit mapping obligations.
