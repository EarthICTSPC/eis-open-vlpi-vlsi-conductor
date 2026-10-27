# PTC Lean JSON → Python layout-backend bridge

**Status: integration scaffold; not yet connected to the canonical Harmonic-Aristotle-Lean4 source.**

This example establishes a narrow, reviewable boundary:

```text
canonical Lean PTC.Netlist
  → Lean JSON exporter
  → EIS-PTC-Netlist-v0 JSON
  → Python schema/graph validation
  → placement plan
  → (only after PDK mapping is configured) layout backend
```

## Important limits

- The Lean exporter shown in `PTC.Netlist.JSON.template.lean` is a porting template. The canonical `PTC.Netlist` definitions and Lean toolchain were not present in this repository when this scaffold was prepared. Do not treat the template as compiled or proven.
- The Python default is **validation and placement-plan output only**. It does not emit GDS by silently substituting generic cells.
- Generic grating couplers are not lasers or balanced photodetectors. A two-input/two-output MZI cell is not interchangeable with any arbitrary MZI abstraction. These substitutions must not be represented as a physical implementation.
- No routing is accepted merely because two components have references. Routing must use explicit logical port names mapped to real PDK port names, and must fail closed on missing ports or route errors.
- `SiEPIC_EBeam` is an example target label, not proof that the corresponding PDK is installed or authorized. EIS's preferred physical direction remains SiN/TFLN; this SOI example is a software-interface exercise only.
- This logical netlist is not Tian et al.'s CUMEC GDS, not a foundry-qualified layout, and not evidence of simulated or measured performance.

## Files

- `PTC.Netlist.JSON.template.lean` — exporter template to adapt after importing the canonical source.
- `netlist.schema.json` — JSON Schema for format v0.
- `eis_ptc_netlist_to_siepic.py` — strict JSON validation and deterministic placement-plan consumer. Layout generation is intentionally gated behind a future explicit PDK adapter.
- `test_netlist_consumer.py` — standard-library unit tests.

## Run the checks

```bash
python -m unittest discover -s examples/ptc-lean-json-siepic -p 'test_*.py' -v
python examples/ptc-lean-json-siepic/eis_ptc_netlist_to_siepic.py examples/ptc-lean-json-siepic/fixtures/ptc10x1_minimal.json
```

These checks validate the Python interface and example fixture only. They do not validate the Lean exporter, canonical PTC topology, PDK mapping, optical behavior, DRC/LVS, or GDS.

## Next gate

Obtain the canonical Harmonic-Aristotle-Lean4 repository revision containing `PTC.Netlist` and `ptc10x1`. Add the exporter there (or import it as a pinned dependency), compile and run it, then compare its JSON against the schema and graph invariants. Only after a real PDK adapter and explicit port map exist should a separate opt-in step generate GDS.
