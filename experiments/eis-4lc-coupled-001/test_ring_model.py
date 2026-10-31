import math
import unittest

from ring_model import (
    RingParameters, assert_matched_eo_load, derivative, energy_rate_w,
    ideal_modes, ideal_quadrature_frequency_hz, ring_laplacian, simulate,
    stored_energy_j, voltage_mode_projection, dissipated_power_w, input_power_w,
)


class FourLCRingTests(unittest.TestCase):
    def setUp(self):
        self.ideal = RingParameters.from_sequences(
            inductance_h=(1e-6,)*4,
            branch_resistance_ohm=(0,)*4,
            shunt_capacitance_f=(1e-9,)*4,
        )

    def test_graph_laplacian_eigenpairs(self):
        for _, (basis, eigenvalue) in ideal_modes().items():
            got = ring_laplacian(basis)
            expected = tuple(eigenvalue*x for x in basis)
            for a, b in zip(got, expected):
                self.assertAlmostEqual(a, b, places=14)

    def test_quadrature_frequency(self):
        expected = math.sqrt(2/(1e-6*1e-9))/(2*math.pi)
        self.assertAlmostEqual(ideal_quadrature_frequency_hz(1e-6, 1e-9), expected)

    def test_opposite_node_differential_outputs(self):
        cos_mode = (1.0, 0.0, -1.0, 0.0)
        sin_mode = (0.0, 1.0, 0.0, -1.0)
        self.assertEqual(cos_mode[0]-cos_mode[2], 2.0)
        self.assertEqual(cos_mode[1]-cos_mode[3], 0.0)
        self.assertEqual(sin_mode[0]-sin_mode[2], 0.0)
        self.assertEqual(sin_mode[1]-sin_mode[3], 2.0)

    def test_power_balance_identity_at_state(self):
        p = RingParameters.from_sequences(
            inductance_h=(2e-6, 2.1e-6, 1.9e-6, 2e-6),
            branch_resistance_ohm=(0.1, 0.2, 0.15, 0.1),
            shunt_capacitance_f=(2e-9,)*4,
            eo_load_capacitance_f=(0.2e-9,)*4,
            eo_load_conductance_s=(1e-5, 2e-5, 1e-5, 2e-5),
        )
        state = (1.0, -0.4, 0.2, -0.1, 0.001, -0.002, 0.0015, -0.0005)
        drive = (2e-4, -1e-4, 1e-4, 0.0)
        ds = derivative(p, state, drive)
        lhs = energy_rate_w(p, state, ds)
        rhs = input_power_w(state, drive)-dissipated_power_w(p, state)
        self.assertAlmostEqual(lhs, rhs, delta=1e-15)

    def test_ideal_ring_energy_conserved_by_rk4(self):
        initial = (1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        e0 = stored_energy_j(self.ideal, initial)
        omega = math.sqrt(2/(1e-6*1e-9))
        dt = (2*math.pi/omega)/2000
        samples = simulate(self.ideal, initial, 20*dt*200, dt, sample_every=200)
        for sample in samples:
            self.assertAlmostEqual(sample.stored_energy_j, e0, delta=e0*2e-8)

    def test_voltage_projection_is_not_mislabeled_as_modal_energy(self):
        projection = voltage_mode_projection((1.0, 0.0, -1.0, 0.0))
        self.assertAlmostEqual(projection["quadrature_cos"], 1.0)
        self.assertAlmostEqual(projection["quadrature_sin"], 0.0)

    def test_candidate_comparison_requires_same_eo_load(self):
        changed_load = RingParameters.from_sequences(
            inductance_h=(1e-6,)*4,
            branch_resistance_ohm=(0,)*4,
            shunt_capacitance_f=(1e-9,)*4,
            eo_load_capacitance_f=(0.1e-9, 0, 0, 0),
        )
        with self.assertRaises(ValueError):
            assert_matched_eo_load(self.ideal, changed_load)

    def test_load_validation_fails_closed(self):
        with self.assertRaises(ValueError):
            RingParameters.from_sequences(
                inductance_h=(1e-6,)*4,
                branch_resistance_ohm=(0,)*4,
                shunt_capacitance_f=(1e-9,)*4,
                eo_load_capacitance_f=(-1e-12, 0, 0, 0),
            )


if __name__ == "__main__":
    unittest.main()
