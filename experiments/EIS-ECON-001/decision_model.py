"""Matched-workload decision model: measured energy + utilization-sensitive capital."""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def crf(rate: float, years: float) -> float:
    if years <= 0 or rate < 0:
        raise ValueError("useful life must be > 0 and capital rate >= 0")
    if rate == 0:
        return 1.0 / years
    growth = (1.0 + rate) ** years
    return rate * growth / (growth - 1.0)


def annual_accepted_outputs(hw: dict[str, str], acceptance_rate: float) -> float:
    peak = float(hw["peak_accepted_outputs_s"])
    hours = float(hw["operating_hours_per_year"])
    utilization = float(hw["utilization"])
    uptime = float(hw["uptime"])
    if peak <= 0 or hours <= 0 or not 0 < utilization <= 1 or not 0 < uptime <= 1:
        raise ValueError("invalid throughput, hours, utilization or uptime")
    if not 0 < acceptance_rate <= 1:
        raise ValueError("acceptance_rate must be in (0,1]")
    return peak * 3600.0 * hours * utilization * uptime * acceptance_rate


def capital_cost_per_accepted(hw: dict[str, str], acceptance_rate: float) -> dict[str, float]:
    capex = float(hw["capex_usd"])
    salvage = float(hw["salvage_value_usd"] or 0)
    if capex < 0 or salvage < 0 or salvage > capex:
        raise ValueError("capex/salvage values invalid")
    factor = crf(float(hw["annual_cost_of_capital"]), float(hw["useful_life_years"]))
    annual_volume = annual_accepted_outputs(hw, acceptance_rate)
    annualized = (capex - salvage) * factor
    return {
        "capital_recovery_factor": factor,
        "annual_accepted_outputs": annual_volume,
        "annualized_capital_cost_usd": annualized,
        "capital_cost_per_accepted_usd": annualized / annual_volume,
    }


def integrate_power_trace(rows: list[dict[str, str]], trace_id: str,
                          expected_boundary: str, required_components: list[str] | None = None) -> dict[str, Any]:
    selected = [r for r in rows if r.get("trace_id") == trace_id]
    if not selected:
        raise ValueError(f"missing power trace: {trace_id}")
    boundaries = {r.get("boundary") for r in selected}
    if boundaries != {expected_boundary}:
        raise ValueError(f"trace boundary mismatch: expected {expected_boundary}, got {boundaries}")
    if any((r.get("synchronized", "").lower() != "true") or not r.get("calibration_id") for r in selected):
        raise ValueError("all trace samples must be synchronized and have calibration IDs")
    calibration_ids = {r["calibration_id"] for r in selected}
    if len(calibration_ids) != 1:
        raise ValueError("calibration ID must be consistent across one trace")
    by_component: dict[str, list[tuple[float, float]]] = {}
    for row in selected:
        t, p = float(row["timestamp_s"]), float(row["power_w"])
        if p < 0:
            raise ValueError("power samples cannot be negative")
        by_component.setdefault(row["component"], []).append((t, p))
    if expected_boundary == "facility_meter":
        if set(by_component) != {"facility_total"}:
            raise ValueError("facility_meter trace must contain only facility_total")
    elif expected_boundary == "component_rails":
        if not required_components:
            raise ValueError("component_rails requires an explicit required_components list")
        if set(by_component) != set(required_components):
            raise ValueError("component rail set must exactly match required_components; avoid omissions and overlap")
    else:
        raise ValueError("unsupported boundary; use facility_meter or component_rails")

    total_j = 0.0
    component_j = {}
    for component, samples in by_component.items():
        samples.sort(key=lambda item: item[0])
        times = [x[0] for x in samples]
        if len(times) < 2 or any(b <= a for a, b in zip(times, times[1:])):
            raise ValueError(f"{component} needs >=2 strictly increasing timestamps")
        joules = sum((p0 + p1) * 0.5 * (t1 - t0)
                     for (t0, p0), (t1, p1) in zip(samples, samples[1:]))
        component_j[component] = joules
        total_j += joules
    return {
        "trace_id": trace_id,
        "boundary": expected_boundary,
        "calibration_id": next(iter(calibration_ids)),
        "synchronized": True,
        "duration_s": max(t for samples in by_component.values() for t, _ in samples)
                      - min(t for samples in by_component.values() for t, _ in samples),
        "energy_joules": total_j,
        "energy_kwh": total_j / 3_600_000.0,
        "component_energy_joules": component_j,
    }


