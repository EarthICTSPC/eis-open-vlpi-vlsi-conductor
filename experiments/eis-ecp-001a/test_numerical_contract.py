import math
import unittest
import numpy as np

from numerical_contract import (
    output_abs_bound, quantize, score_abs_bound, score_matrix, output_matrix,
)


class NumericalContractTests(unittest.TestCase):
    def test_declared_bounds(self):
        self.assertEqual(score_abs_bound(64), 1.0)
        self.assertEqual(output_abs_bound(64), 64.0)

    def test_score_bound_for_domain(self):
        rng = np.random.default_rng(123)
        D = 64
        Q = rng.uniform(-1 / math.sqrt(D), 1 / math.sqrt(D), (64, D))
        K = rng.uniform(-1 / math.sqrt(D), 1 / math.sqrt(D), (64, D))
        S = score_matrix(Q, K)
        self.assertLessEqual(float(np.max(np.abs(S))), 1.0 + 1e-10)

    def test_rejects_operand_outside_declared_domain(self):
        Q = np.zeros((2, 4)); K = np.zeros((2, 4))
        Q[0, 0] = 0.6
        with self.assertRaises(ValueError):
            score_matrix(Q, K)

    def test_output_bound(self):
        S = np.ones((3, 4))
        V = np.ones((4, 2))
        Y = output_matrix(S, V)
        self.assertTrue(np.all(Y == 4.0))
        self.assertLessEqual(float(np.max(np.abs(Y))), output_abs_bound(4))

    def test_rejects_score_precondition_violation(self):
        with self.assertRaises(ValueError):
            output_matrix(np.array([[1.01]]), np.array([[0.0]]))

    def test_quantizer_reports_saturation_before_clipping(self):
        q = quantize(np.array([-2.0, -1.0, 0.0, 0.5, 1.0, 1.01]), bits=4, full_scale=1.0)
        self.assertEqual(q.saturation_count, 2)
        self.assertEqual(q.element_count, 6)
        self.assertAlmostEqual(q.saturation_rate, 2 / 6)
        self.assertLessEqual(float(np.max(np.abs(q.values))), 1.0)

    def test_quantizer_rejects_bad_configuration(self):
        for args in [(np.array([1.0]), 1, 1.0), (np.array([1.0]), 4, 0.0)]:
            with self.assertRaises(ValueError):
                quantize(*args)

    def test_quantizer_rejects_nonfinite_input(self):
        with self.assertRaises(ValueError):
            quantize(np.array([np.nan]), bits=4, full_scale=1.0)


if __name__ == "__main__":
    unittest.main()
