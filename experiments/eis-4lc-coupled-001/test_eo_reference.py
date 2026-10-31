import unittest

from eo_reference import (
    LEE_2024_TFLN_SIN,
    conditional_ideal_quadrature_frequency_hz,
    conditional_required_ring_inductance_h,
    reported_style_sinusoidal_energy_j,
)


class PublishedEOReferenceTests(unittest.TestCase):
    def test_published_values_and_capacitance_uncertainty_are_explicit(self):
        case = LEE_2024_TFLN_SIN
        case.validate()
        self.assertAlmostEqual(case.capacitance_per_phase_modulator_f, 0.98e-12)
        self.assertEqual(case.capacitance_terminal_definition,
                         "not specified in the paper")
        self.assertIsNone(case.capacitance_measurement_frequency_hz)
        self.assertEqual(case.capacitance_measurement_method,
                         "HIOKI IM3536 LCR meter")
        self.assertAlmostEqual(case.half_wave_voltage_v, 3.64)
        self.assertAlmostEqual(case.reported_energy_per_pi_j, 3.2e-12)
        self.assertAlmostEqual(case.interaction_length_m, 15.6e-3)
        self.assertAlmostEqual(case.estimated_bandwidth_hz, 1.2e9)
        self.assertAlmostEqual(case.measured_test_bandwidth_hz, 2.9e9)
        self.assertAlmostEqual(case.measured_test_length_m, 9.4e-3)

    def test_published_energy_expression_matches_report_with_rounding(self):
        case = LEE_2024_TFLN_SIN
        calculated = reported_style_sinusoidal_energy_j(
            case.capacitance_per_phase_modulator_f, case.half_wave_voltage_v
        )
        self.assertAlmostEqual(calculated*1e12, 3.246, places=3)
        self.assertLess(abs(calculated-case.reported_energy_per_pi_j),
                        0.05e-12)

    def test_conditional_sizing_only_if_098_pf_is_the_differential_port_c(self):
        case = LEE_2024_TFLN_SIN
        # This deliberately hypothetical mapping is NOT established by the paper.
        l_h = conditional_required_ring_inductance_h(
            case.estimated_bandwidth_hz, 0.0,
            case.capacitance_per_phase_modulator_f
        )
        self.assertAlmostEqual(l_h*1e9, 17.95, places=1)
        f = conditional_ideal_quadrature_frequency_hz(
            l_h, 0.0, case.capacitance_per_phase_modulator_f
        )
        self.assertAlmostEqual(f, case.estimated_bandwidth_hz, delta=1.0)

    def test_added_node_capacitance_changes_required_inductance(self):
        c = LEE_2024_TFLN_SIN.capacitance_per_phase_modulator_f
        l0 = conditional_required_ring_inductance_h(1.2e9, 0.0, c)
        l1 = conditional_required_ring_inductance_h(1.2e9, 0.5e-12, c)
        self.assertLess(l1, l0)

    def test_bad_parameters_fail_closed(self):
        with self.assertRaises(ValueError):
            conditional_required_ring_inductance_h(0, 0, 0.98e-12)
        with self.assertRaises(ValueError):
            conditional_ideal_quadrature_frequency_hz(18e-9, -1e-12, 0.98e-12)
        with self.assertRaises(ValueError):
            reported_style_sinusoidal_energy_j(-1e-12, 3.64)


if __name__ == "__main__":
    unittest.main()
