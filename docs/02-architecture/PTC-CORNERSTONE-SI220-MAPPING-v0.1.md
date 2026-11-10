# Cornerstone si220 mapping assessment for Tian-style PTC

**Status:** public-source inventory complete; three-heater MZI mapping not yet implemented or verified  
**Purpose:** assess whether the pinned Cornerstone cspdk si220 package can serve as an internal SOI functional-reconstruction backend. This is not a foundry selection or Tian-process reproduction.

## Pinned candidate identity

The existing EIS manifest identifies:
- package: `gdsfactory/cspdk`, `cspdk==2.1.0`;
- process variant: `cspdk.si220`, SOI 220 nm;
- source tag: `v2.1.0`;
- source commit: `09ca1a1e23c3a00f4f51e89ef2fa83b3f352ccbb`;
- wheel SHA-256: `eea56e49535ab5aa61b189dd94bd4d6f7f284afd035b851b21dd2a35ef13febf`.

The clean Python 3.12.16 CI smoke previously installed the package, imported the si220 library, instantiated its default MZI, and evaluated selected SAX models. This proves package/API smoke only.

## Component map

| Tian PTC function | Cornerstone si220 candidate | Mapping status |
|---|---|---|
| 450 nm × 220 nm SOI strip waveguide | `strip_cband` cross-section | Nominal width/thickness match; exact optical mode/process equivalence not established |
| MZI 1×2 input coupler | `cells.mmi1x2` | Available; Cornerstone Run-50 geometry/model, not CUMEC geometry |
| MZI 2×2 output coupler | `cells.mmi2x2` | Available; Cornerstone Run-50 geometry/model, not CUMEC geometry |
| One internal heater | `cells.mzi_heater_loop` | Available; one upper-arm heater only |
| 200 µm × 2 µm heater geometry | `cells.heater(length=200, width=2)` | Geometry primitive exists; does not by itself provide a characterized thermal transfer model |
| Three independent phase controls per MZI | custom composition of one external and two arm heaters | Not implemented; port placement, routing, and independent transfer models remain to be verified |
| Output grating couplers | `cells.grating_coupler_rectangular` | Candidate exists; not Tian's original CUMEC grating |
| Balanced photodetection | paired output ports / external power measurement | The PDK manifest does not establish an integrated balanced-photodiode macro/model |

Public upstream sources:
- [MZI cells](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/cells/mzis.py)
- [Heater cells](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/cells/heaters.py)
- [MMI cells](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/cells/mmis.py)
- [Grating couplers](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/cells/grating_couplers.py)
- [Layer definitions](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/layers.yaml)
- [Technology stack](https://github.com/gdsfactory/cspdk/blob/v2.1.0/cspdk/si220/tech.py)

## Important process differences

Tian reports a 200 µm × 2 µm × 120 nm TiN heater. The Cornerstone si220 technology source defines a TiN heater layer stack with a default thickness of 150 nm. The geometry helper can draw a 200 µm × 2 µm heater, but that does not make the resulting heater electrically or thermally equivalent to Tian's device.

The Cornerstone `mzi_heater_loop` cell is documented as an MZI with one heater on the upper arm. Tian's MZI requires three independent phase controls: one external and two internal. The Cornerstone cell is therefore a useful starting primitive, not a complete drop-in PTC MZI.

The package includes compact models for selected MMIs, heaters, and a one-heater MZI. The existing EIS manifest explicitly records that these models do not establish a characterized three-heater Tian macro, a thermal-crosstalk matrix, or an integrated balanced detector.

## Proposed bounded mapping experiment

Before attempting the 10×1 array, build one candidate three-phase-shifter MZI and prove the following independently:

1. Three distinct electrical control ports exist and map one-to-one to external, internal-A, and internal-B heaters.
2. The optical path is continuous through the 1×2 MMI, both arms, and 2×2 MMI.
3. Each heater's geometry, layer, pad, and route is obtained from the selected PDK library or explicitly documented adapter—not guessed from layer numbers.
4. The MZI's optical port semantics agree with the Lean ideal transfer contract.
5. Each heater transfer is labelled as measured, fitted, simulated, or assumed. No ideal model is presented as a measured response.
6. The exported test-cell OASIS reopens with stable hierarchy, layers, and geometry hashes.
7. DRC and connectivity checks are run only with a verified, supported deck/flow; a KLayout round-trip alone is not DRC.

Only after this cell passes should the design be replicated into ten A-side MZIs plus one shared B-side MZI.

## Rights and publication boundary

The cspdk package's MIT license does not establish rights to redistribute foundry-derived process data, submit a design to the foundry, or use a particular MPW. The current EIS manifest therefore limits this candidate to internal engineering evaluation pending written rights/access confirmation. No confidential PDK content is to be copied into the public repository.

## Decision

**Cornerstone si220 is a technically plausible open reference backend for an internal functional reconstruction, but it is not yet a qualified or authorized EIS fabrication backend.** The next engineering object is the three-heater MZI test cell, not the full array and not a claim of a Tian-equivalent chip.
