# EIS-ECON-001A — Matched Baseline, Utilization and Energy Boundary

This extension converts the scenario-only economic model into a measurement-ready decision model. It does not manufacture measurements: blank templates remain blank and a matched comparison is emitted only when both implementations have complete, quality-matched run records and valid calibrated power traces.

## 1. Matched electronic baseline

For every comparison, the electronic and EIS run records must match on:

- `workload_id` and `quality_contract_id`
- `latency_limit_ms` and `throughput_target_outputs_s`
- model/checkpoint or task specification and input-set hash (recorded in the CSV)
- measurement window definition and accepted-output semantics

Each implementation records attempted and accepted outputs, p95 latency, achieved throughput, non-energy operating cost, trace ID and evidence status. Failed outputs and retries remain in the cost numerator; only accepted outputs are in the denominator. A mismatch in workload or contract blocks the comparison.

## 2. Whole-system energy boundary

`power_traces.csv` supports two mutually exclusive methods:

- `facility_meter`: one calibrated, synchronized `facility_total` meter series. This is preferred for the total-system comparison.
- `component_rails`: calibrated, synchronized, non-overlapping component rails whose required component set is explicitly configured. Do not sum overlapping rails (for example, a PSU input meter and the downstream device rails).

The integrator checks trace ID, calibration ID, synchronization flag, monotonic timestamps, sample count and required components. It trapezoid-integrates watts over seconds to joules. The model will not infer energy from KKA logical interference samples or operation counts.

For each run:

`energy_kWh = energy_J / 3,600,000`

`energy_cost = energy_kWh × effective_tariff_USD_per_kWh`

Keep location-based and market-based Scope 2 emissions separate from the cost calculation. They require their own dated, source-backed emissions factors and renewable-attribute evidence.

## 3. Utilization-sensitive capital cost

Annual accepted capacity is:

`annual_accepted = peak_accepted_outputs_per_second × 3600 × operating_hours_per_year × utilization × uptime × acceptance_rate`

Capital recovery factor:

`CRF = i(1+i)^n / ((1+i)^n - 1)`

where `i` is annual cost of capital and `n` is useful life in years. For zero discount rate, `CRF=1/n`.

`annualized_capital_cost = (capex - salvage_value) × CRF`

`capital_cost_per_accepted = annualized_capital_cost / annual_accepted`

The model reports utilization explicitly. Low utilization increases capital cost per accepted output. The same method is applied to the electronic baseline and EIS candidate.

## 4. Cost and affordable premium

`cost_per_accepted = (non_energy_operating_cost + measured_energy_cost) / accepted_outputs + capital_cost_per_accepted`

`max_affordable_incremental_EIS_cost_per_accepted = baseline_cost_per_accepted - EIS_operating_cost_per_accepted_before_incremental_EIS_capital`

`max_affordable_EIS_capex = max(0, max_affordable_incremental_cost_per_accepted) × EIS_annual_accepted_outputs / EIS_CRF`

This is the maximum incremental capital budget under the declared assumptions, before any risk premium, financing fees, taxes or additional deployment costs not explicitly included. A negative per-output allowance means the EIS candidate does not break even even with zero incremental capital cost.

## 5. Inputs

- `matched_workload_runs.csv`: one row per implementation/run; includes task and quality contract IDs, acceptance, latency, throughput, non-energy operating cost and trace ID.
- `power_traces.csv`: timestamped power samples with boundary, calibration and synchronization metadata.
- `hardware_economics.csv`: one row per implementation with capex, salvage, life, cost of capital, peak accepted throughput, annual operating hours, utilization and uptime.
- `decision_assumptions.json`: tariff and required rail names.

Use actual measured data only after instrument calibration, time synchronization, workload identity and run provenance are documented. Otherwise set `evidence_status` to `scenario` and do not mix it into observed results.

## 6. Run

```bash
python3 -m unittest discover -s experiments/EIS-ECON-001 -p 'test_*.py' -v
python3 experiments/EIS-ECON-001/decision_model.py \
  --runs experiments/EIS-ECON-001/inputs/matched_workload_runs.csv \
  --traces experiments/EIS-ECON-001/inputs/power_traces.csv \
  --hardware experiments/EIS-ECON-001/inputs/hardware_economics.csv \
  --assumptions experiments/EIS-ECON-001/decision_assumptions.json \
  --out experiments/EIS-ECON-001/output/decision_comparison.json
```

An empty template returns `not_ready`, not a fabricated baseline or zero-energy result.
