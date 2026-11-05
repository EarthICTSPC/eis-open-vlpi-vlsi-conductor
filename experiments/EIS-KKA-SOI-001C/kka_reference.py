"""Scalar KKA interference reference.

This mirrors the proposed EIS-KKA-001 scalar contract. It is not a Lean-derived
or Lean-verified artifact until the repository contains a pinned Lean project
and the corresponding definitions/theorems are compiled and cross-referenced.
No physical device response is assumed here.
"""
from __future__ import annotations

import math
from typing import SupportsComplex


def _as_finite_complex(value: SupportsComplex, name: str) -> complex:
    try:
        z = complex(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise TypeError(f"{name} must be a complex-convertible scalar") from exc
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise ValueError(f"{name} must have finite real and imaginary parts")
    return z


def propagate(field: SupportsComplex, transfer: SupportsComplex) -> complex:
    """Apply a supplied complex field transfer T to an input field E: E_out=T*E."""
    e = _as_finite_complex(field, "field")
    t = _as_finite_complex(transfer, "transfer")
    out = t * e
    if not (math.isfinite(out.real) and math.isfinite(out.imag)):
        raise ValueError("propagated field is not finite")
    return out


def total_intensity(a: SupportsComplex, b: SupportsComplex) -> float:
    """Return |a+b|^2 for coherently combined, normalized complex envelopes."""
    x = _as_finite_complex(a, "a")
    y = _as_finite_complex(b, "b")
    result = abs(x + y) ** 2
    if not math.isfinite(result):
        raise ValueError("total intensity is not finite")
    return float(result)


def cross_term(a: SupportsComplex, b: SupportsComplex) -> float:
    """Return the signed balanced cross term 2*Re(a*conj(b)); do not clip."""
    x = _as_finite_complex(a, "a")
    y = _as_finite_complex(b, "b")
    result = 2.0 * (x * y.conjugate()).real
    if not math.isfinite(result):
        raise ValueError("cross term is not finite")
    return float(result)


def cross_term_after_transfers(
    a: SupportsComplex,
    b: SupportsComplex,
    transfer_a: SupportsComplex,
    transfer_b: SupportsComplex,
) -> float:
    """Apply independent field transfers, then evaluate the signed cross term."""
    return cross_term(
        propagate(a, transfer_a),
        propagate(b, transfer_b),
    )
