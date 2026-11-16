import cmath
import math
import unittest
from eis_kka_ref import BalancedDetector, ComplexTransfer, apply_complex_transfer, complex_transfer, kka_activation

class ComplexTransferTests(unittest.TestCase):
    def test_polar_transfer_and_apply(self):
        h = complex_transfer(0.5, math.pi / 2)
        self.assertAlmostEqual(h.real, 0.0, places=14)
        self.assertAlmostEqual(h.imag, 0.5, places=14)
        field = apply_complex_transfer(2 + 0j, ComplexTransfer(0.5, math.pi / 2))
        self.assertAlmostEqual(field.real, 0.0, places=14)
        self.assertAlmostEqual(field.imag, 1.0, places=14)

    def test_from_complex_round_trip(self):
        original = 0.3 - 0.4j
        rebuilt = ComplexTransfer.from_complex(original).coefficient
        self.assertAlmostEqual(rebuilt.real, original.real, places=14)
        self.assertAlmostEqual(rebuilt.imag, original.imag, places=14)

    def test_rejects_invalid_transfer(self):
        with self.assertRaises(ValueError): ComplexTransfer(-0.1, 0.0)
        with self.assertRaises(ValueError): complex_transfer(float("nan"), 0.0)

class KKAActivationTests(unittest.TestCase):
    def test_zero_phase_is_identity(self):
        self.assertAlmostEqual(kka_activation(0.7, lambda _a: 0.0), 0.7)

    def test_nonzero_phase_matches_equation(self):
        amplitude, theta_n = 0.8, 0.2
        phi = lambda a: 0.4 * a
        expected = amplitude * math.cos(phi(amplitude) + theta_n) / math.cos(theta_n)
        self.assertAlmostEqual(kka_activation(amplitude, phi, theta_n), expected)

    def test_zero_amplitude(self):
        self.assertEqual(kka_activation(0.0, lambda _a: 1.2), 0.0)

    def test_singular_normalization_rejected(self):
        with self.assertRaises(ValueError): kka_activation(1.0, lambda _a: 0.0, math.pi / 2)

    def test_invalid_phase_response_rejected(self):
        with self.assertRaises(ValueError): kka_activation(1.0, lambda _a: float("nan"))

class BalancedDetectorTests(unittest.TestCase):
    def test_in_phase_constructive(self):
        r = BalancedDetector().measure(1+0j, 1+0j)
        self.assertAlmostEqual(r.differential_current_a, 2.0)
        self.assertAlmostEqual(r.current_plus_a, 2.0)
        self.assertAlmostEqual(r.current_minus_a, 0.0)

    def test_opposite_phase_destructive_signed_output(self):
        r = BalancedDetector().measure(1+0j, -1+0j)
        self.assertAlmostEqual(r.differential_current_a, -2.0)
        self.assertAlmostEqual(r.current_plus_a, 0.0)
        self.assertAlmostEqual(r.current_minus_a, 2.0)

    def test_quadrature_zero_cross_term(self):
        self.assertAlmostEqual(BalancedDetector().measure(1+0j, 1j).differential_current_a, 0.0, places=14)

    def test_unequal_amplitudes(self):
        self.assertAlmostEqual(BalancedDetector().measure(2+0j, 0.5+0j).differential_current_a, 2.0)

    def test_zero_arm(self):
        self.assertAlmostEqual(BalancedDetector().measure(0j, 2+1j).differential_current_a, 0.0)

    def test_phase_sweep_matches_analytic_cross_term(self):
        detector = BalancedDetector(responsivity_a_per_unit=0.73)
        for index in range(37):
            phase = -math.pi + 2 * math.pi * index / 36
            a, b = 0.8 * cmath.exp(0.31j), 0.4 * cmath.exp(1j * phase)
            expected = 0.73 * 2 * (a * b.conjugate()).real
            self.assertAlmostEqual(detector.measure(a, b).differential_current_a, expected, places=13)

    def test_gain_mismatch_and_offsets_are_explicit(self):
        d = BalancedDetector(0.5, 1.1, 0.9, 0.01, -0.02)
        r = d.measure(1+0j, 1+0j)
        self.assertAlmostEqual(r.current_plus_a, 1.11)
        self.assertAlmostEqual(r.current_minus_a, -0.02)
        self.assertAlmostEqual(r.differential_current_a, 1.13)

if __name__ == "__main__":
    unittest.main()
