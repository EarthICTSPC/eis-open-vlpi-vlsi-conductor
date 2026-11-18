import unittest
from benchmark import (compare_outputs, electronic_attention,
    electronic_kka_reference, integrate_power_trace, physical_soi_record,
    softmax_operation_ledger)


def fixture_kka_operator(q_fields, k_fields, causal_offset):
    # Synthetic deterministic fixture only; not a Tian equation or device model.
    nq, nk = len(q_fields), len(k_fields)
    out = []
    for i in range(nq):
        visible = nk if causal_offset is None else min(nk, i + causal_offset + 1)
        out.append([1.0 / visible if j < visible else 0.0 for j in range(nk)])
    return out


class BenchmarkTests(unittest.TestCase):
    def test_electronic_attention_shape_and_normalization(self):
        q = [[1.0, 0.0], [0.0, 1.0]]
        k = [[1.0, 0.0], [0.0, 1.0]]
        v = [[2.0, 0.0], [0.0, 4.0]]
        out = electronic_attention(q, k, v)
        self.assertEqual((len(out), len(out[0])), (2, 2))
        self.assertAlmostEqual(sum(out[0]), 2.0, places=7)

    def test_value_dimension_can_differ_from_qk_dimension(self):
        out = electronic_attention([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]],
                                   [[3.0], [9.0]])
        self.assertEqual(len(out[0]), 1)

    def test_causal_attention(self):
        q = [[1.0, 0.0], [0.0, 1.0]]
        k = [[1.0, 0.0], [0.0, 1.0]]
        v = [[1.0], [9.0]]
        out = electronic_attention(q, k, v, causal=True)
        self.assertAlmostEqual(out[0][0], 1.0, places=7)

    def test_kka_operator_is_required(self):
        with self.assertRaises(ValueError):
            electronic_kka_reference([[1+0j]], [[1+0j]], [[1.0]], None)

    def test_kka_fixture_runs_without_softmax_fallback(self):
        qf, kf, v = [[1+0j], [0+1j]], [[1+0j], [0+1j]], [[2.0], [4.0]]
        out = electronic_kka_reference(qf, kf, v, fixture_kka_operator)
        self.assertEqual(out, [[3.0], [3.0]])

    def test_output_metrics(self):
        metrics = compare_outputs([[1.0, 2.0]], [[1.0, 2.0]])
        self.assertEqual(metrics.max_abs_error, 0.0)
        self.assertAlmostEqual(metrics.cosine_similarity, 1.0)

    def test_power_trace_integration(self):
        self.assertAlmostEqual(integrate_power_trace([(0.0, 2.0), (1.0, 2.0)]), 2.0)

    def test_power_trace_rejects_non_monotonic_time(self):
        with self.assertRaises(ValueError):
            integrate_power_trace([(1.0, 2.0), (1.0, 3.0)])

    def test_physical_record_integrates_component_traces(self):
        record = physical_soi_record([[0.5]], {
            "laser": [(0.0, 2.0), (1.0, 2.0)],
            "detector": [(0.0, 1.0), (1.0, 1.0)],
        }, latency_s=0.25)
        self.assertAlmostEqual(record.total_energy_j, 3.0)
        self.assertEqual(record.latency_s, 0.25)

    def test_operation_ledger_preserves_operation_types(self):
        ledger = softmax_operation_ledger(4, 2)
        self.assertEqual(ledger["softmax_exponentials"], 32)
        self.assertEqual(ledger["score_scale_multiplications"], 32)
        self.assertEqual(ledger["softmax_row_sum_additions"], 24)


if __name__ == "__main__":
    unittest.main()
