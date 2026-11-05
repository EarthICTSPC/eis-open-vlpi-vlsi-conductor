# EIS-CRC-FIRST-PAIRWISE-001 — Physical Budget Register and Approval Record

**Version:** BUDGET-v1-proposal  
**Status:** PROPOSED FOR EIS OWNER APPROVAL — NOT YET APPROVED  
**Simulation authorization:** NO-GO until approval is recorded and the model gate passes.

## 1. Purpose and boundaries

This register prevents component-level or simulated figures from being treated as accepted system budgets. It defines two separate boundaries:

- **Pairwise primitive boundary:** encoded score inputs through a usable A/B winner token, including any source, encoding, control, decision, regeneration, and calibration energy required by the chosen architecture.
- **Workload service boundary:** PRISM score generation plus all required ranking/selection and output-token delivery for the intended K/V block selection workload. This boundary is needed to determine whether replacing or augmenting electronic top-k selection is beneficial.

The pairwise primitive must be budgeted against the workload service boundary; a low-energy primitive is not useful if the cascade, calibration, routing, or control costs dominate.

## 2. Source-backed facts (not approved requirements)

| Source statement | What it supports | What it does not support |
|---|---|---|
| PRISM repository describes 4–6 bit score/rank precision as sufficient for its intended selection approach. | Use 6-bit score/rank resolution as a conservative *proposal for workload evaluation*, then validate on real score traces. | It does not prove a 6-bit pairwise optical comparator meets quality requirements. |
| PRISM repository reports ~9 ns selection and ~2.3 nJ/query dynamic energy as device-physics-simulation figures, with explicit limitations and excluded thermal stabilization overhead. | A candidate workload service can be compared against these reported simulated figures as contextual reference points. | These are not measurements, not approved EIS targets, and not per-comparator budgets. They cannot be allocated directly to each pairwise comparison. |
| PRISM README states no chip has been fabricated; its photonic performance values are simulated. | Keep those metrics labelled SIMULATED and do not claim physical validation. | Does not establish real hardware energy, latency, yield, or drift. |
| KKA paper DOI 10.1186/s43074-025-00182-7 describes an experimental photonic transformer and balanced photodetection. | Supports that interference and detected outputs are a physically investigated computing primitive. | Does not establish PRISM score comparison, top-k, detector-free winner tokens, or comparator budgets. |
| SiEPIC EBeam PDK documents MZI/ring/coupler examples and circuit-simulation flows. | Supports exploratory layout/circuit-model scaffolding if clearly labelled as an alternate PDK. | Does not supply transferable Ligentec/X-FAB SiN/TFLN comparator parameters. |

Sources: https://github.com/hyoseokp/PRISM ; https://doi.org/10.1186/s43074-025-00182-7 ; https://github.com/SiEPIC/SiEPIC_EBeam_PDK ; https://doi.org/10.1186/s43074-021-00042-0

## 3. Approval-ready proposed budget entries

These entries are deliberately marked PROPOSED. They must not be treated as approved until the owner accepts them after reviewing the workload evidence.

| Metric | Proposed criterion | Basis and caveat | Approval status |
|---|---|---|---|
| Score representation | Evaluate 6-bit rank/score resolution first; also run 4-bit and 5-bit ablations if workload traces show acceptable quality. | PRISM repository states 4–6 bit precision is sufficient as a design claim; EIS must independently validate retrieval quality. | PROPOSED |
| Minimum relevant score gap | Derive from the empirical score-gap distribution and ranking/retrieval degradation tolerance; do not use synthetic g=0.05 as a physical requirement. | Requires representative PRISM traces and application metric. | BLOCKED — INPUT DATA NEEDED |
| False-winner probability | Set the allowed rate from end-to-end retrieval-quality tolerance and the number of comparisons per request; calculate confidence bounds for the tested count. | A per-comparison error rate alone may compound in a ranking network. | BLOCKED — WORKLOAD RISK MODEL NEEDED |
| Pairwise latency | Set from the permitted total selection-stage latency after accounting for comparison topology, parallelism, fanout, and recovery. | PRISM's reported ~9 ns is a simulated selection-stage reference, not an approved per-comparator limit. | BLOCKED — ARCHITECTURE NEEDED |
| Pairwise energy | Allocate from an approved total selection-energy budget after accounting for the number of comparisons, optical source, modulation, bias/control, receiver or nonlinear decision, token generation, and calibration. | PRISM's reported ~2.3 nJ/query is simulated and optical-core scoped; it is not a per-comparator budget. | BLOCKED — SYSTEM BOUNDARY NEEDED |
| Output winner-token separability | Must meet a measured/modelled error margin across the declared envelope and preserve A/B identity; numeric contrast threshold to be set after encoding and receiver are specified. | No validated comparator transfer curve is currently available. | BLOCKED — ENCODING NEEDED |
| Insertion loss | Allocate from source power, receiver/threshold sensitivity, cascade depth and total energy budget. Freeze the allowable loss at named reference planes. | A standalone loss target cannot be defensibly set before topology and source/receiver are selected. | BLOCKED — TOPOLOGY NEEDED |
| Robustness | Specify process, temperature, wavelength, input-power imbalance, drift and calibration interval from the selected PDK and operating environment. | No transferable EIS PDK-specific comparator model currently established. | BLOCKED — PDK / OPERATING ENVELOPE NEEDED |
| Energy accounting | Include source, encoding/modulation, control/bias, decision, token output, calibration amortization and any receiver/regeneration required inside the declared boundary. | System-level photonic energy reviews show transmitter/modulator/converter/receiver overheads must be considered, not just optical core. | PROPOSED ACCOUNTING RULE |
| Selection quality | Compare selected block IDs and downstream inference against the software reference; report recall@k and task-quality delta with workload, seed and confidence interval. | PRISM itself reports workload-specific retrieval metrics; EIS must test the actual integration. | PROPOSED ACCEPTANCE METHOD |

