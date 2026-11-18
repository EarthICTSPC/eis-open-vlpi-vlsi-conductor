import unittest

from formal_counts import COUNTS, FORMAL_SPEC, SHAPE


class FormalCountTests(unittest.TestCase):
    def test_spec_identity_and_shape(self):
        self.assertEqual(FORMAL_SPEC["spec_id"], "EIS-KKA-BENCH-001A")
        self.assertEqual(SHAPE, {
            "heads": 2, "sequence_length": 10,
            "head_dimension": 5, "value_dimension": 5,
        })

    def test_tian_eq2_is_not_encoded_as_universal_equality(self):
        self.assertEqual(
            FORMAL_SPEC["tian_eq2_status"],
            "approximation_claim_not_universal_identity",
        )

    def test_operation_classes_are_not_collapsed(self):
        self.assertEqual(COUNTS["score_scaling_multiplications"], 200)
        self.assertEqual(COUNTS["softmax_score_subtractions"], 200)
        self.assertEqual(COUNTS["softmax_exponentials"], 200)
        self.assertEqual(COUNTS["softmax_normalization_divisions"], 200)
        self.assertEqual(COUNTS["softmax_row_max_comparisons"], 180)
        self.assertEqual(COUNTS["softmax_row_sum_additions"], 180)

    def test_kka_interference_events_are_separate_from_mac_counts(self):
        self.assertEqual(COUNTS["qk_multiplications"], 1000)
        self.assertEqual(COUNTS["av_multiplications"], 1000)
        self.assertEqual(COUNTS["kka_qk_interference_samples"], 1000)
        self.assertEqual(COUNTS["kka_av_interference_samples"], 1000)
        self.assertEqual(COUNTS["kka_total_interference_samples"], 2000)

    def test_softmax_shorthand_is_not_the_whole_reduction_cost(self):
        s = SHAPE["sequence_length"]
        h = SHAPE["heads"]
        scores = h * s * s
        triad = (
            COUNTS["softmax_score_subtractions"]
            + COUNTS["softmax_exponentials"]
            + COUNTS["softmax_normalization_divisions"]
        )
        self.assertEqual(triad, 3 * scores)
        self.assertEqual(COUNTS["softmax_row_max_comparisons"], h * s * (s - 1))
        self.assertEqual(COUNTS["softmax_row_sum_additions"], h * s * (s - 1))


if __name__ == "__main__":
    unittest.main()
