# EIS-CRC-FIRST-PAIRWISE-001 — Analytical Comparator Model v1

Status: source-backed analytical reference; not a validated compact model. FDTD/EM remains NO-GO until workload budgets are approved.

## Sources and what they establish

- PRISM public repository: https://github.com/hyoseokp/PRISM. It describes optical MRR score generation and electronic top-k selection. Its README states that no chip has been fabricated and that the photonic latency/energy figures are simulated, not measured. Its ~9 ns and ~2.3 nJ/query figures are system context, not comparator requirements or comparator measurements.
- Tian et al., PhotoniX 6, 45 (2025), https://doi.org/10.1186/s43074-025-00182-7. The paper describes KKA interference and balanced photodetection on an experimental silicon photonic transformer. It does not demonstrate a PRISM-score pairwise comparator or detector-free winner token.
- SiEPIC EBeam PDK: https://github.com/SiEPIC/SiEPIC_EBeam_PDK. It provides exploratory MZI, ring, coupler, layout and circuit-simulation examples; it is not the intended Ligentec/X-FAB SiN/TFLN PDK.
- System accounting review: https://doi.org/10.1186/s43074-021-00042-0.

## Behavioral domain

The current software convention is normalized scores sA,sB in [0,1] and synthetic indifference gap g=0.05. This is not claimed to represent the PRISM score distribution or an application-derived minimum gap. A software score must not be silently equated with optical power.

## Interface A analytical baseline

Let score-to-power encoding be P_i = P0 + Ks*s_i + e_i, for i=A,B. P0 is an offset, Ks is the power change per normalized score unit, and e_i is encoding/calibration error. These are symbolic, not assumed numerical values. Require P_i >= 0 throughout the operating domain.

Differential power: DeltaP = P_A - P_B = Ks*(s_A-s_B) + (e_A-e_B).

For a photodiode with responsivity R, the ideal differential current is DeltaI = R*DeltaP. Model the observed decision variable as z = R*DeltaP + b + n, where b is receiver/calibration offset and n is noise with an explicitly stated bandwidth and statistical model. Decide A only above +T_I, B only below -T_I, otherwise INDETERMINATE. Invalid calibration or out-of-envelope inputs return FAULT. This is an architecture-level analog optoelectronic model, not a compact model.

A conservative deterministic separation condition outside the frozen score gap is Ks*g > E_DeltaP + P_T, where E_DeltaP bounds differential encoding error and P_T bounds input-referred threshold/offset uncertainty in power units. For g=0.05, this becomes 0.05*Ks > E_DeltaP + P_T. The condition cannot be evaluated until units, calibration, and justified parameter bounds are supplied.

## Energy and latency boundary

E_cmp = E_source + E_encode + E_control + E_receiver + E_decision + E_token + E_cal,amortized.

t_cmp = t_encode + t_prop + t_decision + t_recovery + t_token.

Declare every included term, reference plane, duty cycle, and amortization rule. Report throughput separately from latency. Optical-core-only energy must be labeled as such.

## B1 detector-free optical status

The reviewed sources do not establish a detector-free physical mechanism that compares both score orderings, identifies the indifference band, and emits an A/B winner token. KKA's interference operation is not evidence of that comparator function. A passive MZI/resonator response or a thresholding element alone is not a complete winner-decision model.

- Interface A analog optoelectronic: symbolic model defined; parameters not yet sourced.
- B1 detector-free optical comparator: decision mechanism not established; BLOCKED.
- Integrated PRISM-to-comparator-to-KKA service: not demonstrated.

## Parameter ledger

| Parameter | Current status | Required evidence |
|---|---|---|
| Score range [0,1] | MOCKED_FOR_EXPLORATION | Representative PRISM score traces and normalization |
| Gap g=0.05 | MOCKED_FOR_EXPLORATION | Workload-derived ranking margin/tie policy |
| P0, Ks | UNKNOWN | Encoding design and calibration or bounded specification |
| Differential encoding error | UNKNOWN | Calibration/drift budget and defensible interval |
| Responsivity R | UNKNOWN | Identified detector/process/wavelength datasheet or measurement |
| Receiver offset/noise | UNKNOWN | Circuit model/datasheet, bandwidth and temperature |
| Threshold T_I | UNKNOWN | Receiver architecture and threshold/hysteresis characterization |
| B1 optical transfer/nonlinearity | UNKNOWN | Specific mechanism and source-backed model |
| Comparison energy and latency | UNKNOWN | Complete component-level ledger and timing evidence |
| Process/temperature/wavelength envelope | UNKNOWN | Target PDK data and intended operating conditions |

## Gate before FDTD/EM

1. Obtain a representative PRISM score trace and freeze normalization, rank-loss tolerance, and minimum relevant score gap.
2. Select Interface A as the baseline or specify B1 as a separate candidate; do not blend them.
3. Populate all parameters with sourced values or explicit uncertainty intervals. Unknown remains unknown.
4. Run bounded analytical sweeps over both orderings, gap edges, imbalance, drift, and uncertainty corners.
5. Independently review dimensional consistency, winner identity, noise assumptions, and energy/latency boundaries.
6. Obtain EIS owner approval of the companion physical-budget register.
7. Only then authorize targeted physics simulation for a named unresolved EM question.

Current disposition: NO FDTD/EM authorization.