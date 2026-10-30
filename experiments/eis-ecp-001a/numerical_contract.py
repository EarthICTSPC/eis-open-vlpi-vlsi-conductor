"""EIS-ECP-001A numerical helpers.

These functions implement software-level bounds and quantization accounting.
They are not a device model and do not establish Lean/Python conformance.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class Quantized:
    values: np.ndarray
    saturation_count: int
    element_count: int
    full_scale: float
    bits: int

    @property
    def saturation_rate(self) -> float:
        return self.saturation_count / self.element_count if self.element_count else 0.0


def score_abs_bound(D: int) -> float:
    """Bound |q dot k| when each coordinate is in [-1/sqrt(D), 1/sqrt(D)]."""
    if D <= 0:
        raise ValueError("D must be positive")
    # Each vector norm <= 1, hence Cauchy-Schwarz bounds the dot product by 1.
    return 1.0


def output_abs_bound(T: int) -> float:
    """Bound |sum_j score_j * V_j| for |score_j|<=1 and |V_j|<=1."""
    if T <= 0:
        raise ValueError("T must be positive")
    return float(T)


def quantize(x, bits: int, full_scale: float) -> Quantized:
    """Symmetric signed quantization; full_scale is the maximum represented magnitude.

    Values with |x| > full_scale are clipped and counted before clipping.
    """
    arr = np.asarray(x, dtype=np.float64)
    if bits < 2:
        raise ValueError("bits must be >= 2")
    if not math.isfinite(full_scale) or full_scale <= 0:
        raise ValueError("full_scale must be finite and > 0")
    if not np.all(np.isfinite(arr)):
        raise ValueError("input contains NaN or infinity")
    levels = 2 ** (bits - 1) - 1
    saturated = int(np.count_nonzero(np.abs(arr) > full_scale))
    step = full_scale / levels
    q = np.clip(np.rint(arr / step), -levels, levels) * step
    return Quantized(q, saturated, int(arr.size), float(full_scale), bits)


def score_matrix(Q, K):
    """Compute scores and assert declared operand-domain assumptions."""
    Q = np.asarray(Q, dtype=np.float64)
    K = np.asarray(K, dtype=np.float64)
    if Q.ndim != 2 or K.ndim != 2 or Q.shape[1] != K.shape[1]:
        raise ValueError("Q and K must be 2-D with matching feature dimension")
    D = Q.shape[1]
    limit = 1.0 / math.sqrt(D)
    if np.any(np.abs(Q) > limit + 1e-12) or np.any(np.abs(K) > limit + 1e-12):
        raise ValueError("Q/K values violate the declared input domain")
    S = Q @ K.T
    if np.any(np.abs(S) > score_abs_bound(D) + 1e-10):
        raise AssertionError("computed score violates Cauchy-Schwarz bound")
    return S


def output_matrix(S, V):
    """Compute unnormalized output and enforce the declared score/V domain."""
    S = np.asarray(S, dtype=np.float64)
    V = np.asarray(V, dtype=np.float64)
    if S.ndim != 2 or V.ndim != 2 or S.shape[1] != V.shape[0]:
        raise ValueError("S and V shapes are incompatible")
    if np.any(np.abs(S) > 1.0 + 1e-10):
        raise ValueError("scores violate |score| <= 1 precondition")
    if np.any(np.abs(V) > 1.0 + 1e-12):
        raise ValueError("V violates declared |V| <= 1 domain")
    Y = S @ V
    if np.any(np.abs(Y) > output_abs_bound(S.shape[1]) + 1e-8):
        raise AssertionError("computed output violates triangle-inequality bound")
    return Y