def evaluate_run(run: dict[str, str], hw: dict[str, str], traces: list[dict[str, str]],
                 assumptions: dict[str, Any]) -> dict[str, Any]:
    if run.get("evidence_status") != "measured":
        raise ValueError(f"run {run.get('run_id')} is not marked measured")
    attempted, accepted = int(run["attempted_outputs"]), int(run["accepted_outputs"])
    if attempted <= 0 or accepted <= 0 or accepted > attempted:
        raise ValueError("invalid attempted/accepted output counts")
    acceptance = accepted / attempted
    limit = float(run["latency_limit_ms"])
    p95 = float(run["p95_latency_ms"])
    target = float(run["throughput_target_outputs_s"])
    achieved = float(run["achieved_throughput_outputs_s"])
    if p95 > limit or achieved < target:
        raise ValueError("run fails declared latency or throughput contract")
    energy = integrate_power_trace(
        traces, run["power_trace_id"], assumptions["power_trace_boundary"],
        assumptions.get("required_components", []))
    tariff = assumptions.get("effective_electricity_tariff_usd_per_kwh")
    if tariff is None or float(tariff) < 0:
        raise ValueError("a source-backed effective electricity tariff is required")
    nonenergy = float(run["non_energy_operating_cost_usd"])
    if nonenergy < 0:
        raise ValueError("non-energy operating cost cannot be negative")
    energy_cost = energy["energy_kwh"] * float(tariff)
    capital = capital_cost_per_accepted(hw, acceptance)
    variable_per_accepted = (nonenergy + energy_cost) / accepted
    total_per_accepted = variable_per_accepted + capital["capital_cost_per_accepted_usd"]
    return {
        "run_id": run["run_id"],
        "implementation": run["implementation"],
        "workload_id": run["workload_id"],
        "model_or_task_id": run["model_or_task_id"],
        "input_set_hash": run["input_set_hash"],
        "quality_contract_id": run["quality_contract_id"],
        "attempted_outputs": attempted,
        "accepted_outputs": accepted,
        "acceptance_rate": acceptance,
        "p95_latency_ms": p95,
        "latency_limit_ms": limit,
        "achieved_throughput_outputs_s": achieved,
        "throughput_target_outputs_s": target,
        "non_energy_operating_cost_usd": nonenergy,
        "measured_energy": energy,
        "electricity_tariff_usd_per_kwh": float(tariff),
        "energy_cost_usd": energy_cost,
        "variable_cost_per_accepted_usd": variable_per_accepted,
        **capital,
        "total_cost_per_accepted_usd": total_per_accepted,
        "evidence_status": "measured_run_with_declared_boundary",
    }


def compare_matched(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    match_fields = ("workload_id", "model_or_task_id", "input_set_hash",
                    "quality_contract_id", "latency_limit_ms", "throughput_target_outputs_s")
    mismatches = [k for k in match_fields if baseline[k] != candidate[k]]
    if mismatches:
        raise ValueError(f"unmatched comparison fields: {mismatches}")
    base = baseline["total_cost_per_accepted_usd"]
    eis = candidate["total_cost_per_accepted_usd"]
    delta = base - eis
    return {
        "matched": True,
        "baseline_cost_per_accepted_usd": base,
        "eis_cost_per_accepted_usd": eis,
        "savings_per_accepted_usd": delta,
        "cost_reduction_fraction": delta / base if base else None,
        "eis_advantage": delta > 0,
        "maximum_incremental_eis_cost_per_accepted_usd": max(
            0.0, base - candidate["variable_cost_per_accepted_usd"]),
        "baseline_annual_accepted_outputs": baseline["annual_accepted_outputs"],
        "eis_annual_accepted_outputs": candidate["annual_accepted_outputs"],
        "maximum_incremental_eis_capex_usd": max(
            0.0, base - candidate["variable_cost_per_accepted_usd"])
            * candidate["annual_accepted_outputs"] / candidate["capital_recovery_factor"],
        "interpretation": "Measured comparison under matched workload and contract; capex ceiling excludes unmodeled financing, deployment, tax and risk costs."
    }


def run_decision_model(runs_path: str | Path, traces_path: str | Path,
                       hardware_path: str | Path, assumptions_path: str | Path,
                       output_path: str | Path) -> dict[str, Any]:
    runs, traces, hardware = read_csv(runs_path), read_csv(traces_path), read_csv(hardware_path)
    with open(assumptions_path, encoding="utf-8") as f:
        assumptions = json.load(f)
    if not runs or not any(r.get("run_id") for r in runs):
        result = {"model_id": "EIS-ECON-001A", "status": "not_ready",
                  "reason": "No matched workload run records supplied; templates are intentionally empty."}
    else:
        hw_by_impl = {r["implementation"]: r for r in hardware if r.get("implementation")}
        evaluated = []
        for run in runs:
            if not run.get("run_id"):
                continue
            impl = run["implementation"]
            if impl not in hw_by_impl:
                raise ValueError(f"missing hardware economics for implementation {impl}")
            evaluated.append(evaluate_run(run, hw_by_impl[impl], traces, assumptions))
        baseline = next((r for r in evaluated if r["implementation"] == "electronic_baseline"), None)
        candidate = next((r for r in evaluated if r["implementation"] == "eis_candidate"), None)
        if baseline is None or candidate is None:
            result = {"model_id": "EIS-ECON-001A", "status": "not_ready",
                      "reason": "Both electronic_baseline and eis_candidate measured runs are required.",
                      "evaluated_runs": evaluated}
        else:
            result = {"model_id": "EIS-ECON-001A", "status": "measured_comparison",
                      "baseline": baseline, "candidate": candidate,
                      "comparison": compare_matched(baseline, candidate)}
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", required=True)
    parser.add_argument("--traces", required=True)
    parser.add_argument("--hardware", required=True)
    parser.add_argument("--assumptions", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(run_decision_model(args.runs, args.traces, args.hardware,
                                        args.assumptions, args.out), indent=2))


if __name__ == "__main__":
    main()
