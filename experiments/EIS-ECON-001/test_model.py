import tempfile
import unittest
from pathlib import Path
from model import (accepted_cost, capability_price_scenarios,
                   weighted_api_price_per_million, workload_cost_from_observation)


class EconModelTests(unittest.TestCase):
    def test_capability_scenario_5x(self):
        rows = capability_price_scenarios(100, [5], [2026, 2027, 2028])
        self.assertEqual([r["price_index"] for r in rows], [100, 20, 4])

    def test_capability_scenario_13x(self):
        rows = capability_price_scenarios(100, [13], [2026, 2027])
        self.assertAlmostEqual(rows[1]["price_index"], 100 / 13)

    def test_api_blended_price_weights_token_volume(self):
        rows = [{
            "uncached_input_tokens": "800000", "cached_input_tokens": "0",
            "output_tokens": "200000", "uncached_input_usd_per_million": "2",
            "cached_input_usd_per_million": "0", "output_usd_per_million": "10"
        }]
        self.assertAlmostEqual(weighted_api_price_per_million(rows), 3.6)

    def test_api_price_empty_is_none(self):
        self.assertIsNone(weighted_api_price_per_million([]))

    def test_cost_scenario_includes_incremental_cost(self):
        result = accepted_cost(1.0, .5, .3, .02)
        self.assertAlmostEqual(result["eis_cost_per_accepted"], .87)
        self.assertTrue(result["break_even"])
        self.assertAlmostEqual(result["maximum_incremental_cost_before_parity"], .15)

    def test_no_advantage_if_incremental_cost_exceeds_energy_saving(self):
        result = accepted_cost(1.0, .3, .2, .08)
        self.assertAlmostEqual(result["eis_cost_per_accepted"], 1.02)
        self.assertFalse(result["break_even"])

    def test_invalid_share_rejected(self):
        with self.assertRaises(ValueError):
            accepted_cost(1.0, 1.2, .2)

    def test_workload_observation_counts_retries(self):
        result = workload_cost_from_observation({
            "total_cost_usd": "2.0", "accepted_outputs": "100", "attempted_outputs": "125"
        })
        self.assertEqual(result["cost_per_accepted_usd"], .02)
        self.assertEqual(result["acceptance_rate"], .8)


if __name__ == "__main__":
    unittest.main()
