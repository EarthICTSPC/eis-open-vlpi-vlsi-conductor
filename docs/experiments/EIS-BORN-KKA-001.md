# EIS-BORN-KKA-001 — Born Attention and KKA Computational Contract

**Status:** Proposed bounded software/formal investigation  
**Branch:** `eis-born-kka-001`  
**Parent:** EIS-KKA-SOI-001 scalar field/interference contract  
**Source under study:** Tongloy, Pongsopa & Jomtarak, *Reading Why: Born-Measured Attention with Exact Word Evidence on Light and Qubits*, arXiv:2611.05355 (2026)  
**Hardware/foundry authorization:** None  
**Fabrication commitment:** None

## 1. Question and decision

Can the Born-measured attention architecture be represented using EIS's existing KKA/VLPI mathematical primitives, and does a physically credible implementation improve **total system energy per accepted useful transformation** on a frozen workload?

This investigation tests compatibility and identifies the missing operations. It does not assume that the Born Transformer runs on Tian et al.'s Photonic Transformer Chip (PTC), that Born attention is equivalent to Tian KKA, or that an optical-operation efficiency implies a system-level energy advantage.

**Decision sought:** (a) mathematically equivalent using existing KKA primitives; (b) implementable with explicitly identified additional measurements/operations; or (c) not a useful fit. A negative result is acceptable and should stop further work unless it identifies a separately justified experiment.

## 2. Source-faithful mathematical target

For query vector (q_i) and key vector (k_j), define the complex overlap

[
z_{ij} = \langle q_i,k_j\rangle
       = \sum_{r=1}^{d} q_{i,r}\,\overline{k_{j,r}}.
]

The Born score and row-normalized attention weight are

[
s_{ij}=|z_{ij}|^4=(|z_{ij}|^2)^2,
\qquad
w_{ij}=\frac{s_{ij}}{\sum_{t=1}^{m}s_{it}},
]

where the denominator must be strictly positive. A zero denominator is an invalid/undefined attention row for this contract; do not silently clip, add epsilon, or invent a fallback distribution.

The source's measured bilinear feed-forward operation is represented at the scalar level as

[
r_c=\operatorname{Re}(x_c y_c),
\]

with the full paper-specific projection, gain, measurement and re-modulation details kept separate from this scalar identity.

The EIS scalar KKA contract is

[
X(a,b)=2\operatorname{Re}(a\overline b).
]

Consequently,

[
X(x,\overline y)=2\operatorname{Re}(xy)=2r.
]

This identity is a mathematical bridge for the bilinear readout, not proof that a physical KKA cell supplies conjugation, correct scaling, the complete vector overlap, or the Born score.

## 3. Existing KKA boundary and expected gaps

EIS-KKA-SOI-001 v1.0 defines dimensionless complex field envelopes, independently supplied complex path transfers, total intensity, and the **signed** balanced cross-term (2\operatorname{Re}(a\overline b)). Its Lean source proves scalar identities and bounds. It explicitly does not define full tensor attention, an actual device transfer function, a detector, or a KKA/SoftMax equivalence.

The Born operation adds requirements beyond one scalar cross-term:

1. **Complex overlap:** compute both quadratures of (z_{ij}), not only one signed real projection.
2. **Magnitude square:** form (|z_{ij}|^2=(\operatorname{Re}z_{ij})^2+(\operatorname{Im}z_{ij})^2).
3. **Fourth power:** multiply the intensity by itself to form (|z_{ij}|^4).
4. **Row reduction and normalization:** sum all key scores and divide by a common positive row denominator.
5. **Value aggregation:** apply the resulting weights to value vectors under an explicitly stated numerical and physical interface.

The balanced cross-term can measure a selected quadrature against a coherent reference. A second reference phase (or another independently justified quadrature-recovery method) is required to recover the orthogonal quadrature. The intensity-square and row normalization are additional operations; they must not be described as being supplied automatically by the scalar Tian KKA cell.

## 4. Work packages and deliverables

