import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kka_rff_reference import gaussian_rff_exp_dot, normalized_rff_attention


class KKA001ASI2RFF(unittest.TestCase):
    def test_rff_estimator_converges_to_gaussian_kernel(self):
        q = [0.2, -0.1]
        k = [-0.15, 0.25]
        estimate = gaussian_rff_exp_dot(q, k, feature_count=100000, seed=314159)
        exact = __import__("math").exp(sum(a * b for a, b in zip(q, k)))
        self.assertAlmostEqual(estimate, exact, delta=0.01)

    def test_same_seed_is_reproducible(self):
        q = [0.1, 0.2, -0.1]
        k = [0.2, -0.1, 0.3]
        a = gaussian_rff_exp_dot(q, k, feature_count=512, seed=42)
        b = gaussian_rff_exp_dot(q, k, feature_count=512, seed=42)
        self.assertEqual(a, b)

    def test_normalized_attention_weights_sum_to_one(self):
        q = [0.1, -0.2]
        keys = [[0.2, 0.1], [-0.1, 0.3], [0.05, -0.15]]
        values = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
        weights, output = normalized_rff_attention(
            q, keys, values, feature_count=4096, seed=123
        )
        self.assertAlmostEqual(sum(weights), 1.0, places=12)
        self.assertEqual(len(output), 2)

    def test_nonpositive_finite_sample_normalizer_is_not_clipped(self):
        # Deliberately tiny sample counts are permitted to fail rather than
        # silently turn a signed Monte-Carlo estimate into a positive kernel.
        with self.assertRaises(ArithmeticError):
            normalized_rff_attention(
                [0.2], [[0.1], [-0.1]], [[1.0], [2.0]],
                feature_count=1, seed=7
            )


if __name__ == "__main__":
    unittest.main()
