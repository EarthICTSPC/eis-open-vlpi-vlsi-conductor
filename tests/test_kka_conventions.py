import math
import unittest

from eis_kka_ref.kka import (
    AMPLITUDE_CONVENTION,
    BALANCED_DETECTOR_CONVENTION,
    PHASOR_CONVENTION,
    kappa_a_from_drive,
    kappa_i_from_drive,
)


class KKAConventionTests(unittest.TestCase):
    def test_conventions_are_explicit(self):
        self.assertIn("exp(+i*omega*t)", PHASOR_CONVENTION)
        self.assertIn("field-amplitude", AMPLITUDE_CONVENTION)
        self.assertIn("2*R", BALANCED_DETECTOR_CONVENTION)

    def test_reference_mzi_trajectory(self):
        # H(u)=(1+exp(iu))/2 = exp(iu/2) cos(u/2), on 0<u<pi.
        amplitude = lambda u: math.cos(u / 2.0)
        phase = lambda u: u / 2.0
        u = 0.8
        expected = -1.0 / math.tan(u / 2.0)
        actual = kappa_a_from_drive(amplitude, phase, u, step=1e-6)
        self.assertAlmostEqual(actual, expected, places=8)

    def test_intensity_convention_is_half_field_convention(self):
        amplitude = lambda u: math.cos(u / 2.0)
        phase = lambda u: u / 2.0
        u = 0.8
        kappa_a = kappa_a_from_drive(amplitude, phase, u, step=1e-6)
        kappa_i = kappa_i_from_drive(amplitude, phase, u, step=1e-6)
        self.assertAlmostEqual(kappa_i, kappa_a / 2.0, places=12)

    def test_zero_amplitude_is_rejected(self):
        with self.assertRaises(ValueError):
            kappa_a_from_drive(lambda _u: 0.0, lambda u: u, 0.0)

    def test_stationary_amplitude_is_rejected(self):
        with self.assertRaises(ValueError):
            kappa_a_from_drive(lambda _u: 0.5, lambda u: u, 0.3)

    def test_invalid_step_is_rejected(self):
        with self.assertRaises(ValueError):
            kappa_a_from_drive(lambda u: 1.0 + u, lambda u: u, 0.1, step=0.0)

    def test_nonfinite_phase_is_rejected(self):
        with self.assertRaises(ValueError):
            kappa_a_from_drive(lambda u: 1.0 + u, lambda _u: float("nan"), 0.1)


if __name__ == "__main__":
    unittest.main()
