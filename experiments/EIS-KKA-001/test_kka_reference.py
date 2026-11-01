import pathlib
import sys
import unittest

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kka_reference import (  # noqa: E402
    integrate_current,
    real_cross_term_current,
    real_cross_term_current_direct,
)


class KKA001AMathematicalConformance(unittest.TestCase):
    def setUp(self):
        self.r = 0.85
        self.scale_w = 1.0

    def test_constructive_interference(self):
        y = real_cross_term_current(1 + 0j, 1 + 0j, self.r, power_scale_w=self.scale_w)
        self.assertAlmostEqual(y, 2 * self.r * self.scale_w, places=12)

    def test_destructive_interference(self):
        y = real_cross_term_current(1 + 0j, np.exp(1j * np.pi), self.r, power_scale_w=self.scale_w)
        self.assertAlmostEqual(y, -2 * self.r * self.scale_w, places=12)

    def test_quadrature_is_zero_for_real_cross_term(self):
        y = real_cross_term_current(1 + 0j, np.exp(1j * np.pi / 2), self.r, power_scale_w=self.scale_w)
        self.assertAlmostEqual(y, 0.0, places=12)

    def test_coupler_powers_match_closed_form(self):
        rng = np.random.default_rng(20261101)
        for _ in range(100):
            a = rng.normal() + 1j * rng.normal()
            b = rng.normal() + 1j * rng.normal()
            via_ports = real_cross_term_current(a, b, self.r, power_scale_w=0.002)
            direct = real_cross_term_current_direct(a, b, self.r, power_scale_w=0.002)
            self.assertAlmostEqual(via_ports, direct, places=12)

    def test_integral_returns_charge_and_average_current(self):
        t = np.array([0.0, 1.0, 2.0]) * 1e-9
        current = np.array([2.0, 2.0, 2.0]) * 1e-6
        charge, average = integrate_current(t, current)
        self.assertAlmostEqual(charge, 4e-15, delta=1e-27)
        self.assertAlmostEqual(average, 2e-6, delta=1e-18)

    def test_nonmonotonic_time_rejected(self):
        with self.assertRaises(ValueError):
            integrate_current(np.array([0.0, 1.0, 0.5]), np.array([1.0, 1.0, 1.0]))


if __name__ == "__main__":
    unittest.main()
