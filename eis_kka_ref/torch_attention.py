"""Experimental differentiable KKA-compatible attention core.

This is a trainable numerical surrogate, not a measured modulator model and
not a reproduction of Tian's full PTC algorithm. It consumes Q/K/V tensors
after the model's own projections, normalization and positional encoding.
SoftMax and value aggregation remain explicit electronic reference stages.
"""
from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError as exc:  # pragma: no cover - exercised only without torch
    raise ImportError(
        "torch_attention requires the optional 'torch' dependency"
    ) from exc


class KKAInterferenceCore(nn.Module):
    """One trainable GQA-compatible attention core using ideal BPD scores.

    Inputs:
      q: [batch, query_heads, query_length, head_dim]
      k: [batch, kv_heads, key_length, head_dim]
      v: [batch, kv_heads, key_length, value_dim]

    The surrogate uses A(u)=sigmoid(u), phi(u)=kappa*ln(A(u)).
    The learned kappa is an experimental constant-slope amplitude/phase
    coupling parameter. Replace this surrogate with a calibrated measured
    complex transfer table before making physical claims.
    """

    def __init__(
        self,
        query_heads: int = 32,
        kv_heads: int = 8,
        head_dim: int = 128,
        *,
        initial_kappa: float = 0.25,
        eps: float = 1e-6,
    ) -> None:
        super().__init__()
        if query_heads <= 0 or kv_heads <= 0 or head_dim <= 0:
            raise ValueError("head counts and head_dim must be positive")
        if query_heads % kv_heads:
            raise ValueError("query_heads must be divisible by kv_heads")
        if eps <= 0:
            raise ValueError("eps must be positive")
        self.query_heads = query_heads
        self.kv_heads = kv_heads
        self.head_dim = head_dim
        self.group_size = query_heads // kv_heads
        self.eps = float(eps)
        self.kappa = nn.Parameter(torch.full((query_heads,), float(initial_kappa)))

    def _encode(self, drive: torch.Tensor, kappa: torch.Tensor) -> torch.Tensor:
        amplitude = torch.sigmoid(drive).clamp_min(self.eps)
        phase = kappa.view(1, -1, 1, 1) * torch.log(amplitude)
        return torch.polar(amplitude, phase)

    def forward(
        self,
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        *,
        causal: bool = True,
        attention_mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if q.ndim != 4 or k.ndim != 4 or v.ndim != 4:
            raise ValueError("q, k and v must be rank-4 tensors")
        batch, q_heads, q_len, dim = q.shape
        kb, kv_heads, k_len, k_dim = k.shape
        vb, v_heads, v_len, value_dim = v.shape
        if kb != batch or vb != batch or kv_heads != self.kv_heads:
            raise ValueError("batch or KV-head dimensions do not match")
        if q_heads != self.query_heads or dim != self.head_dim or k_dim != dim:
            raise ValueError("query head dimensions do not match this module")
        if v_heads != kv_heads or v_len != k_len:
            raise ValueError("key/value dimensions do not match")
        if q.device != k.device or q.device != v.device:
            raise ValueError("q, k and v must be on the same device")
        if q.dtype != k.dtype or q.dtype != v.dtype:
            raise ValueError("q, k and v must have the same dtype")

        k_expanded = k.repeat_interleave(self.group_size, dim=1)
        v_expanded = v.repeat_interleave(self.group_size, dim=1)
        # Field encoding and detector arithmetic use float32 even when the
        # surrounding transformer runs BF16/FP16.
        q_field = self._encode(q.float(), self.kappa.float())
        k_field = self._encode(k_expanded.float(), self.kappa.float())

        # Ideal balanced detector: I+ - I- = 2 R Re(q * conj(k)); R=1 here.
        scores = 2.0 * torch.matmul(
            q_field, k_field.conj().transpose(-2, -1)
        ).real / (self.head_dim ** 0.5)

        if causal:
            q_positions = torch.arange(q_len, device=q.device) + max(0, k_len - q_len)
            k_positions = torch.arange(k_len, device=q.device)
            causal_mask = k_positions.view(1, 1, 1, k_len) <= q_positions.view(1, 1, q_len, 1)
            scores = scores.masked_fill(~causal_mask, torch.finfo(scores.dtype).min)
        if attention_mask is not None:
            mask = attention_mask.to(device=scores.device, dtype=torch.bool)
            while mask.ndim < scores.ndim:
                mask = mask.unsqueeze(1)
            scores = scores.masked_fill(~mask, torch.finfo(scores.dtype).min)

        probabilities = torch.softmax(scores, dim=-1)
        output = torch.matmul(probabilities, v_expanded.float()).to(v.dtype)
        return output, probabilities
