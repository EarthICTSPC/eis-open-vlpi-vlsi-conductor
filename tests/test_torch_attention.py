import unittest

try:
    import torch
    from eis_kka_ref.torch_attention import KKAInterferenceCore
except ImportError:
    torch = None
    KKAInterferenceCore = None


@unittest.skipIf(torch is None, "optional PyTorch dependency is not installed")
class KKAInterferenceCoreTests(unittest.TestCase):
    def test_gqa_shapes_and_normalized_probabilities(self):
        torch.manual_seed(7)
        core = KKAInterferenceCore(query_heads=4, kv_heads=2, head_dim=8)
        q = torch.randn(2, 4, 5, 8, requires_grad=True)
        k = torch.randn(2, 2, 5, 8, requires_grad=True)
        v = torch.randn(2, 2, 5, 8, requires_grad=True)
        output, probabilities = core(q, k, v)
        self.assertEqual(tuple(output.shape), (2, 4, 5, 8))
        self.assertEqual(tuple(probabilities.shape), (2, 4, 5, 5))
        self.assertTrue(torch.allclose(
            probabilities.sum(dim=-1), torch.ones(2, 4, 5), atol=1e-6
        ))

    def test_kappa_receives_gradient(self):
        core = KKAInterferenceCore(query_heads=2, kv_heads=1, head_dim=4)
        q = torch.randn(1, 2, 3, 4)
        k = torch.randn(1, 1, 3, 4)
        v = torch.randn(1, 1, 3, 4)
        output, _ = core(q, k, v)
        output.square().mean().backward()
        self.assertIsNotNone(core.kappa.grad)
        self.assertTrue(torch.isfinite(core.kappa.grad).all())


if __name__ == "__main__":
    unittest.main()