| WP | Investigation | Deliverable | Exit condition |
|---|---|---|---|
| 1 | Formalize complex overlap, fourth-power score, positive-denominator row normalization, and score bounds | Lean4/Mathlib definitions and proofs | Lean build and axiom audit pass; no `sorry` or custom axioms |
| 2 | Compare Born overlap/score with Tian KKA signed interference | Equation-level equivalence/gap ledger | Every required quadrature, conjugation, scaling, multiplication and reduction is classified |
| 3 | Formalize measured bilinear feed-forward and its KKA scalar relationship | Lean theorem plus executable reference tests | Algebraic identity proved; physical interface requirements remain explicit |
| 4 | Account for optical and electronic energy/loss overhead | Parameterized wall-plug energy ledger and sensitivity inputs | All terms are explicit; unknowns remain unknown; no energy advantage claimed without matched evidence |

## 5. Energy and loss boundary

For one frozen workload run, the candidate energy ledger must separately record, in joules:

- laser electrical wall-plug input (including source efficiency);
- optical launch, coupling, propagation and other optical losses, with the electrical replacement/replenishment cost accounted for exactly once;
- modulator and driver energy;
- detector, transimpedance/readout and conversion energy;
- electronic feedback, gain, normalization and control energy;
- phase-setting, calibration and recalibration energy (with any amortization rule declared);
- memory energy;
- data-movement/interconnect energy;
- other compute/control electronics required by the candidate;
- relevant cooling and power-delivery overhead.

The comparison baseline must use the same workload, accepted-output criterion, batch/sequence shape, precision or quality requirement, throughput/latency target, and system boundary. Report both total joules and

[
E_{\mathrm{accepted}}=
\frac{E_{\mathrm{system,wall\text{-}plug}}}
{N_{\mathrm{accepted\ useful\ transformations}}}.
]

Do not double-count optical loss and its electrical replacement energy. Do not count recovered energy as negative wall-plug energy unless a measured, boundary-consistent return to the external supply is demonstrated. Internal circulation is not external energy recovery.

## 6. Workload and acceptance freeze

Before any comparative performance or energy claim, freeze:

- task and dataset/version/license;
- train/validation/test split and seeds;
- tokenizer, sequence length, batch and head dimensions;
- reference model and Born model parameter counts/configuration;
- accepted-output definition and quality metric/non-inferiority margin;
- precision/numerical error limits;
- latency/throughput target;
- energy measurement boundary and instrumentation/calibration method.

No quality threshold, energy threshold, or favorable workload may be selected after seeing comparative results. If no defensible workload/acceptance contract is frozen, WP1–WP3 may proceed as mathematical work, but WP4 remains a parameterized accounting model only.

## 7. Evidence labels and claim boundary

Use the repository's evidence discipline:

- **E0 — literature/specification:** source statements and extracted equations.
- **E1 — analytic:** hand derivations and mathematical identities.
- **E2 — software:** deterministic reference code and unit tests.
- **E3 — formal:** Lean proofs and axiom audit.
- **E4 — simulation:** reproducible device/system simulation with pinned models and configuration.
- **E5 — measurement:** calibrated physical measurements with raw data and provenance.

This initial branch can produce E1–E3 evidence only. It does not claim E4/E5.

Explicit non-claims:
- no reproduction of the complete Tongloy et al. optical or quantum experiments;
- no claim that the model runs on Tian's fabricated PTC;
- no proof of end-to-end Born attention on Tian KKA hardware;
- no assumption that a single balanced detector output yields complex overlap magnitude;
- no foundry PDK qualification, DRC/LVS, FDTD, FlexCompute job, fabrication, MPW booking or lab measurement;
- no accuracy, latency, TOPS/W, joules/accepted-transformation or CO2e advantage.

## 8. Staged gates

- **G0 — Contract review:** approve equations, types, conventions, source mapping and non-claims.
- **G1 — Formal core:** prove Born score non-negativity, denominator positivity precondition, normalized row sum and weight bounds.
- **G2 — KKA bridge:** prove the scalar bilinear identity and document the additional quadrature/intensity/reduction operations.
- **G3 — Executable reference:** Python tests agree with exact definitions on deterministic and randomized finite cases.
- **G4 — Energy ledger:** schema/model and tests complete; no numerical advantage asserted until workload and measurement inputs exist.
- **G5 — Continue/stop decision:** decide whether a workload-frozen software comparison is justified. Any optical simulation or external compute requires a separate explicit authorization and pinned model/cost preflight.

## 9. Immediate implementation

This branch adds a Lean formal core, deterministic Python reference/tests, and an energy-ledger model. It intentionally does not add a physical device model or invoke a simulator. Review and passing CI are required before calling the formal/software artifacts verified.