## 4. Workload evidence required before numeric approval

The owner approval packet must include:

1. Representative PRISM score traces for the intended model/context/head distribution, including ties, near-ties and score-gap percentiles.
2. Baseline electronic top-k output and downstream quality/recall metrics for the same traces.
3. Intended k, candidate count N, whether comparisons are serial or parallel, allowed throughput and end-to-end latency.
4. Explicit selection-service energy boundary, including any optical source and thermal stabilization overhead; state whether shared/static energy is amortized and at what request rate.
5. Candidate score encoding and receiver/decision architecture, including candidate identity token format.
6. Intended PDK/process and available model provenance; EIS's target Ligentec/X-FAB SiN/TFLN data must not be replaced silently by SiEPIC SOI values.
7. The service-level error/quality budget and the method used to allocate it to each pairwise decision.

## 5. Approval record — intentionally unsigned

- EIS accountable approver: **NOT RECORDED**
- Approved workload / model / trace revision: **NOT RECORDED**
- Approved score-resolution / ranking-quality target: **NOT RECORDED**
- Approved max selection-stage latency: **NOT RECORDED**
- Approved max energy per query at stated boundary: **NOT RECORDED**
- Approved false-winner / retrieval-quality budget: **NOT RECORDED**
- Approved operating envelope and robustness target: **NOT RECORDED**
- Approval date and evidence hash: **NOT RECORDED**

No approval is inferred from repository edits, a successful CI run, or an assistant recommendation. The EIS owner must explicitly approve the completed values after the workload evidence is attached.

## 6. Decision gate

Current decision: **BLOCKED_PHYSICAL_BUDGET / NO FDTD-EM SPEND**.

The next non-simulation action is to acquire representative score traces and define the workload-service boundary. Then complete and sign this register, parameterize the analytical Interface A baseline, and separately decide whether a credible B1 detector-free mechanism exists. After the model and budgets pass independent review, authorize only the smallest simulation that resolves a named uncertainty.

## 7. Workload evidence inventory update (2026-10-11)

Public PRISM repository artifacts have now been inspected:

- `results/downstream/mrr_niah_v2b.json` contains configuration metadata and aggregate downstream outcomes.
- `results/signatures/recall_bf16_8k.json` contains aggregate recall values by configuration.
- `results/retrieval_heads/` contains retrieval-head evaluation records.
- `results/raw_logs/` contains run logs.
- `prism/simulator.py` exposes `PRISMSimulator.select_with_scores(query)`, which returns candidate scores from the software-emulated impairment path and selected indices.

These are useful starting evidence, but the checked-in aggregate result files do **not** themselves provide the frozen, per-query, candidate-level score-vector corpus required to approve a comparator gap or false-winner budget. Software-emulated score traces must be exported from a pinned PRISM commit and clearly labelled **SOFTWARE_EMULATED**; they are not measured hardware evidence.

EIS has added:
- `workload_evidence_protocol_v1.md` — capture protocol, source inventory, required metrics, and approval inputs.
- `workload_trace.schema.json` — trace schema including provenance, workload configuration, candidate-level scores/ranks, reference and emulated top-k IDs, and declared system boundaries.

**Current register state remains unchanged:** no trace artifact hash, approved workload distribution, end-to-end quality tolerance, complete service energy/latency boundary, or accountable owner approval has been recorded. Numeric physical budgets therefore remain **NOT APPROVED**. **FDTD/EM remains NO-GO.**

