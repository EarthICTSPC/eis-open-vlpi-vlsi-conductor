# EIS-ECON-001 — Cost per Accepted Transformation Model

**Status:** reproducible model and dashboard scaffold; projections are scenarios, not measured EIS results.

## Purpose

Keep three distinct economic series:

1. **Capability-adjusted model price index.** The 5×–13× annual decline is an explicit scenario range, not a market-wide observed API price decline.
2. **Usage-weighted API price.** Calculated from dated usage records and vendor rates for uncached input, cached input and output tokens.
3. **Cost per accepted useful transformation.** Full workload cost divided by outputs passing a declared quality contract.

The third series is EIS's strategic metric. It must include compute, memory, control, modulation, phase control, detector/TIA/ADC, conversion, calibration, cooling, capital amortization and operations where applicable. Failed outputs and retries remain part of cost.

## Model boundary

The model is intentionally transparent and uses editable JSON/CSV inputs. It does not infer physical energy savings from optical operation counts. It can ingest a future KKA operation-ledger JSON export as provenance metadata, but the ledger is not converted into joules. Measured SOI power traces replace scenario energy inputs only after calibration, synchronized acquisition and run provenance are supplied.

### Scenario equation

For baseline cost per accepted transformation (C_b), baseline energy share (s), energy-cost reduction (r), and incremental EIS non-energy cost (k):

`C_{EIS}=C_b(1-sr)+k`

Break-even requires `C_EIS < C_b`. The model reports the implied cost reduction and break-even status. The simple equation assumes the same quality contract, workload, throughput and latency. If these differ, comparisons are invalid until normalized.

## California reporting layer

The quarterly dashboard includes a California reporting-readiness register. It is a **data-collection and applicability tracker, not legal advice or a determination that EIS is a covered reporting entity**.

- **CEC Building Energy Benchmarking:** California's existing benchmarking program generally applies to buildings larger than 50,000 square feet (with program-specific rules and exceptions); CEC says standalone data centers over 50,000 sq ft and data centers in buildings over 50,000 sq ft report annually.
- **AB 1577 (2026, Chapter 434):** the chaptered law defines covered data centers around installed IT electrical capacity of at least 10 MW (subject to statutory exclusions) and requires CEC reporting of specified facility, energy and operational information. Local-agency disclosures also apply in connection with specified discretionary permit/entitlement applications. Track implementation instructions and applicability before filing.
- **SB 253:** CARB's 2026 first-year Scope 1 and 2 reporting deadline was November 10, 2026 for covered U.S.-based entities with more than $1 billion annual revenue doing business in California. Scope 3 begins in 2027 under subsequent rulemaking. This is not presumed applicable to EIS.
- **SB 261:** enforcement remains enjoined while appellate proceedings are pending; CARB says it will not enforce the statutory deadline during the injunction. Track status; do not mark as an active mandatory filing absent updated legal guidance.

California data fields tracked: monthly grid electricity (kWh), on-site generation and fuel by type, storage, renewable procurement/attributes, PUE, IT load/capacity, water, cooling and waste heat where available; location and facility-size/threshold evidence; reporting owner, period, source and status. Preserve confidentiality and statutory limits on disclosure.

Official and primary references:
- CEC data centers: https://www.energy.ca.gov/programs-and-topics/topics/data-centers
- CEC Building Energy Benchmarking: https://www.energy.ca.gov/programs-and-topics/programs/building-energy-benchmarking-program/building-energy-benchmarking
- AB 1577 chaptered bill / status: https://calmatters.digitaldemocracy.org/bills/ca_202520260ab1577
- Governor's September 21, 2026 data-center package announcement: https://www.gov.ca.gov/2026/09/21/governor-newsom-signs-most-comprehensive-data-center-laws-in-the-nation-providing-communities-more-control-on-water-electricity-and-land-use/
- CARB corporate GHG reporting: https://ww2.arb.ca.gov/our-work/programs/california-corporate-greenhouse-gas-reporting-and-climate-related-financial-risk
- CARB SB 261 status: https://ww2.arb.ca.gov/our-work/programs/corporate-ghg-reporting/climate-related-financial-risk

## Files

- `model.py`: pure-Python calculation engine and CSV/JSON ingestion.
- `dashboard.py`: quarterly charts and summary CSV/JSON outputs.
- `assumptions.json`: editable, explicitly illustrative scenario assumptions.
- `inputs/market_observations.csv`: dated API-rate and token-usage input template.
- `inputs/workload_observations.csv`: matched workload and accepted-output input template.
- `inputs/california_facility_observations.csv`: California reporting and energy data template.
- `inputs/kka_operation_ledger.example.json`: provenance-only example link to the formal KKA ledger.
- `test_model.py`: deterministic tests.

## Run

From repository root:

```bash
python3 experiments/EIS-ECON-001/model.py --assumptions experiments/EIS-ECON-001/assumptions.json --out experiments/EIS-ECON-001/output
python3 -m pip install matplotlib
python3 experiments/EIS-ECON-001/dashboard.py --assumptions experiments/EIS-ECON-001/assumptions.json --inputs experiments/EIS-ECON-001/inputs --out experiments/EIS-ECON-001/output
python3 -m unittest discover -s experiments/EIS-ECON-001 -p 'test_*.py' -v
```

The dashboard labels scenarios and observed data separately. Empty observation templates produce no fabricated market or physical results.

## Evidence discipline

- **Scenario:** editable assumption, not a measurement.
- **Market observation:** dated rate-card/usage record with source URL and billing period.
- **Modeled workload:** cost model derived from declared assumptions and workload contract.
- **Measured EIS:** only when synchronized physical traces, instrument calibration, quality acceptance and full-system energy boundary are supplied.
- **California reportable datum:** source-backed facility observation with period, units and evidence; legal applicability reviewed separately.

No EIS performance, energy-saving, emissions-reduction or regulatory-compliance result is claimed by this scaffold.
