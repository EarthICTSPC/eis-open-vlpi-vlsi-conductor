"""EIS-ECON-001 transparent cost-per-accepted-transformation model.

Standard-library only. No scenario is represented as measured performance.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def capability_price_scenarios(base_index: float, annual_decline_factors: list[float],
                               years: list[int]) -> list[dict[str, float | int]]:
    """Return indexed capability-adjusted price scenarios; factor 5 means /5 per year."""
    if base_index <= 0 or not years:
        raise ValueError("base_index and years must be positive/non-empty")
    rows = []
    for factor in annual_decline_factors:
        if factor <= 0:
            raise ValueError("annual decline factors must be positive")
        for year in years:
            exponent = year - years[0]
            rows.append({"year": year, "decline_factor": factor,
                         "price_index": base_index / (factor ** exponent)})
    return rows


def weighted_api_price_per_million(rows: list[dict[str, str]]) -> float | None:
    """Weighted effective $/1M tokens from dated usage and per-class $/1M rates."""
    total_tokens = 0.0
    total_cost = 0.0
    for row in rows:
        classes = (
            ("uncached_input_tokens", "uncached_input_usd_per_million"),
            ("cached_input_tokens", "cached_input_usd_per_million"),
            ("output_tokens", "output_usd_per_million"),
        )
        for token_key, price_key in classes:
            tokens = float(row.get(token_key) or 0)
            price = row.get(price_key, "")
            if tokens < 0:
                raise ValueError("token counts cannot be negative")
            if tokens and price == "":
                raise ValueError(f"missing rate for used token class: {price_key}")
            if price != "" and float(price) < 0:
                raise ValueError("token prices cannot be negative")
            total_tokens += tokens
            total_cost += tokens * float(price or 0) / 1_000_000
    return None if total_tokens == 0 else total_cost / total_tokens * 1_000_000


def accepted_cost(baseline_cost: float, energy_share: float, energy_cost_reduction: float,
                  incremental_non_energy_cost: float = 0.0) -> dict[str, float | bool]:
    """Scenario cost under a matched contract and workload."""
    if baseline_cost <= 0:
        raise ValueError("baseline_cost must be positive")
    if not 0 <= energy_share <= 1:
        raise ValueError("energy_share must be between 0 and 1")
    if not 0 <= energy_cost_reduction <= 1:
        raise ValueError("energy_cost_reduction must be between 0 and 1")
    if incremental_non_energy_cost < 0:
        raise ValueError("incremental_non_energy_cost cannot be negative")
    eis_cost = baseline_cost * (1 - energy_share * energy_cost_reduction) + incremental_non_energy_cost
    reduction = (baseline_cost - eis_cost) / baseline_cost
    return {
        "baseline_cost_per_accepted": baseline_cost,
        "eis_cost_per_accepted": eis_cost,
        "cost_reduction_fraction": reduction,
        "break_even": eis_cost < baseline_cost,
        "energy_cost_reduction_fraction": energy_cost_reduction,
        "energy_share_fraction": energy_share,
        "incremental_non_energy_cost": incremental_non_energy_cost,
        "maximum_incremental_cost_before_parity": baseline_cost * energy_share * energy_cost_reduction,
    }


def workload_cost_from_observation(row: dict[str, str]) -> dict[str, float]:
    """Compute actual all-in cost per accepted output from an observation row."""
    total_cost = float(row["total_cost_usd"])
    accepted = int(row["accepted_outputs"])
    attempted = int(row["attempted_outputs"])
    if total_cost < 0 or accepted < 0 or attempted < accepted:
        raise ValueError("invalid cost or output counts")
    if accepted == 0:
        raise ValueError("accepted_outputs must be > 0 to compute unit cost")
    return {
        "total_cost_usd": total_cost,
        "accepted_outputs": accepted,
        "attempted_outputs": attempted,
        "acceptance_rate": accepted / attempted if attempted else 0.0,
        "cost_per_accepted_usd": total_cost / accepted,
    }


def build_scenario_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    base = config["workload_scenario"]["baseline_cost_per_accepted_usd"]
    rows = []
    for scenario in config["workload_scenario"]["scenarios"]:
        row = {"scenario": scenario["name"], **accepted_cost(
            baseline_cost=base,
            energy_share=scenario["energy_share"],
            energy_cost_reduction=scenario["energy_cost_reduction"],
            incremental_non_energy_cost=scenario["incremental_non_energy_cost_usd"],
        )}
        rows.append(row)
    return rows


def run_model(assumptions_path: str | Path, input_dir: str | Path,
              output_dir: str | Path) -> dict[str, Any]:
    config = load_json(assumptions_path)
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    years = config["capability_price_scenario"]["years"]
    capability = capability_price_scenarios(
        config["capability_price_scenario"]["base_index"],
        config["capability_price_scenario"]["annual_decline_factors"], years)
    with open(output_dir / "capability_price_scenarios.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "decline_factor", "price_index"])
        writer.writeheader()
        writer.writerows(capability)

    market_rows = load_csv(input_dir / "market_observations.csv")
    market_records = [r for r in market_rows if r.get("date") and r.get("provider")]
    api_price = weighted_api_price_per_million(market_records)

    scenario_rows = build_scenario_rows(config)
    with open(output_dir / "eis_cost_scenarios.csv", "w", newline="", encoding="utf-8") as f:
        fields = list(scenario_rows[0].keys()) if scenario_rows else []
        writer = csv.DictWriter(f, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(scenario_rows)

    workload_rows = load_csv(input_dir / "workload_observations.csv")
    actual_workloads = []
    for row in workload_rows:
        if row.get("total_cost_usd") and row.get("accepted_outputs"):
            actual_workloads.append({**row, **workload_cost_from_observation(row)})

    california_rows = load_csv(input_dir / "california_facility_observations.csv")
    summary = {
        "model_id": "EIS-ECON-001",
        "model_version": config["model_version"],
        "evidence_status": "scenario_only_unless_observation_rows_present",
        "capability_adjusted_price": {
            "status": "scenario",
            "annual_decline_factors": config["capability_price_scenario"]["annual_decline_factors"],
            "note": "Not a market-wide observed API price decline."
        },
        "usage_weighted_api_price": {
            "status": "observed" if api_price is not None else "no_observations",
            "usd_per_million_tokens": api_price,
            "dated_records": len(market_records)
        },
        "eis_cost_per_accepted": {
            "status": "scenario",
            "scenarios": scenario_rows,
            "actual_workload_records": actual_workloads
        },
        "california_reporting": {
            "status": "facility_observations_present" if california_rows else "template_only",
            "observation_records": len([r for r in california_rows if any(v for v in r.values())])
        },
        "non_claims": [
            "No physical EIS energy saving is inferred from operation counts.",
            "No regulatory applicability determination is made.",
            "Scenario results assume matched workload, quality contract, latency and throughput."
        ]
    }
    with open(output_dir / "quarterly_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assumptions", default="experiments/EIS-ECON-001/assumptions.json")
    parser.add_argument("--inputs", default="experiments/EIS-ECON-001/inputs")
    parser.add_argument("--out", default="experiments/EIS-ECON-001/output")
    args = parser.parse_args()
    summary = run_model(args.assumptions, args.inputs, args.out)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
