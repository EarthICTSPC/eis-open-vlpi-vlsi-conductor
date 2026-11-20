import unittest

from eis_kka_ref.qwen3 import load_pinned_config


class Qwen3MappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shape = load_pinned_config()

    def test_pinned_dimensions(self):
        s = self.shape
        self.assertEqual(s.hidden_size, 4096)
        self.assertEqual(s.num_attention_heads, 32)
        self.assertEqual(s.num_key_value_heads, 8)
        self.assertEqual(s.head_dim, 128)
        self.assertEqual(s.num_hidden_layers, 36)
        self.assertEqual(s.queries_per_kv_head, 4)

    def test_projection_shapes(self):
        s = self.shape
        self.assertEqual(s.q_projection_weight_shape, (4096, 4096))
        self.assertEqual(s.k_projection_weight_shape, (1024, 4096))
        self.assertEqual(s.v_projection_weight_shape, (1024, 4096))
        self.assertEqual(s.o_projection_weight_shape, (4096, 4096))

    def test_gqa_mapping(self):
        s = self.shape
        self.assertEqual([s.kv_head_for_query_head(i) for i in range(32)],
                         [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4 +
                         [4] * 4 + [5] * 4 + [6] * 4 + [7] * 4)

    def test_64_tile_ledger(self):
        ledger = self.shape.tile_ledger()
        self.assertEqual(ledger["scores_per_head"], 4096)
        self.assertEqual(ledger["scores_all_query_heads"], 131072)
        self.assertEqual(ledger["qk_scalar_pair_terms"], 16777216)
        self.assertEqual(ledger["av_scalar_pair_terms"], 16777216)
        self.assertEqual(ledger["kv_cache_elements_per_token_per_layer"], 2048)

    def test_tensor_shapes(self):
        shapes = self.shape.tensor_shapes(batch=1, sequence=64)
        self.assertEqual(shapes["q"], (1, 32, 64, 128))
        self.assertEqual(shapes["k"], (1, 8, 64, 128))
        self.assertEqual(shapes["v"], (1, 8, 64, 128))
        self.assertEqual(shapes["attention_scores"], (1, 32, 64, 64))


if __name__ == "__main__":
    unittest.main()
