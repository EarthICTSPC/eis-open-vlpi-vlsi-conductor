# EIS-KKA-001B — MZI Macro-Cell Contract

**Status:** topology-level component contract; physical geometry unknown  
**Source:** Tian et al. (2025), Supporting Information Fig. S1 and main-paper Methods.

## Functional topology

Each MZI macro-cell has one external phase-shifter function, one 1×2 MMI splitter, two internal phase-shifter functions (one on each interferometer arm), and one 2×2 MMI combiner. The three phase-shifter functions are independently addressable in the source description. The 11 MZI count therefore corresponds to 33 phase-shifter functions.

## Abstract ports

- in: optical input to the MZI macro-cell.
- out: selected optical output field used by the PTC functional schematic.
- out_complement: complementary output retained as an explicit port in the physical component implementation.

The top-level PTC netlist may connect the source-schematic selected output as out. The complementary port must remain available and may not be silently deleted from the underlying physical MMI implementation.

## Internal abstract graph

in → external_phase_shifter → MMI_1x2 → {upper_arm_phase_shifter, lower_arm_phase_shifter} → MMI_2x2 → {out, out_complement}

This graph captures functional topology only. Exact phase-shifter placement, MMI port ordering, optical phase convention, routing lengths and reference planes must be fixed in the component implementation contract before simulation.

## Unknown physical parameters

MMI length/width, access taper, port pitch, waveguide gap, arm lengths, bend radii, heater offsets, metal routing, process stack, refractive-index dispersion, loss, wavelength and polarization are source_unknown until supported by source data or explicitly designated eis_assumed for a separate exploratory study.

The source-reported waveguide cross-section and TiN heater dimensions are not enough to determine these unknowns.

## Acceptance

An implementation may be called a Tian-inspired EIS exploratory MZI cell when its topology follows this contract and all non-source geometry values are labelled eis_assumed.

It may not be called a Tian reproduction or a foundry-qualified cell until its geometry and materials are independently supported and the relevant physical evidence gates pass.
