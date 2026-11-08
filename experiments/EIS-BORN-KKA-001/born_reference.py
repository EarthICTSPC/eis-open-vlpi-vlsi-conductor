"""Dependency-free scalar reference for EIS-BORN-KKA-001.

This is an executable mathematical reference, not an optical-device simulator.
All complex amplitudes are dimensionless under a caller-declared normalization.
"""
from __future__ import annotations

import cmath
import math
from collections.abc import Sequence


def _finite_complex(z: complex, name: str) -> None:
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise ValueError(f"{name} must have finite real and imaginary parts")


def overlap(q: Sequence[complex], k: Sequence[complex]) -> complex:
    """Return <q,k> = sum_r q[r] * conjugate(k[r])."""
    if len(q) != len(k):
        raise ValueError("query and key dimensions must match")
    total = 0j
    for index, (qv, kv) in enumerate(zip(q, k, strict=True)):
        _finite_complex(complex(qv), f"q[{index}]")
        _finite_complex(complex(kv), f"k[{index}]")
        total += qv * kv.conjugate()
    _finite_complex(total, "overlap")
    return total


def born_score(q: Sequence[complex], k: Sequence[complex]) -> float:
    """Return |<q,k>|^4 = (|<q,k>|^2)^2."""
    z = overlap(q, k)
    intensity = z.real * z.real + z.imag * z.imag
    score = intensity * intensity
    if not math.isfinite(score):
        raise ValueError("Born score overflowed or became non-finite")
    return score


def born_attention(
    q: Sequence[complex], keys: Sequence[Sequence[complex]]
) -> list[float]:
    """Return fourth-power Born scores normalized across one key row.

    A zero or non-finite denominator is rejected. No epsilon, clipping, or
    fallback distribution is silently introduced.
    """
    scores = [born_score(q, key) for key in keys]
    denominator = math.fsum(scores)
    if not math.isfinite(denominator) or denominator <= 0.0:
        raise ValueError("Born attention row requires a finite positive denominator")
    return [score / denominator for score in scores]


def kka_cross_term(a: complex, b: complex) -> float:
    """EIS signed balanced cross-term: 2*Re(a*conjugate(b))."""
    _finite_complex(a, "a")
    _finite_complex(b, "b")
    return 2.0 * (a * b.conjugate()).real


def measured_bilinear_readout(x: complex, y: complex) -> float:
    """Scalar measured feed-forward target Re(x*y)."""
    _finite_complex(x, "x")
    _finite_complex(y, "y")
    return (x * y).real


def kka_bilinear_bridge(x: complex, y: complex) -> float:
    """Return X(x, conjugate(y))/2, algebraically equal to Re(x*y)."""
    return 0.5 * kka_cross_term(x, y.conjugate())


def born_score_from_quadratures(real_overlap: float, imag_overlap: float) -> float:
    """Return (real^2 + imag^2)^2 from two overlap quadratures."""
    if not (math.isfinite(real_overlap) and math.isfinite(imag_overlap)):
        raise ValueError("overlap quadratures must be finite")
    intensity = real_overlap**2 + imag_overlap**2
    score = intensity**2
    if not math.isfinite(score):
        raise ValueError("quadrature Born score overflowed or became non-finite")
    return score
