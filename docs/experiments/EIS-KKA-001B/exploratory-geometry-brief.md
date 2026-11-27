# EIS-KKA-001B — Tian-Inspired EIS Exploratory Geometry

**Status:** topology specification; exploratory only; not a foundry layout  
**Source basis:** Tian et al., Photonic Transformer Chip: Interference Is All You Need (2025), Fig. 1d, Fig. 2a and Supporting Information Fig. S1.

## What the paper actually shows

The main-paper Fig. 2a provides a chip micrograph with a laser input, repeated MZI-A channels, an MZI-B region, electrical heater routing/pads, and optical/detector regions. The micrograph is useful for topology and physical organization, but it is not a dimensioned mask: it does not provide reliable coordinates, MMI dimensions, routing widths, layer stack, or reference-plane definitions.

Supporting Information Fig. S1 is the clearest functional schematic for one output channel. It shows a laser input followed by an MMI split; two MZI branches, one carrying the input-side field E_I and one carrying the weight-side field E_W; each MZI has one external phase shifter and two internal phase shifters; each MZI uses an MMI splitter and an MMI combiner; and the two resulting fields enter a final MMI and balanced photodetector (BPD).

The main paper describes the PTC as a left portion split into M channels and modulated as A_i(t), while a right portion is modulated as B(t) and broadcast to M ports. It reports 11 MZIs total, with 10 A_i channels and a shared B-side MZI visible in the chip micrograph; the 10-channel interpretation is consistent with the described one-output unit and Fig. 2a, but the exact physical broadcast routing is not dimensioned.

The paper's Methods identify one 1×2 MMI and one 2×2 MMI per MZI. The source reports a 450 nm × 220 nm waveguide cross-section and TiN heaters 200 µm × 2 µm × 120 nm. Those are source facts, not a complete process stack or a complete set of layout dimensions.

## EIS exploratory system topology

The first EIS geometry is a **10-output logical architecture**:

1. Laser input.
2. Input MMI split into A-side and B-side signal paths.
3. A-side fanout tree: logical 1-to-10 distribution to A channels.
4. Ten parameterized A-side MZI cells.
5. One shared B-side MZI cell.
6. B-side broadcast tree: logical distribution of B to ten output channels.
7. Ten output MMIs, one per output.
8. Ten balanced photodetectors, one per output.

Each MZI macro-cell has three phase-shifter functions: one external phase shifter and two internal arm phase shifters. It contains a 1×2 MMI splitter and a 2×2 MMI combiner. Therefore the 11 MZI cells account for 33 phase shifters, consistent with the source-reported count.

The A-side fanout and B-side broadcast are represented as **logical fanout components**. Their physical MMI-tree decomposition, placement and routing remain unknown and are not guessed.

## Classification rules

| Item | Label |
|---|---|
| 11 MZIs / 33 phase shifters | tian_reported |
| MZI cell uses one 1×2 and one 2×2 MMI | tian_reported |
| 450 × 220 nm cross-section | tian_reported |
| TiN heater dimensions | tian_reported |
| 10 A-side channels and one shared B-side MZI | source_interpretation |
| Explicit 10-output graph and instance names | eis_architecture_choice |
| Logical fanout trees | eis_architecture_choice; physical decomposition unknown |
| MMI lengths, widths, tapers, gaps and port spacing | source_unknown |
| Material stack, dispersion and loss | source_unknown |
| Wavelength and selected polarization | source_unknown |
| Physical coordinates, routing and layer assignment | source_unknown |
| Any illustrative placement or dimensions added later | eis_assumed |
| Any Tidy3D outputs | simulated |

## What this geometry is — and is not

This is an explicitly labelled EIS exploratory architecture derived from the paper's schematic and micrograph. It is suitable for Lean4 netlist type development, graph validation, lowering into a Python component registry, schematic construction in PhotonForge, and later replacement of abstract fanout/MMI cells with sourced geometry and simulation models.

It is not a reverse-engineered Tian GDS/OASIS file, a CUMEC process replica, a fabrication-ready layout, a Tidy3D simulation, or a claim that the micrograph supplies exact dimensions.

## Geometry gate

The next geometry increment is not to guess MMI dimensions. It is to define component interfaces and a typed hierarchical netlist, then let Python/PhotonForge instantiate only components for which EIS has an explicit geometry/model implementation. Unknown cells must fail closed rather than be replaced by generic devices silently.
