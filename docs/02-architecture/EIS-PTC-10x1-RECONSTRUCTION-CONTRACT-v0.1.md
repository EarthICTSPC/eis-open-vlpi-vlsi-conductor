# EIS-PTC-10x1-RECONSTRUCTION-001
## Source-faithful reconstruction contract for Tian et al.'s PTC prototype

**Status:** source-extracted and formally specified at the ideal transfer/count level; technology mapping and physical layout pending  
**Target:** functional reconstruction of the published 10×1 KKA PTC demonstrator, not a mask-identical reproduction  
**Parent work:** [#47](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/47), [#56](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/56), [#60](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/60), [#61](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/issues/61)

## 1. Primary source

Tian, Y., Xiang, S., Guo, X. et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025), DOI: [10.1186/s43074-025-00182-7](https://doi.org/10.1186/s43074-025-00182-7).

The source of the detailed hardware topology and transfer equations is the article's 38-page Supporting Information, especially SI-1, Fig. S1 and Eqs. (S2)–(S4), and SI-3/SI-4 for device characterization and calibration.

## 2. Reconstruction target

The first physical target is the **published 10×1 prototype**, not the 512×512 projection.

The published prototype is described as:
- ten output channels, with ten input-side MZIs A1…A10;
- one shared weight-side MZI B, whose output is broadcast to the ten channels;
- eleven MZIs total;
- three thermal phase shifters per MZI: one external and two internal;
- thirty-three phase shifters total;
- a laser input split into the A and B paths;
- an A-side 1×N split tree and a B-side broadcast tree;
- an MMI split/recombine structure within each MZI;
- an output MMI and balanced-detection pair for each output channel.

The 10 A-side MZIs plus one shared B-side MZI is the source-consistent interpretation of the paper's Ai (i=1…10) and broadcast B, and its stated 11 MZIs / 33 phase shifters. The machine-readable topology is in `architecture/ptc10x1/topology.json`.

## 3. Normative ideal MZI transfer

For one MZI, let the controls be:
- theta_e: external phase shifter;
- theta_a: internal phase shifter on arm A;
- theta_b: internal phase shifter on arm B.

The source SI-1 expressions for the signed output field amplitude and phase are:

[
E_{out} = rac{E_{in}}{sqrt{2}}
cosleft(rac{	heta_b-	heta_a}{2}+rac{pi}{4}ight)
expleft[jleft(	heta_e+rac{	heta_a+	heta_b}{2}+rac{pi}{4}ight)ight].
]

The signed cosine must be retained. Replacing it with an absolute value changes the field phase when the cosine is negative.

For paired input-side and shared weight-side MZIs, SI-1 Eq. (S4) gives the ideal balanced-detection observable:

[
P_{out}=2E_AE_Bsinleft(
	heta_{e,A}-	heta_{e,B}
+rac{	heta_{a,A}+	heta_{b,A}}{2}
-rac{	heta_{a,B}+	heta_{b,B}}{2}
ight),
]

where E_A and E_B are the signed output amplitudes after their respective MZI transfers.

The Lean module `EISKKA/PTCPrototype.lean` encodes these source equations and proves the integer topology invariants (10 A-side MZIs, one shared B-side MZI, 11 total MZIs, 33 phase shifters). This is formal evidence for the ideal equations as encoded and for the stated counts—not proof of a fabricated device.

## 4. Published physical parameters

| Item | Tian et al. source value | Evidence interpretation |
|---|---:|---|
| Platform | SOI; fabricated on CUMEC CSiP-180AL | Source-reported process, not an EIS-selected backend |
| Waveguide cross-section | 450 × 220 nm² | Source-reported geometry |
| TiN heater | 200 µm × 2 µm × 120 nm | Source-reported geometry |
| Heater sheet resistance | 12 Ω/sq | Main article |
| Heater resistance | around 1 kΩ | SI-3 measured population description |
| Heater phase-shift efficiency | about 20 mW | SI-3 typical value |
| Heater trace width | 15 µm; wider shared-ground traces | Main article |
| Temperature stabilization | 25 ± 0.2 °C | Main article |
| High-speed demonstration | 5 GBaud | Main article |

A useful internal consistency check is 200/2 = 100 squares; at 12 Ω/sq this gives a nominal 1.2 kΩ before geometry/contact corrections, consistent in order with the SI's “around 1 kΩ” statement. This is a derived check, not a replacement for measured heater data.

The SI reports individual heater calibration by fitting an optical-power response of the form y = a cos(bV²/R + c) + d, and a non-ideal interference model that includes residual offset and thermal cross-coupling. Those fitted coefficients are device/channel-specific. They must not be replaced by a universal assumed phase-voltage law.

## 5. Correct-by-construction design chain

The required chain is:

1. **Source extraction:** preserve the article/SI source references and separate stated facts from inferred topology.
2. **Formal transfer model:** Lean4 definitions for the three phase controls, signed MZI field amplitude, output phase, and balanced-detection observable.
3. **Topology contract:** validate channel count, MZI roles, shared-B fanout, phase-shifter count, optical port directionality, and detector pair count.
4. **Technology mapping:** map each logical component to a selected, authorized SOI PDK cell and named ports. No generic cell is silently promoted to “Tian-equivalent.”
5. **Geometry generation:** instantiate the selected PDK cells; use technology-aware routing and actual layer/cross-section definitions.
6. **Independent checks:** geometry/grid checks, DRC, optical connectivity/netlist extraction, and LVS where a supported electrical/photonic flow exists. Report each separately.
7. **OASIS generation:** serialize using a pinned KLayout or other established layout engine; reopen independently; compare hierarchy, layers, ports/netlist, and canonical geometry hashes.
8. **Evidence manifest:** bind the artifact to the Lean contract, topology, PDK identity, toolchain, generator configuration, check logs, and output hash.

A successful OASIS round-trip is not DRC, LVS, foundry acceptance, fabrication, or measured KKA performance.

## 6. Known gaps — do not invent

The paper and SI do **not** provide a public, machine-readable mask layout or enough data for a mask-identical reconstruction. The following remain unprovided or unverified in the public source:
- exact die dimensions and component coordinates;
- exact MMI geometries and detailed port coordinates;
- splitter-tree topology and exact branching geometry;
- waveguide bend radii, routing geometry, and layer/datatype map;
- grating-coupler geometry and complete fiber-array pitch;
- pad coordinates, bond-pad geometry, metal/via stack, and die/package drawing;
- full foundry design rules and qualified layout verification deck;
- complete per-heater raw calibration data and thermal interaction matrix.

Consequently, the first EIS result must be described as a **source-faithful functional reconstruction on an explicitly identified SOI backend**, not as a bit-for-bit reproduction of Tian's CUMEC mask set.

## 7. Backend decision

The original device used CUMEC CSiP-180AL. That process is a source fact, not an EIS recommendation or authorization to use that foundry.

EIS's reconstruction must keep the logical PTC architecture technology-independent until a candidate SOI PDK is selected and its access, license, process rules, device inventory, and redistribution rights are confirmed. The current Cornerstone si220 package is an evaluated reference candidate only; its default MZI and compact models are not the Tian three-heater MZI macro. GF/AMF or TSMC mapping requires separate authoritative process evidence.

No confidential PDK material is to be placed in the public repository.

## 8. Current exit status

- Source extraction: **complete for the facts and equations listed above**.
- Ideal Lean transfer/count contract: **added on the reconstruction branch; CI validation pending**.
- Typed topology: **added as a versioned machine-readable artifact; schema/test integration pending**.
- PDK component mapping: **not complete**.
- Physical geometry generation: **blocked pending PDK selection and component mapping**.
- DRC/LVS: **not run**.
- OASIS artifact: **not generated**.
- Simulation, fabrication, and measurement: **not performed or authorized**.

The next action is the component/port inventory for the chosen SOI backend—not an invented geometry or an early OASIS export.
