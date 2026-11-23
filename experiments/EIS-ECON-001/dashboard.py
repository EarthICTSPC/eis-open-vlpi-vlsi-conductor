"""Quarterly EIS-ECON-001 charts; scenarios and observations are visually separated."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import capability_price_scenarios, load_csv, load_json, accepted_cost, weighted_api_price_per_million


def make_dashboard(assumptions_path: str | Path, input_dir: str | Path,
                   output_dir: str | Path) -> list[Path]:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Install matplotlib: python3 -m pip install matplotlib") from exc

    config = load_json(assumptions_path)
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    market = load_csv(input_dir / "market_observations.csv")
    workloads = load_csv(input_dir / "workload_observations.csv")
    years = config["capability_price_scenario"]["years"]
    factors = config["capability_price_scenario"]["annual_decline_factors"]
    curves = capability_price_scenarios(config["capability_price_scenario"]["base_index"], factors, years)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for factor in factors:
        subset = [r for r in curves if r["decline_factor"] == factor]
        axes[0].plot([r["year"] for r in subset], [r["price_index"] for r in subset],
                     marker="o", label=f"{factor}× annual decline")
    axes[0].set_title("Capability-adjusted price scenarios")
    axes[0].set_ylabel("Index (first year = 100)")
    axes[0].set_xlabel("Year")
    axes[0].set_yscale("log")
    axes[0].legend()
    axes[0].grid(True, alpha=.25)

    if market:
        grouped: dict[str, list[dict[str, str]]] = {}
        for row in market:
            if row.get("date") and row.get("provider"):
                grouped.setdefault(row["date"], []).append(row)
        dates, prices = [], []
        for date, rows in sorted(grouped.items()):
            price = weighted_api_price_per_million(rows)
            if price is not None:
                dates.append(date)
                prices.append(price)
        if dates:
            axes[1].plot(dates, prices, marker="o", label="Observed usage-weighted API price")
            axes[1].legend()
    axes[1].set_title("Usage-weighted API price")
    axes[1].set_ylabel("USD per 1M total tokens")
    axes[1].set_xlabel("Observation date")
    axes[1].grid(True, alpha=.25)
    if not market:
        axes[1].text(.5, .5, "No dated market observations\n(template only)",
                     ha="center", va="center", transform=axes[1].transAxes)

    scenarios = config["workload_scenario"]["scenarios"]
    baseline = config["workload_scenario"]["baseline_cost_per_accepted_usd"]
    names, values = [], []
    for s in scenarios:
        result = accepted_cost(baseline, s["energy_share"], s["energy_cost_reduction"],
                               s["incremental_non_energy_cost_usd"])
        names.append(s["name"])
        values.append(result["eis_cost_per_accepted"])
    axes[2].bar(names, values, label="EIS scenario")
    axes[2].axhline(baseline, linestyle="--", label="Electronic baseline scenario")
    axes[2].set_title("Cost per accepted transformation")
    axes[2].set_ylabel("USD per accepted output")
    axes[2].tick_params(axis="x", rotation=20)
    axes[2].legend()
    axes[2].grid(True, axis="y", alpha=.25)

    fig.suptitle("Earth ICT, SPC — quarterly economic evidence dashboard")
    fig.text(.5, .01, "Scenario curves are assumptions, not EIS measurements. Market series appears only when dated records are supplied.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, .93))
    chart = output_dir / "eis_econ_001_quarterly_dashboard.png"
    fig.savefig(chart, dpi=160)
    plt.close(fig)

    # California reporting readiness snapshot (data inventory, not a compliance opinion).
    ca = load_csv(input_dir / "california_facility_observations.csv")
    populated = [r for r in ca if any(v for v in r.values())]
    readiness = {
        "dashboard_component": "California facility and disclosure data inventory",
        "observation_rows": len(populated),
        "status": "observations_present" if populated else "template_only",
        "tracked_fields": [
            "facility_id, reporting_period, facility_location, installed_it_capacity_mw",
            "monthly_grid_electricity_kwh, onsite_generation_kwh_by_type, onsite_fuel_by_type",
            "storage_capacity_and_dispatch, renewable_procurement, electricity_cost_and_tariff, hourly_or_monthly_grid_emissions_factor, scope2_location_and_market_based_emissions, caiso_zone_and_interval_data, pue",
            "water, cooling, waste_heat, source_document, data_owner, review_status"
        ],
        "regulatory_tracks": {
            "CEC_building_benchmarking": "screen building area and program rules; annual reporting may apply above 50,000 sq ft",
            "AB_1577": "screen installed IT electrical capacity at 10 MW threshold, statutory exclusions and CEC/local-agency implementation",
            "SB_253": "screen entity revenue and California nexus; 2026 Scope 1/2 first-year reporting deadline was 2026-11-10",
            "SB_261": "track injunction and CARB updates; enforcement paused while appellate proceedings pending"
        },
        "legal_note": "This is a data-readiness tracker, not legal advice or a determination of coverage."
    }
    with open(output_dir / "california_reporting_readiness.json", "w", encoding="utf-8") as f:
        json.dump(readiness, f, indent=2)
    # California operating dashboard: energy, spend and Scope 2 emissions remain separate.
    ca_chart = output_dir / "eis_econ_001_california_reporting.png"
    ca_fig, ca_axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    if populated:
        by_period: dict[str, dict[str, float]] = {}
        for row in populated:
            period = row.get("reporting_period", "")
            if not period:
                continue
            bucket = by_period.setdefault(period, {"kwh": 0.0, "cost": 0.0, "scope2_location": 0.0, "scope2_market": 0.0})
            for key, target in (("monthly_grid_electricity_kwh", "kwh"),
                                ("grid_electricity_cost_usd", "cost"),
                                ("scope2_location_based_kgco2e", "scope2_location"),
                                ("scope2_market_based_kgco2e", "scope2_market")):
                if row.get(key):
                    bucket[target] += float(row[key])
        periods = sorted(by_period)
        if periods:
            ca_axes[0].plot(periods, [by_period[x]["kwh"] for x in periods], marker="o")
            ca_axes[1].plot(periods, [by_period[x]["cost"] for x in periods], marker="o")
            ca_axes[2].plot(periods, [by_period[x]["scope2_location"] for x in periods], marker="o", label="Location-based")
            ca_axes[2].plot(periods, [by_period[x]["scope2_market"] for x in periods], marker="s", label="Market-based")
            ca_axes[2].legend()
        else:
            ca_axes[0].text(.5, .5, "Facility rows need reporting_period values", ha="center", va="center", transform=ca_axes[0].transAxes)
    else:
        ca_axes[0].text(.5, .5, "No California facility observations yet\\n(template only)", ha="center", va="center", transform=ca_axes[0].transAxes)
    ca_axes[0].set_ylabel("Grid electricity (kWh)")
    ca_axes[1].set_ylabel("Electricity cost (USD)")
    ca_axes[2].set_ylabel("Scope 2 emissions (kgCO2e)")
    ca_axes[2].set_xlabel("Reporting period")
    for axis in ca_axes:
        axis.grid(True, alpha=.25)
    ca_fig.suptitle("California facility energy and Scope 2 reporting")
    ca_fig.tight_layout(rect=(0, 0, 1, .96))
    ca_fig.savefig(ca_chart, dpi=160)
    plt.close(ca_fig)
    return [chart, ca_chart, output_dir / "california_reporting_readiness.json"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assumptions", default=str(HERE / "assumptions.json"))
    parser.add_argument("--inputs", default=str(HERE / "inputs"))
    parser.add_argument("--out", default=str(HERE / "output"))
    args = parser.parse_args()
    for path in make_dashboard(args.assumptions, args.inputs, args.out):
        print(path)


if __name__ == "__main__":
    main()
