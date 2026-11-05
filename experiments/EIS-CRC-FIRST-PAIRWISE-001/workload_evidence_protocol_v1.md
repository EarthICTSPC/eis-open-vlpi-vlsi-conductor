# EIS-CRC-FIRST-PAIRWISE-001 — Workload Evidence Protocol v1

**Status:** Evidence assembly started; public aggregate artifacts inventoried; raw candidate-level score traces not yet captured.
**Simulation authorization:** FDTD/EM remains **NO-GO**.
**Purpose:** Convert the intended PRISM KV-block selection workload into reproducible evidence for choosing the pairwise comparator's score range, relevant score gap, winner-error budget, latency boundary, energy boundary, and operating envelope.

## 1. Public evidence inventory

The public PRISM repository currently exposes useful aggregate/downstream artifacts, including:

- `results/downstream/mrr_niah_v2b.json`: model/configuration metadata and needle-in-a-haystack downstream outcomes across context lengths, k values, and simulated MRR configurations.
- `results/signatures/recall_bf16_8k.json`: aggregate recall summaries by block size, signature dimension, and method.
- `results/retrieval_heads/qwen25_7b_bf16_128k.json` and related retrieval-head files: workload/head-level result records.
- `results/raw_logs/mrr_niah_v2b_log.txt` and related logs: run logs.

Sources:
- https://github.com/hyoseokp/PRISM/tree/main/results
- https://github.com/hyoseokp/PRISM/blob/main/results/downstream/mrr_niah_v2b.json
- https://github.com/hyoseokp/PRISM/blob/main/results/signatures/recall_bf16_8k.json
- https://github.com/hyoseokp/PRISM/blob/main/prism/simulator.py

**Important evidence boundary:** These committed JSON files and logs provide aggregate results/configuration, not a ready-made, per-query, candidate-level score-vector dataset sufficient to derive the pairwise score-gap distribution. They are **PAPER/REPOSITORY-REPORTED aggregate evidence**, not raw score traces and not physical measurements. Do not calculate a physical comparator threshold from aggregate recall values.

The public simulator's `PRISMSimulator.select_with_scores(query)` exposes candidate score values from its software-emulated MRR/impairment path, plus selected indices. This is a candidate trace source for a reproducible software-emulation run, not measured hardware evidence. Capture exact code commit, configuration, seeds, query/candidate identity, and reference outputs.

## 2. Required trace contents

Each query trace must preserve:

1. **Provenance:** upstream repository URL, commit SHA, script/API, model/checkpoint, dataset/evaluation split, command, environment, random seeds, timestamp, artifact hash, and evidence class.
2. **Workload:** model, layer/head (if applicable), context length, number of candidate blocks N, block size, selected k, signature dimension, and batch/concurrency.
3. **Per-candidate data:** stable candidate/block ID; reference score; PRISM-emulated score before/after each modeled impairment where available; final score delivered to top-k; reference rank; selected/not selected.
4. **Selection baseline:** exact software electronic top-k candidate IDs, PRISM software-emulated top-k IDs, and ground-truth/retrieval target where available.
5. **System boundary:** request rate, concurrency, timing boundary, energy boundary, whether optical-source and thermal stabilization energy are included or amortized, and which terms remain unknown.
6. **Validity:** missing/NaN values, ties, duplicate scores, clipped/saturated values, and any excluded trace with an explicit reason. Never silently discard ties or difficult cases.

Do not upload prompts, customer data, proprietary model outputs, credentials, or other sensitive material. Use a public benchmark or appropriately authorized, de-identified workload.

## 3. Capture protocol

1. Pin the exact PRISM commit and record the SHA. Do not rely on a moving `main` branch for final evidence.
2. Reproduce a published public configuration first (baseline smoke test); retain its original output and command.
3. Add a trace-export wrapper around the existing software simulator API. For each fixed query, persist the complete candidate score vector and IDs, not only top-k indices. Preserve any digital/reference score vector separately.
4. Fix all random seeds where supported. If the simulator uses unseeded random operations, explicitly seed and document them or classify the run as non-reproducible until corrected.
5. Use multiple workload strata: context length, N, k, model/layer/head, and score-gap/tie cases. Include the intended production-representative distribution, not only a hand-picked easy case.
6. Hash and freeze the raw trace artifact before computing thresholds. Keep raw traces immutable; derived tables/scripts must point to that hash.
7. Compute score-gap quantiles, tie/near-tie frequency, rank disagreement, top-k overlap/recall, and downstream task-quality delta. Report per-stratum values and confidence intervals; do not pool away a failing stratum.
8. Only after EIS reviews workload representativeness and quality tolerance should the score encoding, indifference gap, per-comparison false-winner budget, N/k/topology, latency and energy targets be frozen.

## 4. Required derived metrics

For each query, with candidate scores sorted descending (s_{(1)} \ge \dots \ge s_{(N)}):

- **Adjacent gaps:** (g_i=s_{(i)}-s_{(i+1)}) for all adjacent ranks relevant to the comparator's eventual role.
- **Top-k boundary gap:** (g_k=s_{(k)}-s_{(k+1)}), where defined.
- **Pair sampling:** include all adjacent pairs for the small evaluation set, or preregister a reproducible pair-sampling strategy for larger N; retain all top-k-boundary and tie/near-tie pairs.
- **Rank/top-k impact:** exact top-k agreement, recall@k/overlap, and downstream retrieval or inference quality against the software reference.
- **Decision-risk allocation:** translate the approved end-to-end quality tolerance and comparisons-per-query topology into a per-decision error budget; state assumptions and confidence method.

The pairwise comparator contract is not itself the complete top-k network. Pairwise evidence must not be presented as proof of cascade/top-k behavior.

## 5. Approval register inputs

The following values cannot be inferred from public aggregate results alone:

- Approved workload/model/trace revision and trace SHA-256.
- Representative N and k distribution; topology and parallelism.
- Score normalization and score-to-signal encoding.
- Minimum relevant score gap / indifference policy.
- Downstream quality tolerance and per-comparison false-winner budget.
- End-to-end selection-stage latency and throughput target.
- Complete energy boundary, request-rate amortization, source/thermal/control overhead.
- Target PDK/process and justified operating envelope.
- EIS accountable approver and approval date.

Until these are supplied and reviewed, the budget register remains **PROPOSED / NOT APPROVED** and FDTD/EM remains **NO-GO**.

## 6. Current decision

**Evidence status:** Public aggregate/downstream artifacts identified; raw per-query score traces not yet captured; service-level energy/latency boundary not yet approved.
**Next measurable action:** Run a pinned, reproducible PRISM software-emulation trace export for representative N/k/context strata, then analyze the frozen artifact. This is workload characterization, not FDTD/EM and not physical validation.
