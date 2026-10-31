import unittest

from eo_reference import (
    LEE_2024_TFLN_SIN,
    ideal_quadrature_frequency_hz,
    matched_pair_mean_eo_energy_j,
    reported_style_sinusoidal_energy_j,
    required_ring_inductance_h,
)


class PublishedEOReferenceTests(unittest.TestCase):
    def test_published_case_provenance_and_values(self):
        case = LEE_2024_TFLN_SIN
        case.validate()
        self.assertAlmostEqual(case.differential_capacitance_f, 0.98e-12)
        self.assertAlmostEqual(case.half_wave_voltage_v, 3.64)
        self.assertAlmostEqual(case.reported_energy_per_pi_j, 3.2e-12)
        self.assertAlmostEqual(case.interaction_length_m, 15.6e-3)
        self.assertAlmostEqual(case.estimated_bandwidth_hz, 1.2e9)
        self.assertAlmostEqual(case.measured_test_bandwidth_hz, 2.9e9)
        self.assertAlmostEqual(case.measured_test_length_m, 9.4e-3)

    def test_recomputed_sinusoidal_energy_matches_report(self):
        case = LEE_2024_TFLN_SIN
        calculated = reported_style_sinusoidal_energy_j(
            case.differential_capacitance_f, case.half_wave_voltage_v
        )
        self.assertAlmostEqual(calculated*1e12, 3.246, places=3)
        self.assertLess(abs(calculated-case.reported_energy_per_pi_j),
                        0.05e-12)

    def test_two_matched_differential_loads(self):
        self.assertAlmostEqual(
            matched_pair_mean_eo_energy_j(LEE_2024_TFLN_SIN)*1e12,
            6.492, places=3
        )

    def test_zero_node_shunt_inductance_sizing_at_1p2_ghz(self):
        case = LEE_2024_TFLN_SIN
        l_h = required_ring_inductance_h(
            case.estimated_bandwidth_hz, 0.0, case.differential_capacitance_f
        )
        self.assertAlmostEqual(l_h*1e9, 17.95, places=1)
        f = ideal_quadrature_frequency_hz(
            l_h, 0.0, case.differential_capacitance_f
        )
        self.assertAlmostEqual(f, case.estimated_bandwidth_hz, delta=1.0)

    def test_added_node_capacitance_changes_required_inductance(self):
        case = LEE_2024_TFLN_SIN
        l0 = required_ring_inductance_h(
            1.2e9, 0.0, case.differential_capacitance_f
        )
        l1 = required_ring_inductance_h(
            1.2e9, 0.5e-12, case.differential_capacitance_f
        )
        self.assertLess(l1, l0)

    def test_bad_parameters_fail_closed(self):
        with self.assertRaises(ValueError):
            required_ring_inductance_h(0, 0, 0.98e-12)
        with self.assertRaises(ValueError):
            ideal_quadrature_frequency_hz(18e-9, -1e-12, 0.98e-12)
        with self.assertRaises(ValueError):
            reported_style_sinusoidal_energy_j(-1e-12, 3.64)


if __name__ == "__main__":
    unittest.main()
