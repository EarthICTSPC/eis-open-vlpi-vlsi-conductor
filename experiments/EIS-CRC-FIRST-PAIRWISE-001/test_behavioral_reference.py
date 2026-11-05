import unittest

from behavioral_reference import ComparatorInput, Decision, reference_decision


class PairwiseReferenceTests(unittest.TestCase):
    def test_a_wins_for_gap_outside_indifference_band(self):
        self.assertEqual(
            reference_decision(ComparatorInput(0.9, 0.2, 0.1)),
            Decision.A_WINS,
        )

    def test_b_wins_for_gap_outside_indifference_band(self):
        self.assertEqual(
            reference_decision(ComparatorInput(0.2, 0.9, 0.1)),
            Decision.B_WINS,
        )

    def test_equal_scores_are_indeterminate(self):
        self.assertEqual(
            reference_decision(ComparatorInput(0.5, 0.5, 0.0)),
            Decision.INDETERMINATE,
        )

    def test_gap_at_boundary_is_indeterminate(self):
        self.assertEqual(
            reference_decision(ComparatorInput(0.6, 0.5, 0.1)),
            Decision.INDETERMINATE,
        )

    def test_negative_gap_is_fault(self):
        self.assertEqual(
            reference_decision(ComparatorInput(0.8, 0.2, -0.1)),
            Decision.FAULT,
        )

    def test_nan_is_fault(self):
        self.assertEqual(
            reference_decision(ComparatorInput(float("nan"), 0.2, 0.0)),
            Decision.FAULT,
        )


if __name__ == "__main__":
    unittest.main()
