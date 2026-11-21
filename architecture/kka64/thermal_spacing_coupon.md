# EIS-KKA-THERMAL-COUPON-001 — SOI Spacing-First Thermal Interaction Coupon

**Design principle:** Use ordinary layout area and separation as the first thermal-crosstalk mitigation. Do not introduce special trenches, substrate undercut or complex thermal processing unless the spacing-first SOI design fails predefined acceptance limits.

**Parent workstream:** #66 (64×64 KKA scale-up)  
**Phase-control work:** #71  
**Energy accounting:** #72  
**Related design note:** [EIS-KKA-PHASE-001](https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/blob/eis-kka-phase-soi-lessons-001/architecture/kka64/phase_control_soi_lessons.md)

## 1. Objective

Characterize how much physical separation is needed between thermo-optic phase-shifter/PTC elements to keep unwanted phase perturbation within the KKA error budget. The coupon is deliberately simple: standard SOI process, standard foundry-approved phase shifters, multiple spacings, no special thermal-isolation process in the baseline.

This specifies a design and measurement plan. It does not claim an EIS coupon has been fabricated or measured.

## 2. Thermal boundary

The optical computation is not assumed to create GPU-like instantaneous transistor hotspots. If thermo-optic phase controls are used, the electrical heaters create local heat. Neighboring phase-sensitive elements can be perturbed, and simultaneous active heaters can create a steady-state temperature field. Test both one-heater and simultaneous-heater conditions.

## 3. Exploratory spacing sweep

Use heater/phase-shifter center-to-center pitch as the controlled variable:
- 25 µm
- 50 µm
- 100 µm
- 200 µm
- 400 µm
- 1 mm isolated reference, if coupon area permits.

These are **test points, not asserted safe distances or final design rules**. Foundry spacing, metal routing, optical routing, bend radii, keep-outs and DRC constraints take precedence. Keep device and heater geometry constant across the sweep.

For each pitch, characterize driven phase and complex optical transfer; induced phase/amplitude shift in each neighbor; nearest- and next-nearest-neighbor effects; crosstalk versus heater power and simultaneous activation pattern; chip/ambient temperature and wavelength; heating/cooling transients and steady state; drift, hysteresis, repeatability and uncertainty.

Define normalized phase crosstalk as C_ij = |Δφ_j|/|Δφ_i| for heater i driving and monitored phase-sensitive element j. Also report absolute induced phase error; a ratio alone can hide its significance.

## 4. Simple layout variants

A. **Spacing-only baseline:** identical phase-control elements at the pitch sweep, ordinary foundry-qualified SOI stack and cladding.

B. **Routing-aware spacing:** compare heater routing and shared-return geometry without changing optical device geometry. Record metal density and current-return topology.

C. **Optional isolation comparison:** only if spacing-only fails, add foundry-authorized trench/isolation variants as a second-stage experiment. Do not make trench/undercut a prerequisite.

## 5. 64×64 area arithmetic — logical scores are not physical PTC count

The EIS 64×64 contract currently means 64 queries × 64 keys = 4,096 logical pairwise score relationships. It does **not** establish that 4,096 separate PTC/MZI cells are required. Physical mapping, time multiplexing, broadcast/fanout and detector sharing remain architectural decisions.

For an illustrative square grid of 64 physical sites per side, with site pitch p, active grid side is approximately 64p and area approximately (64p)^2, before routing margins, IO, couplers, detectors, control electronics, guard bands and packaging:

| Illustrative pitch | Grid side | Idealized grid area |
|---:|---:|---:|
| 25 µm | 1.6 mm | 2.56 mm² |
| 50 µm | 3.2 mm | 10.24 mm² |
| 100 µm | 6.4 mm | 40.96 mm² |
| 200 µm | 12.8 mm | 163.84 mm² |
| 400 µm | 25.6 mm | 655.36 mm² |

These are geometric scenarios only, **not an EIS die-area estimate**. A 64×64 logical attention tile may map to fewer physical cells through time multiplexing/reuse, or to a different geometry. Compute actual area from placed cell dimensions, routed paths, keep-outs, pads and foundry rules once the physical mapping is frozen.

## 6. Acceptance

Choose the **smallest area / shortest pitch** that meets predeclared requirements under simultaneous-heater operation:
- KKA output/attention error remains within system tolerance.
- Induced phase and amplitude perturbations remain within device contract.
- Calibration recovers residual error without excessive measurement/time/energy overhead.
- Drift and repeatability are acceptable over intended operating interval.
- Static phase-control power and total system energy remain inside #72 budget.

The criterion must be defined in KKA output/attention-quality terms, not an arbitrary thermal-crosstalk percentage alone. Record uncertainty and separate measured, simulated and assumed values.

## 7. Economics

Compare incremental photonic area/routing cost of wider spacing against special process steps, yield risk, calibration complexity, phase-control power, thermal stabilization, packaging and optical loss. Do not assume photonic fab economics are universally lower than a 3 nm GPU roadmap: build a matched cost model from actual wafer/MPW pricing, die area, yield, packaging, test, control electronics, volume and system performance.

## 8. Deliverables

1. Parametric KLayout/gdsfactory-compatible SOI coupon layout.
2. Foundry-rule and connectivity review; no fabrication release until approved.
3. Measurement protocol and raw-data schema.
4. Thermal interaction matrix and spacing-versus-KKA-error plot with uncertainty.
5. Recommended minimum spacing and 64×64 area estimate after architecture mapping is frozen.
6. Go/no-go: spacing-only, spacing plus calibration, or investigate isolation structures.

No paid simulation, MPW, fabrication, packaging or lab measurement is authorized by this issue. Each requires separate EIS approval and a costed plan.

## 9. References

1. Maxime Jacques, Alireza Samani, Eslam El-Fiky, David Patel, Zhenping Xing, and David V. Plant, “Optimization of thermo-optic phase-shifter design and mitigation of thermal crosstalk on the SOI platform,” *Optics Express* 27(8), 10456–10471 (2019). DOI: https://doi.org/10.1364/OE.27.010456.
2. Shengping Liu et al., “Thermo-optic phase shifters based on silicon-on-insulator platform: state-of-the-art and a review,” *Frontiers of Optoelectronics* 15, 9 (2022). DOI: https://doi.org/10.1007/s12200-022-00012-9.
3. Ye Tian et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025). DOI: https://doi.org/10.1186/s43074-025-00182-7.