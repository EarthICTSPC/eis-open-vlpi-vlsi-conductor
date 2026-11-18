import unittest
from decision_model import (crf, annual_accepted_outputs, capital_cost_per_accepted,
                            integrate_power_trace, compare_matched)


class DecisionModelTests(unittest.TestCase):
    def test_crf_zero_rate(self):
        self.assertAlmostEqual(crf(0, 10), .1)

    def test_crf_positive_rate(self):
        self.assertAlmostEqual(crf(.1, 10), .1627453949, places=8)

    def test_utilization_scales_annual_volume(self):
        hw = {"peak_attempted_outputs_s":"10", "operating_hours_per_year":"1000",
              "utilization":"0.5", "uptime":"0.9"}
        self.assertAlmostEqual(annual_accepted_outputs(hw, .8), 10*3600*1000*.5*.9*.8)

    def test_capital_cost_per_accepted(self):
        hw = {"capex_usd":"100000", "salvage_value_usd":"0",
              "useful_life_years":"10", "annual_cost_of_capital":"0",
              "peak_attempted_outputs_s":"10", "operating_hours_per_year":"1000",
              "utilization":"0.5", "uptime":"1"}
        r = capital_cost_per_accepted(hw, 1)
        self.assertAlmostEqual(r["annualized_capital_cost_usd"], 10000)
        self.assertAlmostEqual(r["capital_cost_per_accepted_usd"], 10000/(10*3600*1000*.5))

    def test_integrate_facility_meter(self):
        rows = [
            {"trace_id":"t1","timestamp_s":"0","component":"facility_total","power_w":"100",
             "boundary":"facility_meter","calibration_id":"cal1","synchronized":"true"},
            {"trace_id":"t1","timestamp_s":"10","component":"facility_total","power_w":"200",
             "boundary":"facility_meter","calibration_id":"cal1","synchronized":"true"}
        ]
        r = integrate_power_trace(rows, "t1", "facility_meter")
        self.assertAlmostEqual(r["energy_joules"], 1500)

    def test_reject_unsynchronized_trace(self):
        rows = [{"trace_id":"t1","timestamp_s":"0","component":"facility_total","power_w":"100",
                 "boundary":"facility_meter","calibration_id":"cal1","synchronized":"false"}]
        with self.assertRaises(ValueError):
            integrate_power_trace(rows, "t1", "facility_meter")

    def test_reject_incomplete_component_rails(self):
        rows = [{"trace_id":"t1","timestamp_s":"0","component":"laser","power_w":"10",
                 "boundary":"component_rails","calibration_id":"cal1","synchronized":"true"},
                {"trace_id":"t1","timestamp_s":"1","component":"laser","power_w":"10",
                 "boundary":"component_rails","calibration_id":"cal1","synchronized":"true"}]
        with self.assertRaises(ValueError):
            integrate_power_trace(rows, "t1", "component_rails", ["laser","control"])

    def test_reject_unsynchronized_component_time_vectors(self):
        rows = []
        for component, times in (("laser", [0, 1]), ("control", [0, 2])):
            for t in times:
                rows.append({"trace_id":"t2","timestamp_s":str(t),"component":component,
                             "power_w":"10","boundary":"component_rails",
                             "calibration_id":"cal2","synchronized":"true"})
        with self.assertRaises(ValueError):
            integrate_power_trace(rows, "t2", "component_rails", ["laser","control"])

    def test_matched_comparison_reports_capex_headroom(self):
        baseline = {"workload_id":"w","model_or_task_id":"m","input_set_hash":"h",
                    "quality_contract_id":"q","latency_limit_ms":10,"throughput_target_outputs_s":2,
                    "total_cost_per_accepted_usd":1.0,"variable_cost_per_accepted_usd":.7,
                    "annual_accepted_outputs":1000,"capital_recovery_factor":.1,
                    "net_capital_cost_basis_usd":2000}
        candidate = {"workload_id":"w","model_or_task_id":"m","input_set_hash":"h",
                     "quality_contract_id":"q","latency_limit_ms":10,"throughput_target_outputs_s":2,
                     "total_cost_per_accepted_usd":.9,"variable_cost_per_accepted_usd":.5,
                     "annual_accepted_outputs":1000,"capital_recovery_factor":.1,
                     "net_capital_cost_basis_usd":3000}
        result = compare_matched(baseline, candidate)
        self.assertAlmostEqual(result["remaining_affordable_cost_per_accepted_usd"], .1)
        self.assertAlmostEqual(result["maximum_affordable_total_eis_net_capex_usd"], 5000)
        self.assertAlmostEqual(result["additional_capex_headroom_vs_candidate_usd"], 2000)

    def test_reject_mismatched_quality_contract(self):
        a = {"workload_id":"w","model_or_task_id":"m","input_set_hash":"h",
             "quality_contract_id":"q1","latency_limit_ms":10,"throughput_target_outputs_s":2,
             "total_cost_per_accepted_usd":1,"variable_cost_per_accepted_usd":.5,
             "annual_accepted_outputs":100,"capital_recovery_factor":.1}
        b = {**a, "quality_contract_id":"q2"}
        with self.assertRaises(ValueError):
            compare_matched(a,b)


if __name__ == "__main__":
    unittest.main()
