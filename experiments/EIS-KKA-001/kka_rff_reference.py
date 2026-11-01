from __future__ import annotations

"""SI-2 random-Fourier-feature reference, kept separate from device physics.

Implements the Gaussian identity used in Tian et al., Supporting Information
SI-2, Eqs. S5-S6. It does NOT infer the physical amplitude-phase transfer
function of their chip and does NOT claim a measured KKA device implements
these random features.
"""
import cmath
import math
import random
from typing import Sequence


def gaussian_complex_feature(x: Sequence[float], omega: Sequence[float]) -> complex:
    """exp(i*omega·x - ||x||²/2), the q-side feature after q -> i q."""
    if len(x) != len(omega) or not x:
        raise ValueError("x and omega must have the same non-zero dimension")
    norm_sq = sum(float(v) ** 2 for v in x)
    phase = sum(float(w) * float(v) for w, v in zip(omega, x))
    return cmath.exp(complex(-0.5 * norm_sq, phase))


def gaussian_rff_exp_dot(
    q: Sequence[float],
    k: Sequence[float],
    *,
    feature_count: int = 4096,
    seed: int = 0,
) -> float:
    """Monte-Carlo estimate of exp(q·k) using SI-2's shared Gaussian samples.

    E_omega Re[z_omega(q) * conjugate(z_omega(-k))] is exp(q·k).
    Here z_omega(-k) is evaluated at -k, equivalently the second factor
    exp(-i*omega·k - ||k||²/2). The same omega sample is used on both sides.
    """
    if len(q) != len(k) or not q:
        raise ValueError("q and k must have the same non-zero dimension")
    if feature_count < 1:
        raise ValueError("feature_count must be >= 1")
    rng = random.Random(seed)
    total = 0.0
    for _ in range(feature_count):
        omega = [rng.gauss(0.0, 1.0) for _ in q]
        q_feature = gaussian_complex_feature(q, omega)
        k_feature_conjugate = gaussian_complex_feature(k, omega).conjugate()
        total += (q_feature * k_feature_conjugate).real
    return total / feature_count


def normalized_rff_attention(
    q: Sequence[float],
    keys: Sequence[Sequence[float]],
    values: Sequence[Sequence[float]],
    *,
    feature_count: int = 4096,
    seed: int = 0,
) -> tuple[list[float], list[float]]:
    """Approximate one query's softmax-weighted value sum via RFF kernel ratios.

    Returns (normalized_weights, output). Raises if the finite-sample kernel
    estimates do not yield a positive normalizer; no clipping is silently used.
    """
    if not keys or len(keys) != len(values):
        raise ValueError("keys and values must be non-empty and have equal length")
    value_dim = len(values[0])
    if value_dim == 0 or any(len(v) != value_dim for v in values):
        raise ValueError("all value vectors must have the same non-zero dimension")
    kernels = [
        gaussian_rff_exp_dot(q, key, feature_count=feature_count, seed=seed + j)
        for j, key in enumerate(keys)
    ]
    denominator = sum(kernels)
    if not math.isfinite(denominator) or denominator <= 0.0:
        raise ArithmeticError("finite-sample RFF normalizer is not positive")
    weights = [v / denominator for v in kernels]
    output = [
        sum(weights[j] * float(values[j][d]) for j in range(len(values)))
        for d in range(value_dim)
    ]
    return weights, output
